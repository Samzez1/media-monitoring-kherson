````markdown
# Руководство для контрибьютеров

Спасибо за интерес к Media Monitoring Kherson! Этот документ описывает, как вы можете помочь в развитии проекта.

## 📋 Кодекс поведения

- Будьте уважительны к другим участникам
- Не используйте оскорбления или дискриминационный язык
- Сосредоточьтесь на конструктивной критике
- Помните, что за экраном сидят реальные люди

## 🚀 Как начать

### 1. Fork репозитория

```bash
# Перейдите на https://github.com/Samzez1/media-monitoring-kherson
# Нажмите "Fork" в верхнем правом углу
```

### 2. Клонируйте свой fork

```bash
git clone https://github.com/YOUR_USERNAME/media-monitoring-kherson.git
cd media-monitoring-kherson
git remote add upstream https://github.com/Samzez1/media-monitoring-kherson.git
```

### 3. Создайте ветку для вашего фича

```bash
git fetch upstream
git checkout -b feature/your-feature-name upstream/main
```

## 🐛 Типы вклада

### Регистрация проблем (Issues)

Если вы нашли ошибку или у вас есть идея, создайте Issue:

```markdown
**Описание проблемы**
Четкое и лаконичное описание того, что не так.

**Шаги для воспроизведения**
1. Перейти на...
2. Нажать на...
3. Увидеть ошибку

**Ожидаемое поведение**
Что должно было произойти

**Фактическое поведение**
Что произошло на самом деле

**Окружение**
- OS: [e.g. Windows, macOS, Linux]
- Browser: [e.g. Chrome, Firefox]
- Docker: [e.g. 20.10.0]
- Docker Compose: [e.g. 1.29.0]

**Скриншоты/логи**
Если применимо
```

### Развитие функций (Features)

1. Обсудите идею в Issue перед началом работы
2. Создайте ветку: `feature/descriptive-name`
3. Разработайте функцию
4. Напишите/обновите тесты
5. Обновите документацию
6. Сделайте Pull Request

### Исправление ошибок (Bug Fixes)

1. Создайте Issue с описанием ошибки
2. Создайте ветку: `fix/issue-description`
3. Исправьте ошибку
4. Добавьте тесты для проверки
5. Сделайте Pull Request с ссылкой на Issue

### Документация

1. Обновления README, CONTRIBUTING, и других .md файлов
2. Улучшения в документировании кода
3. Примеры использования API

## 📝 Правила кодирования

### Python (Backend)

```python
# Используйте type hints
def parse_article(url: str, timeout: int = 30) -> Optional[Article]:
    """
    Парсит статью с заданного URL.
    
    Args:
        url: URL статьи для парсинга
        timeout: Таймаут соединения в секундах
        
    Returns:
        Объект Article если успешно, иначе None
    """
    pass

# Следуйте PEP 8
# Используйте docstrings для всех функций и классов
# Добавляйте логирование для важных операций
```

### TypeScript (Frontend)

```typescript
// Используйте явное типизирование
interface ArticleProps {
  article: Article;
  onSelect?: (id: number) => void;
}

const ArticleComponent: React.FC<ArticleProps> = ({ article, onSelect }) => {
  // Компонент код
};

// Используйте kebab-case для имен файлов
// Components -> components/article-card.tsx

// Добавляйте JSDoc комментарии
```

### CSS/Tailwind

```css
/* Организуйте стили логически */
/* Используйте Tailwind утилиты где возможно */
/* Избегайте глубокой вложенности */

@layer components {
  .btn-primary {
    @apply px-4 py-2 rounded font-medium bg-primary text-white hover:bg-blue-600 transition-colors;
  }
}
```

## 🧪 Тестирование

### Backend

```bash
# Установите зависимости для тестирования
pip install pytest pytest-cov

# Запустите тесты
pytest backend/tests/

# С покрытием
pytest --cov=backend backend/tests/
```

### Frontend

```bash
# Запустите тесты
npm test

# С покрытием
npm test -- --coverage
```

## ✅ Перед Pull Request

1. **Обновите основную ветку**
```bash
git fetch upstream
git rebase upstream/main
```

2. **Запустите тесты**
```bash
# Backend
pytest

# Frontend
npm test
```

3. **Проверьте линтинг**
```bash
# Backend
flake8 backend/
pylint backend/

# Frontend
npm run lint
```

4. **Форматируйте код**
```bash
# Backend
black backend/
isort backend/

# Frontend
prettier --write frontend/
```

5. **Обновите документацию**
   - Добавьте docstrings к новым функциям
   - Обновите README если нужно
   - Добавьте примеры использования

## 📬 Процесс Pull Request

### Создание PR

1. **Хорошее описание PR**
```markdown
## Описание

Краткое описание того, что делает этот PR.

## Связанные Issues

Closes #123

## Тип изменения

- [ ] Исправление ошибки
- [x] Новая функция
- [ ] Разломающее изменение
- [ ] Обновление документации

## Как это было протестировано?

Описание тестов, которые вы запустили.

## Скриншоты (если применимо)

Добавьте скриншоты для UI изменений.

## Чек-лист

- [x] Мой код следует стилю проекта
- [x] Я выполнил self-review своего кода
- [x] Я добавил комментарии к сложным частям
- [x] Я обновил документацию
- [x] Я добавил тесты
- [x] Все новые и существующие тесты прошли
```

### Ответы на отзывы

- Отвечайте на все комментарии
- Просите уточнения если что-то неясно
- Делайте обновления небольшими commits с ясными сообщениями

### После одобрения

Мейнтейнер объединит ваш PR в main ветку.

## 📚 Структура проекта

```
backend/
  app/
    api/           # REST API маршруты
    tasks/         # Celery задачи
    nlp/           # NLP модули
    parsers/       # Парсеры данных
  tests/           # Unit тесты
  requirements.txt

frontend/
  app/             # Next.js страницы
  components/      # React компоненты
  lib/             # Утилиты и типы
  tests/           # Jest тесты
  package.json
```

## 🔄 Релизный процесс

1. Мейнтейнер создает ветку `release/vX.Y.Z`
2. Обновляется версия в `package.json` и `pyproject.toml`
3. Обновляется CHANGELOG.md
4. Создается Pull Request в main
5. После одобрения, создается тег и релиз на GitHub

## 📖 Дополнительные ресурсы

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [How to Write a Good Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Python Code Style - PEP 8](https://pep8.org/)
- [TypeScript Best Practices](https://www.typescriptlang.org/docs/handbook/2/narrowing.html)

## ❓ Вопросы?

- Откройте Discussion на GitHub
- Создайте Issue с тегом `question`
- Свяжитесь с мейнтейнером

## 🎉 Спасибо!

Ваш вклад помогает сделать этот проект лучше для всех!

---

**Remember: Great open source comes from a great community** 🚀
````
