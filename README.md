# URL Shortener Service

Сервис сокращения URL с аналитикой переходов, аналогичный Bit.ly. Позволяет создавать короткие ссылки, отслеживать переходы по ним и просматривать аналитику.

## Основные возможности

- **Сокращение URL** с помощью алгоритмов CRC32 или nanoid
- **Редирект** с коротких ссылок на оригинальные
- **Аналитика переходов**:
  - Количество кликов
  - Геоданные (страна)
  - Устройства и браузеры
- **Визуализация данных**:
  - Графики по странам
  - Временные графики
- **Ограничение запросов** (до 1000 RPS)

## Технологии

- Python 3.10+
- FastAPI (асинхронный веб-фреймворк)
- PostgreSQL (основное хранилище)
- Redis (для rate limiting)
- SQLAlchemy 2.0 (асинхронный ORM)
- Pydantic (валидация данных)
- Matplotlib (визуализация аналитики)
- GeoIP2 (геолокация по IP)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/url-shortener.git
cd url-shortener
```

2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements/base.txt  # Для production
pip install -r requirements/dev.txt   # Для разработки
```

4. Настройте окружение:
Скопируйте пример конфигурации и отредактируйте его:
```bash
cp src/url_shortener/config.example.py src/url_shortener/config.py
```

5. Инициализируйте базу данных:
```bash
python scripts/migrate.py
```

## Запуск

Для разработки:
```bash
uvicorn src.url_shortener.main:app --reload
```

Для production:
```bash
uvicorn src.url_shortener.main:app --host 0.0.0.0 --port 80
```

После запуска сервис будет доступен по адресу: `http://localhost:8000`

## API Документация

После запуска сервиса документация API доступна по адресам:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Примеры использования

Смотрите [examples/example_usage.py](examples/example_usage.py) для примеров работы с API.

## Тестирование

Для запуска тестов:
```bash
pytest -v
```

## Лицензия

MIT License. Подробнее см. в файле LICENSE.
