## 📦 Storage Inventory API (Lab #3)

Профессиональная система инвентаризации накопителей (HDD/SSD). Реализована многопользовательская архитектура с защитой данных на уровне владельца (Ownership) и безопасной сессионной авторизацией через JWT.

## 🛠 Технологический стек

Backend: Python 3.13 + FastAPI.

Database: PostgreSQL + SQLAlchemy (ORM).

Migrations: Alembic.

Security: JWT (JSON Web Tokens), Bcrypt (хеширование паролей).

DevOps: Docker + Docker Compose.

## 📂 Структура проекта
```
storage_inventory_api/
├── alembic/                # Миграции базы данных (версии таблиц)
├── app/
│   ├── api/                # Слой обработки запросов (FastAPI)
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py     # Регистрация, логин, логаут
│   │   │   │   └── storage.py  # CRUD для твоих дисков (get, post, delete...)
│   │   │   └── api.py          # Сборщик всех роутеров в один
│   │   └── deps.py             # Тот самый "охранник" (get_current_user)
│   ├── core/               # Конфиги и безопасность
│   │   ├── config.py           # Настройки проекта (переменные из .env)
│   │   └── security.py         # Хеширование паролей и работа с JWT
│   ├── db/                 # Подключение к БД
│   │   ├── base.py             # Импорт всех моделей для Alembic
│   │   └── session.py          # Создание сессии SQLAlchemy
│   ├── models/             # Таблицы базы данных (SQLAlchemy)
│   │   ├── user.py             # Таблица пользователей
│   │   └── storage.py          # Таблица твоих железок/дисков
│   ├── schemas/            # Валидация данных (Pydantic)
│   │   ├── user.py             # Схемы для юзеров
│   │   ├── storage.py          # Схемы для дисков (что можно слать в POST/PATCH)
│   │   └── token.py            # Схемы для JWT ответов
│   ├── services/           # Бизнес-логика (самый важный слой)
│   │   ├── user.py             # Логика работы с юзерами
│   │   └── storage.py          # Логика работы с хранилищем (фильтрация по владельцу)
│   └── main.py                 # Точка входа в приложение
├── .env                    # Секреты (пароли БД, ключи JWT)
├── docker-compose.yml      # Описание контейнеров (App + Postgres)
├── Dockerfile              # Инструкция по сборке образа
└── requirements.txt        # Список библиотек
```

## 🚀 Быстрый запуск

1. Сборка и запуск контейнеров
```
docker-compose up -d --build
```

2. Управление миграциями (База данных)

При первом запуске или изменении моделей выполните:

Создание новой миграции (фиксация изменений):
```
docker-compose exec app alembic revision --autogenerate -m "full_fix"
```

Применение миграции к БД:
```
docker-compose exec app alembic upgrade head
```

3. Проверка состояния БД

Убедитесь, что таблицы созданы корректно:
```
docker-compose exec db psql -U postgres -d inventory_db -c "\dt"
```

## 🔐 Примеры использования API

1. Регистрация пользователя

### POST /api/v1/auth/register
```
{
  "email": "maho0math@example.com",
  "password": "strong_password123"
}
```

2. Авторизация (Логин)

### POST /api/v1/auth/login
Сервер проверяет учетные данные и устанавливает HttpOnly Cookie access_token.
```
{
  "email": "maho0math@example.com",
  "password": "strong_password123"
}
```

3. Работа с дисками (CRUD)

### POST /api/v1/storage/
Поле user_id подставляется автоматически из сессии пользователя.
```
{
  "model": "Kingston KC3000 1024GB",
  "serial_number": "K-SN-2026-999",
  "capacity_gb": 1024,
  "status": "active"
}
```

## 🛡 Безопасность и Особенности

HttpOnly Cookies: Токены защищены от кражи через JavaScript (защита от XSS-атак).

Data Ownership: Реализована жесткая фильтрация. Каждый пользователь имеет доступ только к своим записям.

UUID Идентификаторы: Используются UUID для защиты от подбора ID устройств (Insecure Direct Object Reference).

Bcrypt Hashing: Пароли хранятся в виде защищенных хэшей с солью.

## 📋 Полезные команды

Просмотр логов: docker-compose logs -f app

Перезапуск сервера: docker-compose restart app

Полная остановка: docker-compose down
