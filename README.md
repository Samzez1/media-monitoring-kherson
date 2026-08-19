````markdown
# 📰 Media Monitoring Kherson

Платформа для агрегации и анализа публикаций о Национальных проектах РФ в Херсонской области с использованием NLP технологий.

## 🎯 Основные возможности

- **📊 Агрегация данных** - Сбор статей из множества RSS источников
- **🤖 NLP классификация** - Автоматическая классификация по 12 Национальным проектам
- **📍 Геолокация** - Фильтрация по Херсонской области
- **⚡ Фоновая обработка** - Celery для асинхронного парсинга
- **🔍 Полнотекстовый поиск** - Поиск по заголовкам и содержимому
- **📈 Статистика** - Аналитика по проектам и источникам
- **🎨 Современный UI** - React/Next.js интерфейс

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────┐
│                   Frontend (Next.js)                    │
│                   http://localhost:3000                 │
└──────────────────────────┬──────────────────────────────┘
                           │
                    HTTP/REST API
                           │
┌──────────────────────────▼──────────────────────────────┐
│              Backend (FastAPI)                          │
│              http://localhost:8000                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │ API Routes:                                        │ │
│  │ - /api/v1/articles                                │ │
│  │ - /api/v1/projects                                │ │
│  │ - /api/v1/sources                                 │ │
│  └────────────────────────────────────────────────────┘ │
└──────────────────┬───────────────────┬──────────────────┘
                   │                   │
        ┌──────────▼──┐      ┌────────▼────────┐
        │   Database  │      │  Message Queue  │
        │ PostgreSQL  │      │    Redis        │
        │ :5432       │      │   :6379         │
        └─────────────┘      └────────┬────────┘
                                      │
                          ┌───────────▼──────────┐
                          │  Celery Worker       │
                          │  (Background Tasks)  │
                          │  - RSS Parsing       │
                          │  - NLP Processing    │
                          │  - Cleanup           │
                          └────────────���─────────┘
```

## 🛠️ Технологический стек

### Backend
- **Python 3.11** - Основной язык
- **FastAPI** - REST API фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Celery** - Асинхронная очередь задач
- **Redis** - Брокер сообщений и кэш
- **PostgreSQL** - Основная БД
- **Natasha** - NLP библиотека для русского языка
- **feedparser** - Парсинг RSS потоков

### Frontend
- **Next.js 14** - React фреймворк
- **TypeScript** - Типизированный JavaScript
- **Tailwind CSS** - Утилитарный CSS фреймворк
- **Axios** - HTTP клиент
- **Lucide React** - Иконки

### DevOps
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация контейнеров

## 📋 Национальные проекты

Система поддерживает классификацию по 12 Национальным проектам РФ:

1. 👨‍👩‍👧‍👦 **Демография** - Семья, рождаемость, материнский капитал
2. 🎭 **Культура** - Музеи, театры, выставки, памятники
3. 🎓 **Образование** - Школы, университеты, инновации в образовании
4. 🏥 **Здравоохранение** - Больницы, клиники, здоровый образ жизни
5. 🔬 **Наука и университеты** - Исследования, НИИ, лаборатории
6. 🏢 **Жилье и городская среда** - Строительство, благоустройство, парки
7. ♻️ **Экология** - Охрана природы, загрязнение, леса
8. 🛣️ **Безопасные качественные дороги** - БКД, транспорт, безопасность
9. 💻 **Цифровая экономика** - IT, интернет, электронные услуги
10. 💼 **МСП** - Малое и среднее предпринимательство
11. 🏨 **Туризм** - Туристический бизнес, гостиницы
12. 👶 **Семья** - Поддержка семей, многодетные

## 🚀 Быстрый старт

### Предварительные требования

- Docker & Docker Compose
- 4GB+ RAM
- 10GB+ свободного места на диске

### Установка и запуск

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/Samzez1/media-monitoring-kherson.git
cd media-monitoring-kherson
```

2. **Инициализируйте проект**
```bash
chmod +x scripts/*.sh
bash scripts/init.sh
```

3. **Откройте приложение**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs (Swagger): http://localhost:8000/docs

## 📖 Использование

### Frontend

**Главная страница**
- Просмотр всех статей о Национальных проектах
- Фильтрация по проектам и источникам
- Поиск по ключевым словам

**Фильтры слева**
- Выбор Национальных проектов
- Выбор источников информации
- Быстрая очистка фильтров

**Статьи**
- Просмотр заголовка, фрагмента текста
- Информация об источнике и дате публикации
- Ссылка на оригинальную статью
- Теги проектов и маркеры локации

### Backend API

**Получить статьи**
```bash
curl http://localhost:8000/api/v1/articles?page=1&page_size=20
```

**Получить проекты**
```bash
curl http://localhost:8000/api/v1/projects
```

**Получить источники**
```bash
curl http://localhost:8000/api/v1/sources
```

**Статистика по проектам**
```bash
curl http://localhost:8000/api/v1/articles/stats/by-project
```

**Поиск статей**
```bash
curl "http://localhost:8000/api/v1/articles/search/by-text?q=образование"
```

Полную документацию API смотрите на http://localhost:8000/docs

## 🔧 Управление проектом

### Полезные команды

