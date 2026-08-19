# Media Monitoring Kherson - Национальные проекты РФ

Веб-приложение для агрегации и мониторинга публикаций о реализации Национальных проектов РФ на территории Херсонской области.

## 🎯 Функциональность

- **Агрегация данных**: Парсинг RSS-лент (ТАСС, РИА, Интерфакс), региональных порталов и Telegram-каналов
- **Геолокация**: Автоматическая фильтрация статей по маркерам локации (Херсон, Геническ, Каховка и т.д.)
- **NLP Классификация**: Извлечение и классификация 12 Национальных проектов РФ
- **Интерактивная лента**: Просмотр карточек с бейджами Нацпроектов, сортировка по дате
- **Фильтры**: По Нацпроекту, источнику, дате

## 🏗️ Архитектура

```
media-monitoring-kherson/
├── backend/                  # FastAPI приложение
│   ├── app/
│   │   ├── main.py          # Entry point
│   │   ├── config.py        # Конфигурация
│   │   ├── models.py        # SQLAlchemy модели
│   │   ├── database.py      # DB подключение
│   │   ├── schemas.py       # Pydantic схемы
│   │   ├── parsers/         # Парсеры данных
│   │   │   ├── rss_parser.py
│   │   │   ├── scrapy_spider.py
│   │   │   └── telegram_parser.py
│   │   ├── nlp/             # NLP модуль
│   │   │   ├── classifier.py
│   │   │   └── entity_extractor.py
│   │   ├── api/             # API маршруты
│   │   │   ├── articles.py
│   │   │   ├── projects.py
│   │   │   └── sources.py
│   │   └── tasks/           # Celery задачи
│   │       └── parse_feeds.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                 # Next.js приложение
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   └── api/
│   ├── components/
│   │   ├── ArticleCard.tsx
│   │   ├── ArticleFeed.tsx
│   │   ├── FilterPanel.tsx
│   │   └── Header.tsx
│   ├── lib/
│   │   ├── api.ts
│   │   └── types.ts
│   ├── styles/
│   ├── package.json
│   ├── next.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── docker-compose.yml        # Оркестрация контейнеров
├── .env.example              # Переменные окружения
├── .gitignore
└── README.md
```

## 🛠️ Технический стек

### Backend
- **Framework**: FastAPI + Uvicorn
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Task Queue**: Celery + Redis
- **Parsing**: Feedparser, BeautifulSoup4, Scrapy, Playwright
- **NLP**: Natasha, pymorphy2, spaCy

### Frontend
- **Framework**: Next.js 14 (React 18)
- **Styling**: TailwindCSS
- **HTTP Client**: axios/fetch
- **State Management**: React Context API

### DevOps
- **Containerization**: Docker + Docker Compose
- **VCS**: Git + GitHub

## 📋 Требования

- Docker & Docker Compose
- Git
- Python 3.11+ (для локальной разработки)
- Node.js 18+ (для локальной разработки)

## 🚀 Быстрый старт

### 1. Клонировать репозиторий
```bash
git clone https://github.com/Samzez1/media-monitoring-kherson.git
cd media-monitoring-kherson
```

### 2. Настроить переменные окружения
```bash
cp .env.example .env
# Отредактируйте .env согласно вашим параметрам
```

### 3. Запустить через Docker Compose
```bash
docker-compose up --build
```

Приложение будет доступно:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### 4. Первый запуск парсеров
```bash
docker-compose exec backend celery -A app.tasks call app.tasks.parse_feeds.parse_all_sources
```

## 📚 API Endpoints

### Articles
- `GET /api/articles` - Получить список статей с фильтрацией
- `GET /api/articles/{id}` - Получить деталь статьи
- `GET /api/articles/search?q=query` - Поиск по тексту

### Projects
- `GET /api/projects` - Список всех Национальных проектов
- `GET /api/projects/{id}/articles` - Статьи по проекту

### Sources
- `GET /api/sources` - Список источников
- `GET /api/sources/{id}/articles` - Статьи от источника

## 🔍 Национальные проекты

Приложение отслеживает следующие проекты:
1. Демография
2. Культура
3. Образование
4. Здравоохранение
5. Наука и университеты
6. Жилье и городская среда
7. Экология
8. Безопасные качественные дороги
9. Цифровая экономика
10. Малое и среднее предпринимательство
11. Туризм и индустрия гостеприимства
12. Семья

## 🌍 Источники данных

- **Федеральные агентства**: ТАСС, РИА Новости, Интерфакс
- **Региональные порталы**: Kherson.ks и локальные издания
- **Social Media**: Telegram-каналы (через Telethon)
- **Локальные сайт��**: Мониторинг госсайтов и муниципальных портал

## 🛡️ Фильтрация локации

Статьи автоматически фильтруются по маркерам:
- Город: Херсон, Геническ, Каховка
- Регион: Херсонская область, Херсонской
- Районы: Голопристанський, Скадовськ, Чорноморськ

## 📊 Database Schema

### Articles
```sql
CREATE TABLE articles (
  id SERIAL PRIMARY KEY,
  title VARCHAR(500) NOT NULL,
  content TEXT NOT NULL,
  snippet VARCHAR(1000),
  url VARCHAR(2048) UNIQUE NOT NULL,
  source_id INTEGER NOT NULL REFERENCES sources(id),
  published_date TIMESTAMP NOT NULL,
  fetched_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  location_markers TEXT[],
  raw_text TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE article_projects (
  id SERIAL PRIMARY KEY,
  article_id INTEGER NOT NULL REFERENCES articles(id) ON DELETE CASCADE,
  project_id INTEGER NOT NULL REFERENCES national_projects(id),
  confidence FLOAT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE national_projects (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  keywords TEXT[],
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sources (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  type VARCHAR(50), -- 'rss', 'telegram', 'website'
  url VARCHAR(2048),
  is_active BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🔄 Workflow парсинга

1. **Периодически** (каждый час) запускаются Celery задачи
2. **Парсеры** извлекают новые статьи из источников
3. **Фильтрация** по локации (Херсонская область)
4. **NLP классификация** определяет связанные Нацпроекты
5. **Сохранение** в PostgreSQL с метаданными
6. **Frontend** отображает актуальные данные

## 🧪 Тестирование

```bash
# Backend тесты
docker-compose exec backend pytest

# Frontend тесты
docker-compose exec frontend npm test
```

## 📝 Логирование

Логи доступны через Docker:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## 🚢 Production Deploy

### Подготовка к продакшену

1. Обновить `.env` для production
2. Использовать переменные окружения для sensitive данных
3. Настроить HTTPS (nginx/Traefik)
4. Настроить резервные копии PostgreSQL
5. Использовать managed Redis (AWS ElastiCache, Heroku Redis)

### Deploy на облако

**Пример для Heroku:**
```bash
heroku create media-monitoring-kherson
heroku addons:create heroku-postgresql:standard-0
heroku addons:create heroku-redis:premium-0
git push heroku main
```

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Samzez1

## 📞 Контакты & Поддержка

Для вопросов создавайте Issues на GitHub.

---

**Статус**: 🚧 В разработке
**Версия**: 0.1.0
