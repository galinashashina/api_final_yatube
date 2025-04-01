# api_final

Вот сокращённый вариант README.md:

# Проект API для социальной сети

## Описание
Этот проект представляет собой REST API для социальной сети, позволяющей пользователям создавать посты, оставлять комментарии, подписываться на других пользователей и создавать группы. Проект использует Django и Django REST Framework.

### Задачи проекта:
- Управление постами и комментариями
- Возможность подписки на других пользователей
- Создание и управление группами

## Установка

1. Клонируйте репозиторий:
    bash
    git clone https://github.com/....git
    cd ваш-репозиторий

2. Создайте и активируйте виртуальное окружение:
    bash
    python -m venv venv
    source venv/bin/activate  # для macOS/Linux

3. Установите зависимости:
    bash
    pip install -r requirements.txt

4. Выполните миграции:
    bash
    python manage.py migrate

5. Запустите сервер:
    bash
    python manage.py runserver

Теперь доступ к API по адресу: http://127.0.0.1:8000/

## Примеры запросов к API

1. **Создание поста**
   `POST /api/v1/posts/`
    json
    {
        "text": "Это мой первый пост!",
        "group": 1
    }

2. **Получение комментариев к посту**
   `GET /api/v1/posts/{post_id}/comments/`

3. **Подписка на пользователя**
   `POST /api/v1/follow/`
    json
    {
        "following": "testuser2"
    }

4. **Получение списка подписок**
   `GET /api/v1/follow/`

## Технологии
- Django
- Django REST Framework
- PostgreSQL
- JWT (для аутентификации)
