# BookSharing

BookSharing — асинхронный REST API для размещения книг и управления личной библиотекой пользователей.

Проект создан как учебный pet-project для практики backend-разработки на FastAPI, работы с PostgreSQL через SQLAlchemy, JWT-аутентификации, миграций базы данных, загрузки файлов и построения многослойной архитектуры.

## Возможности

### Пользователи и безопасность

- регистрация пользователей;
- аутентификация по JWT;
- access- и refresh-токены;
- обновление access-токена;
- хеширование паролей;
- получение текущего пользователя через зависимости FastAPI;
- разграничение доступа к защищённым операциям.

### Книги

- создание книги;
- получение списка книг;
- получение книги по идентификатору;
- изменение и удаление книги;
- проверка владельца при изменении и удалении;
- фильтрация по автору, жанру и владельцу;
- сортировка и пагинация;
- загрузка обложки;
- проверка типа и размера загружаемого файла;
- сохранение ссылки на обложку в базе данных.

### Инфраструктура

- асинхронная работа с PostgreSQL;
- миграции Alembic;
- обработка собственных исключений;
- middleware для централизованной обработки ошибок;
- административная панель на Starlette Admin;
- запуск PostgreSQL через Docker Compose;
- интерактивная документация Swagger и ReDoc.

## Технологии

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic
- asyncio
- JWT
- Starlette Admin
- Docker Compose
- uv
- pytest

## Архитектура

В проекте используется разделение приложения по зонам ответственности:

```text
HTTP-запрос
    ↓
API-роутеры
    ↓
Сервисный слой
    ↓
Репозитории
    ↓
SQLAlchemy-модели
    ↓
PostgreSQL
```

Основные директории:

```text
app/
├── admin/          # конфигурация административной панели
├── api/            # API-роутеры
├── core/           # настройки, БД, безопасность, middleware и исключения
├── models/         # SQLAlchemy-модели
├── repositories/   # запросы к базе данных
├── schemas/        # Pydantic-схемы
├── services/       # бизнес-логика
├── static/         # загруженные обложки
└── main.py         # создание FastAPI-приложения

tests/              # автоматические тесты приложения
migrations/         # миграции Alembic
db/                 # Dockerfile PostgreSQL
docker-compose.yml
alembic.ini
pyproject.toml
uv.lock
```

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone https://github.com/Iridium111/booksharing.git
cd booksharing
```

### 2. Установить зависимости

Проект использует `uv`:

```bash
uv sync
```

### 3. Настроить переменные окружения

Создайте файл `.env` в корне проекта и укажите параметры подключения к базе данных и настройки JWT.

Пример:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=booksharing
DB_USER=postgres
DB_PASSWORD=postgres

SECRET_KEY=change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30
```

Названия переменных должны совпадать с полями, объявленными в `app/core/config.py`.

### 4. Запустить PostgreSQL

```bash
docker compose up -d
```

Текущий `docker-compose.yml` запускает контейнер PostgreSQL и сохраняет данные в Docker volume.

### 5. Применить миграции

```bash
uv run alembic upgrade head
```

### 6. Запустить приложение

```bash
uv run uvicorn app.main:app --reload
```

После запуска:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- административная панель: `http://127.0.0.1:8000/admin`

Основные API-роуты подключены с префиксом:

```text
/api/v1
```

## Пример работы с книгами

Получение списка книг:

```http
GET /api/v1/books?author=tolkien&genre=fantasy&limit=10&offset=0
```

Создание книги:

```http
POST /api/v1/books
Authorization: Bearer <access_token>
Content-Type: application/json
```

```json
{
  "title": "The Hobbit",
  "author": "J. R. R. Tolkien",
  "genre": "Fantasy"
}
```

## Аутентификация и авторизация

Аутентификация определяет текущего пользователя с помощью JWT-токена.

Авторизация проверяет право пользователя выполнить действие. Изменять или удалять книгу может только её владелец.

```text
current_user.id == book.user_id
```

При несовпадении идентификаторов API возвращает `403 Forbidden`.

## Административная панель

Starlette Admin используется для просмотра и управления пользователями и книгами через браузер.
Реализована защита административной панели.

Панель доступна по адресу:

```text
/admin
```



## Статус проекта

Реализовано:

- JWT-аутентификация;
- access- и refresh-токены;
- обновление токенов;
- CRUD пользователей и книг;
- проверка владельца ресурса;
- фильтрация, сортировка и пагинация;
- загрузка обложек;
- миграции Alembic;
- собственные исключения и middleware;
- административная панель;
- PostgreSQL в Docker Compose;
- защита административной панели.

Планируется:

- роли пользователей;
- кэширование через Redis;
- автоматические тесты на Pytest (в процессе);
- логирование;
- развёртывание приложения.

## Автор

Евгений Бабкин

GitHub: [Iridium111](https://github.com/Iridium111)
