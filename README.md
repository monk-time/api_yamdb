# YaMDb

### Описание
Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Произведению может быть присвоен жанр из списка предустановленных. Добавлять произведения, категории и жанры может только администратор.

Пользователи могут оставлять отзывы на произведения, оценивать их (в диапазоне от 1 до 10) и обсуждать отзывы в комментариях. Из оценок формируется усреднённая оценка произведения — рейтинг. На одно произведение пользователь может оставить только один отзыв.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

Полная документация к API находится в файле `api_yamdb/static/redoc.yaml` и по эндпоинту `/redoc/`.

### Используемые технологии
- Python 3.9
- Django
- DRF
- djangorestframework-simplejwt

### Как запустить проект
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/monk-time/api_yamdb.git
cd api_yamdb
```

Для Linux/macOS здесь и далее используем python3 взамен python.

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

* Если у вас Linux/macOS:

    ```
    source env/bin/activate
    ```

* Если у вас Windows:

    ```
    source env/Scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Можно заполнить базу тестовыми данными:

```
python manage.py bulkupload
```

Запустить проект:

```
python manage.py runserver
```

### Пользовательские роли и права доступа

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, публиковать отзывы и ставить оценки произведениям, комментировать отзывы, редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Роль по умолчанию.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django - обладает правами Администратора.

### Ресурсы API:
- **auth**: аутентификация.
- **users**: пользователи.
- **titles**: произведения и информация о них.
- **categories**: категории произведений.
- **genres**: жанры произведений. Одно произведение может иметь несколько жанров
- **reviews**: отзывы на произведения. Каждый отзыв относится к определенному произведению.
- **comments**: комментарии к отзывам на произведения.

### Регистрация пользователя
1. Передайте на `/api/v1/auth/signup/` свои username и email. Использовать имя 'me' запрещено. Каждое поле должно быть уникальнымм. Если пользователя ещё нет в базе данных, он будет создан.

```http
POST /api/v1/auth/signup/

{
    "email": "string",
    "username": "string"
}

```

2. На ваш email будет отправлен код подтверждения.
3. Передайте на `/api/v1/auth/token/` свой email и confirmation_code из письма, в ответе вы получите JWT-токен.

```http
POST /api/v1/auth/token/

{
    "username": "string",
    "confirmation_code": "string"
}
```

### Примеры работы с API

Получение списка всех категорий: `GET /api/v1/categories/`

Получение списка всех отзывов: `GET /api/v1/titles/{title_id}/reviews/`

Получение пользователя: `GET /api/v1/users/{username}/`

Получение данных своей учетной записи: `GET /api/v1/users/me/`

Удаление категории: `DELETE /api/v1/categories/{slug}/`

Добавление жанра:

```http
POST /api/v1/genres/

{
    "name": "string",
    "slug": "string"
}
```

Добавление произведения:

```http
POST /api/v1/titles/

{
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
    ],
    "category": "string"
}
```

Добавление пользователя:

```http
POST /api/v1/users/

{
    "username": "string",
    "email": "user@example.com",
    "first_name": "string",
    "last_name": "string",
    "bio": "string",
    "role": "user"
}
```

### Команда разработки
Проект выполнен в рамках курса "Яндекс Практикум" по специальности "Python backend-разработчик".

Дмитрий Богорад [@monk-time](https://github.com/monk-time) (тимлид) - регистрация, подтверждение по e-mail, получение JWT-токена и управление пользователями. Права доступа.

Евгений Мокрушин [@JRushFobos](https://github.com/JRushFobos) (разработчик) - категории, жанры и произведения: модели, view и эндпойнты. Импорт данных в базу данных из .csv файлов.

Ленар Фазлыев [@LenarFazlyev](https://github.com/LenarFazlyev) (разработчик) - отзывы и комментарии: модели, view и эндпойнты. Рейтинги произведений.
