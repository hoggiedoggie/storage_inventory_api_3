# Storage Inventory API
## Профессиональная система инвентаризации накопителей (HDD/SSD). 
### Реализовано:
- Многопользовательская архитектура с защитой данных на уровне владельца (Ownership) и безопасной сессионной авторизацией.
- Технологический стек Backend: Python 3.13 + FastAPI.Database: PostgreSQL + SQLAlchemy (ORM).Migrations: Alembic.
- Security: JWT (JSON Web Tokens), Bcrypt (хеширование паролей).DevOps: Docker + Docker Compose.
## Структура проекта.
```
├── app/ 
│   ├── api/ 
│   │   ├── deps.py             # Зависимости (проверка JWT + получение текущего юзера) 
│   │   └── v1/ 
│   │       └── endpoints/      # Обработчики API (auth.py/storage.py) 
│   ├── core/ 
│   │   ├── config.py           # Настройки проекта (Pydantic Settings + .env) 
│   │   └── security.py         # Логика хеширования и генерации токенов 
│   ├── db/ 
│   │   ├── base.py             # Сборка всех моделей для Alembic 
│   │   └── session.py          # Настройка подключения к БД 
│   ├── models/                 # SQLAlchemy модели (User, StorageDevice) 
│   ├── schemas/                # Pydantic схемы (валидация данных) 
│   ├── services/               # Бизнес-логика (CRUD операции) 
│   └── main.py                 # Точка входа в приложение 
├── alembic/                    # История миграций базы данных 
├── docker-compose.yml          # Оркестрация контейнеров 
├── Dockerfile                  # Инструкции сборки образа 
└── .env                        # Секретные ключи и настройки БД 
```
## Быстрый запуск
### 1. Сборка и запуск контейнеров
```
docker-compose up -d --build
```
### 2. Управление миграциями (База данных)
При первом запуске или изменении моделей выполните:

1. Создание новой миграции (фиксация изменений моделей)
~~~
docker-compose exec app alembic revision --autogenerate -m "full_fix"
~~~
2. Применение миграций к БД
~~~
docker-compose exec app alembic upgrade head
~~~
### 3. Проверка состояния БД
Убедитесь, что таблицы созданы корректно:
```
docker-compose exec db psql -U postgres -d inventory_db -c "\dt" 
```
## Примеры использования API
### 1. Регистрация пользователя
```
POST /api/v1/auth/register
``` 
```
JSON
{
  "email": "maho0math@example.com",
  "password": "strong_password123"
}
```
### 2. Авторизация (Логин)
```
POST /api/v1/auth/login После успешного входа сервер устанавливает HttpOnly Cookie с токеном доступа.
```
```
JSON
{
  "email": "maho0math@example.com",
  "password": "strong_password123"
}
```
