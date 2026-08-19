#!/bin/bash

# Скрипт для инициализации проекта

echo "🚀 Инициализация Media Monitoring Kherson..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Пожалуйста, установите Docker."
    exit 1
fi

# Проверка Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit 1
fi

# Создание .env файла
if [ ! -f .env ]; then
    echo "📝 Создание .env файла..."
    cp .env.example .env
    echo "✅ .env файл создан. Пожалуйста, обновите значения если необходимо."
fi

# Создание директорий
echo "📁 Создание необходимых директорий..."
mkdir -p backend/app/{api,tasks,nlp,parsers}
mkdir -p frontend/{app,components,lib,public}
mkdir -p scripts

# Build Docker images
echo "🐳 Сборка Docker образов..."
docker-compose build

# Start services
echo "▶️ Запуск сервисов..."
docker-compose up -d

# Wait for services
echo "⏳ Ожидание инициализации сервисов..."
sleep 10

# Check health
echo "✅ Проверка здоровья сервисов..."
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend здоров"
else
    echo "⚠️ Backend может быть не готов, проверьте logs"
fi

if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend здоров"
else
    echo "⚠️ Frontend может быть не готов, проверьте logs"
fi

echo ""
echo "🎉 Инициализация завершена!"
echo ""
echo "📊 Доступные сервисы:"
echo "  - Frontend: http://localhost:3000"
echo "  - Backend API: http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo "  - Database: postgres://localhost:5432"
echo "  - Redis: redis://localhost:6379"
echo ""
echo "📋 Полезные команды:"
echo "  - docker-compose logs -f              # Просмотр логов"
echo "  - docker-compose ps                   # Статус сервисов"
echo "  - docker-compose down                 # Остановка сервисов"
echo "  - docker-compose exec backend bash    # Вход в контейнер backend"
