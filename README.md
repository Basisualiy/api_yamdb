# Проект YaMDb

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»). 
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). 
Добавлять произведения, категории и жанры может только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять комментарии к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.
## Пользовательские роли и права доступа

- Аноним — может просматривать описания произведений, читать отзывы и комментарии.
- Аутентифицированный пользователь (user) — может читать всё, как и Аноним, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- Модератор (moderator) — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- Администратор (admin) — полные права на управление всем контентом проекта. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
- Суперюзер Django должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

## Технологии

- Python
- Django
- DRF

## Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

    ```bash
        git clone <https://github.com/Basisualiy/api_yamdb.git>
    ```

2. Cоздать виртуальное окружение:

    windows

    ```bash
        python -m venv venv
    ```

    linux

    ```bash
        python3 -m venv venv
    ```

3. Активируйте виртуальное окружение

    windows

    ```bash
        source venv/Scripts/activate
    ```

    linux

    ```bash
        source venv/bin/activate
    ```

4. Установите зависимости из файла requirements.txt

    ```bash
        pip install -r requirements.txt
    ```

5. В папке с файлом manage.py выполните команду:

    windows

    ```bash
        python manage.py runserver
    ```

    linux

    ```bash
        python3 manage.py runserver
    ```

## Документация к проекту

Документация для API после установки доступна по адресу

```url
    http://127.0.0.1.8000/redoc/
```

## Регистрация пользователя и получение токена

Осуществялется путем контрактации двух аргументов email и username, путем извлечения подстроки из полученного хэш-згачения, которая в дальгейшем используется для генирации кода подтверждения, который затем отправляется пользователю по электронной почте для подтверждения регистрации.
Пользователй также может создавать и администратор через админ зону - описание полей в документации.

## Примеры запросов

- GET-Response: <http://127.0.0.1:8000/api/v1/titles/1/>

Request:

```J-SON
{
    "id": 1,
    "name": "Побег из Шоушенка",
    "year": 1994,
    "description": null,
    "genre": [
        {
            "name": "Драма",
            "slug": "drama"
        }
    ],
    "category": {
        "name": "Фильм",
        "slug": "movie"
    },
    "rating": 10
}
```

- GET-Response: <http://127.0.0.1:8000/api/v1/titles/1/reviews/1/>

Request:

```J-SON
{
    "id": 1,
    "author": "bingobongo",
    "title": 1,
    "text": 
        "Ставлю десять звёзд!\n...Эти голоса были чище и светлее тех,
        о которых мечтали в этом сером, убогом месте. Как будто две птички 
        влетели и своими голосами развеяли стены наших клеток, и на короткий
        миг каждый человек в Шоушенке почувствовал себя свободным.",
    "score": 10,
    "pub_date": "2023-02-05T18:06:02.054698Z"
}
```

## Авторы

Студенты курса "Python-разработчик расширенный" от Яндекс-Практикума:

[Василий Яковлев](https://github.com/Basisualiy)

[Кристина Гордийчук](https://github.com/Christina-Gordiichuk)

[Ярослав Бочков](https://github.com/YroslavBochkov)

