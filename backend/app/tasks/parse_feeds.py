"""
Celery задачи для фонового парсинга и обработки статей
"""
from celery import Celery, shared_task
from app.config import get_settings
from app.database import SessionLocal, Source, Article, NationalProject, ParseLog
from app.parsers.rss_parser import RSSParser
from app.nlp.classifier import classifier
from datetime import datetime, timedelta
import logging

settings = get_settings()

# Инициализация Celery
celery_app = Celery(
    'media_monitoring',
    broker=settings.redis_url,
    backend=settings.redis_url
)

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def parse_rss_source(self, source_id: int):
    """
    Парсинг RSS источника
    
    Args:
        source_id: ID источника в БД
    """
    db = SessionLocal()
    try:
        source = db.query(Source).filter(Source.id == source_id).first()
        if not source or not source.is_active:
            logger.warning(f"Source {source_id} not found or inactive")
            return
        
        # Создание лога парсинга
        parse_log = ParseLog(
            source_id=source_id,
            parse_start=datetime.utcnow(),
            status="pending"
        )
        db.add(parse_log)
        db.commit()
        
        logger.info(f"Starting to parse source: {source.name}")
        
        # Парсинг RSS
        rss_parser = RSSParser()
        articles_data = rss_parser.parse_feed(source.rss_url)
        
        if not articles_data:
            parse_log.status = "failed"
            parse_log.error_message = "Failed to parse RSS feed"
            parse_log.parse_end = datetime.utcnow()
            db.commit()
            return
        
        parse_log.articles_found = len(articles_data)
        articles_saved = 0
        
        # Обработка каждой статьи
        for article_data in articles_data[:settings.max_articles_per_source]:
            try:
                # Проверка, не существует ли статья
                existing = db.query(Article).filter(
                    Article.url == article_data["url"]
                ).first()
                
                if existing:
                    logger.debug(f"Article already exists: {article_data['url']}")
                    continue
                
                # NLP обработка
                nlp_result = classifier.process_article(
                    text=article_data["content"],
                    title=article_data["title"]
                )
                
                # Если статья не о Херсоне - пропустить
                if not nlp_result["is_kherson_related"]:
                    logger.debug(f"Article not Kherson-related: {article_data['title']}")
                    continue
                
                # Если не найдено Национальных проектов - пропустить
                if not nlp_result["national_projects"]:
                    logger.debug(f"No projects found in article: {article_data['title']}")
                    continue
                
                # Создание объекта статьи
                article = Article(
                    title=article_data["title"],
                    content=article_data["content"],
                    snippet=article_data["snippet"],
                    url=article_data["url"],
                    source_id=source_id,
                    published_date=article_data["published_date"],
                    location_markers=nlp_result["location_markers"],
                    is_kherson_related=True,
                    author=article_data.get("author"),
                    raw_text=article_data["content"],
                    is_processed=True
                )
                
                db.add(article)
                db.flush()  # Получить ID статьи
                
                # Привязка Национальных проектов к статье
                for project_name, confidence in nlp_result["national_projects"].items():
                    project = db.query(NationalProject).filter(
                        NationalProject.name == project_name
                    ).first()
                    
                    if project:
                        article.national_projects.append(project)
                
                db.commit()
                articles_saved += 1
                logger.info(f"Saved article: {article.title}")
                
            except Exception as e:
                logger.error(f"Error processing article: {e}")
                db.rollback()
                continue
        
        # Обновление лога парсинга
        parse_log.articles_saved = articles_saved
        parse_log.status = "success"
        parse_log.parse_end = datetime.utcnow()
        
        # Обновление времени последнего парсинга источника
        source.last_parsed = datetime.utcnow()
        source.parse_error_count = 0
        
        db.commit()
        logger.info(f"Successfully parsed {source.name}: saved {articles_saved} articles")
        
    except Exception as exc:
        logger.error(f"Error parsing source {source_id}: {exc}")
        source = db.query(Source).filter(Source.id == source_id).first()
        if source:
            source.parse_error_count += 1
            db.commit()
        
        # Retry с экспоненциальным бэкоффом
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
    
    finally:
        db.close()


@shared_task
def parse_all_sources():
    """
    Парсинг всех активных RSS источников
    Запускается периодически (по расписанию)
    """
    db = SessionLocal()
    try:
        sources = db.query(Source).filter(
            Source.is_active == True,
            Source.source_type == "rss"
        ).all()
        
        logger.info(f"Starting to parse {len(sources)} sources")
        
        for source in sources:
            parse_rss_source.delay(source.id)
        
        logger.info(f"Queued {len(sources)} sources for parsing")
        
    finally:
        db.close()


@shared_task
def cleanup_old_articles():
    """
    Удаление старых статей (старше retention_days)
    """
    db = SessionLocal()
    try:
        cutoff_date = datetime.utcnow() - timedelta(
            days=settings.article_retention_days
        )
        
        old_articles = db.query(Article).filter(
            Article.created_at < cutoff_date
        ).all()
        
        count = len(old_articles)
        
        for article in old_articles:
            db.delete(article)
        
        db.commit()
        logger.info(f"Deleted {count} old articles")
        
    except Exception as e:
        logger.error(f"Error cleaning up articles: {e}")
        db.rollback()
    
    finally:
        db.close()


@shared_task
def update_statistics():
    """
    Обновление статистики (кэширование)
    """
    db = SessionLocal()
    try:
        total_articles = db.query(Article).count()
        total_sources = db.query(Source).filter(Source.is_active == True).count()
        total_projects = db.query(NationalProject).count()
        
        logger.info(
            f"Statistics: {total_articles} articles, "
            f"{total_sources} sources, {total_projects} projects"
        )
        
    finally:
        db.close()


# Celery Beat configuration (в production использовать celery-beat)
from celery.schedules import crontab

celery_app.conf.beat_schedule = {
    'parse-all-sources': {
        'task': 'app.tasks.parse_feeds.parse_all_sources',
        'schedule': crontab(minute=0),  # Каждый час
    },
    'cleanup-old-articles': {
        'task': 'app.tasks.parse_feeds.cleanup_old_articles',
        'schedule': crontab(hour=3, minute=0),  # 03:00 каждый день
    },
    'update-statistics': {
        'task': 'app.tasks.parse_feeds.update_statistics',
        'schedule': crontab(minute='*/15'),  # Каждые 15 минут
    },
}

celery_app.conf.timezone = 'UTC'