```bash
# Просмотр логов всех сервисов
bash scripts/logs.sh

# Просмотр логов конкретного сервиса
bash scripts/logs.sh backend
bash scripts/logs.sh celery-worker
bash scripts/logs.sh frontend

# Остановка сервисов
docker-compose down

# Перезагрузка сервисов
docker-compose restart

# Вход в контейнер backend
docker-compose exec backend bash

# Вход в базу данных PostgreSQL
docker-compose exec postgres psql -U media_user -d media_monitoring

# Просмотр статуса сервисов
docker-compose ps

# Очистка проекта
bash scripts/cleanup.sh
```

## 📚 Структура проекта

```
media-monitoring-kherson/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI приложение
│   │   ├── config.py               # Конфигурация
│   │   ├── database.py             # SQLAlchemy модели
│   │   ├── schemas.py              # Pydantic схемы
│   │   ├── api/
│   │   │   ├── articles.py         # API для статей
│   │   │   ├── projects.py         # API для проектов
│   │   │   └── sources.py          # API для источников
│   │   ├── tasks/
│   │   │   └── parse_feeds.py      # Celery задачи
│   │   ├── nlp/
│   │   │   └── classifier.py       # NLP классификатор
│   │   └── parsers/
│   │       └── rss_parser.py       # RSS парсер
│   ├── requirements.txt
│   ├── Dockerfile
│   └── Dockerfile.worker
├── frontend/
│   ├── app/
│   │   ├── page.tsx               # Главная страница
│   │   ├── layout.tsx             # Root layout
│   │   └── globals.css            # Глобальные стили
│   ├── components/
│   │   ├── Header.tsx             # Заголовок
│   │   ├── ArticleCard.tsx        # Карточка статьи
│   │   ├── ArticleFeed.tsx        # Лента статей
│   │   └── FilterPanel.tsx        # Панель фильтров
│   ├── lib/
│   │   ├── api.ts                 # API клиент
│   │   └── types.ts               # TypeScript типы
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml              # Docker Compose конфигурация
├── .env.example                    # Шаблон переменных окружения
└── scripts/
    ├── init.sh                     # Инициализация проекта
    ├── logs.sh                     # Просмотр логов
    └── cleanup.sh                  # Очистка проекта
```

## ⚙️ Конфигурация

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Основные переменные:

```env
# Database
DATABASE_URL=postgresql://media_user:media_password@postgres:5432/media_monitoring

# Redis
REDIS_URL=redis://redis:6379/0

# API
API_V1_PREFIX=/api/v1
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# Parsers
PARSE_INTERVAL_MINUTES=60          # Интервал парсинга (часы)
MAX_ARTICLES_PER_SOURCE=100        # Макс статей с одного источника
ARTICLE_RETENTION_DAYS=90          # Хранение статей (дни)

# NLP
NLP_CONFIDENCE_THRESHOLD=0.5       # Порог уверенности классификации
USE_NATASHA=True                   # Использовать Natasha для NER
```

## 📊 База данных

### Модели

**Article** - Статья
- id, title, content, url, published_date
- source_id (ForeignKey to Source)
- national_projects (ManyToMany to NationalProject)
- location_markers, is_kherson_related

**Source** - Источник информации
- id, name, source_type (rss/telegram/website)
- url, is_active, last_parsed

**NationalProject** - Национальный проект
- id, name, description, keywords
- is_active, color_badge

**ParseLog** - Лог парсинга
- id, source_id, parse_start, parse_end
- status, articles_found, articles_saved

## 🔄 Расписание задач

Celery Beat запускает задачи по расписанию:

- **Каждый час**: Парсинг всех RSS источников
- **03:00 каждый день**: Удаление старых статей
- **Каждые 15 минут**: Обновление статистики

Отредактируйте `backend/app/tasks/parse_feeds.py` для изменения расписания.

## 🐛 Troubleshooting

### Backend не запускается
```bash
# Проверьте логи
bash scripts/logs.sh backend

# Пересоберите образ
docker-compose build --no-cache backend
docker-compose restart backend
```

### Frontend не загружает данные
- Проверьте, что backend работает: `curl http://localhost:8000/health`
- Проверьте CORS настройки в `.env`
- Посмотрите логи frontend: `bash scripts/logs.sh frontend`

### Статьи не парсятся
```bash
# Проверьте статус Celery worker
bash scripts/logs.sh celery-worker

# Запустите парсинг вручную
docker-compose exec backend python -c "from app.tasks.parse_feeds import parse_all_sources; parse_all_sources()"
```

### Проблемы с БД
```bash
# Проверьте подключение
docker-compose exec postgres psql -U media_user -d media_monitoring -c "SELECT 1;"

# Пересоздайте таблицы
docker-compose exec backend python -c "from app.database import init_db; init_db()"
```

## 📝 Лицензия

MIT License - см. LICENSE файл

## 👤 Автор

**Samzez1** - GitHub профиль: https://github.com/Samzez1

## 🤝 Контрибьютинг

Пулл-реквесты приветствуются! Для больших изменений сначала откройте Issue.

## 📬 Обратная связь

Если у вас есть вопросы или предложения, создайте Issue на GitHub.

---

**Made with ❤️ for monitoring National Projects of Russia in Kherson region**
````
