# Foodgram

Foodgram — это веб-приложение, в котором пользователи могут делиться своими рецептами, просматривать рецепты других пользователей, подписываться на авторов, добавлять рецепты в избранное и список покупок, а также скачивать финальный список покупок для удобства.
Приложение доступно сайте www.olmazurova.ru, по IP 51.250.100.178:7000.

---

#### Основной функционал приложения:

1. Регистрация и аутентификация пользователей
    - Регистрация новых пользователей
    - Авторизация (вход/выход)
2. Работа с рецептами
    - Публикация новых рецептов (название, описание, ингредиенты, шаги приготовления, фото и т.п.)
    - Просмотр списка рецептов и подробной информации о каждом рецепте
    - Фильтрация и поиск по тегам, автору, названию и пр.
    - Редактирование и удаление своих рецептов
3. Подписки на авторов
    - Просмотр списка пользователей
    - Подписка/отписка на других пользователей
    - Просмотр списка своих подписок и их рецептов
4. Избранное
    - Добавление/удаление рецептов в избранное
    - Просмотр избранных рецептов
5. Список покупок
    - Добавление/удаление рецептов в список покупок
    - Просмотр списка покупок (агрегация ингредиентов по всем рецептам)
    - Скачивание списка покупок (в формате TXT)

## Стек технологий
Foodgram написан на Django 4.2, django rest framework 3.16.

### Доступные ендпоинты:
- api/users/ - список пользователей, регистрация пользователя
- api/users/id/ - профиль пользователя
- api/users/me/ - профиль текущего пользователя
- api/users/me/avatar/ - добавление и удаление аватара
- api/users/set_password/ - изменение пароля
- api/auth/token/login/ - вход
- api/auth/token/logout/ - выход
- api/tags/ - список тегов
- api/tags/{id}/ - информация о теге
- api/recipes/ - список всех рецептов, создание рецепта
- api/recipes/{id}/ - просмотр, редактирование или удаление рецепта
- api/recipes/{id}/get-link/ - короткая ссылка на рецепт
- api/recipes/download_shopping_cart/ - загрузить файл со списком покупок
- api/recipes/{id}/shopping_cart/ - добавить/удалить рецепт из списка покупок
- api/recipes/{id}/favorite/ - добавить/удалить рецепт из избранного
- api/users/subscriptions/ - список подписок текущего пользователя
- api/users/{id}/subscribe/ - подписаться/отписаться на пользователя
- api/ingredients/ - список всех ингредиентов
- api/ingredients/{id}/ - информация о конкретном ингредиенте

### Как развернуть проект локально в docker-контейнерах:

**1. Клонировать репозиторий:**

`git clone https://github.com/Olmazurova/foodgram.git`

**2. Cоздать свой файл с секретами на основе .env_example.**

**3. Запустить docker-compose.production.yml из директории foodgram, применить миграции и собрать статику:**

- На ОС Linux:

`sudo docker compose -f docker-compose.production.yml up -d
 sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
 sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
 sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/`

- На ОС Windows:

`docker compose -f docker-compose.production.yml up -d
 docker compose -f docker-compose.production.yml exec backend python manage.py migrate
 docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
 docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/`


### Примеры запросов
- Регистрация пользователя
`{
   "email": "vpupkin@yandex.ru",
   "username": "vasya.pupkin",
   "first_name": "Вася",
   "last_name": "Иванов",
   "password": "Qwerty123"
}`

  - Создание рецепта
`{
  "ingredients": [
   {
      "id": 1123,
      "amount": 10
   }
  ],
  "tags": [
   1,
   2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Очень вкусное блюдо",
  "text": "Приготовить быстро",
  "cooking_time": 1
}`

- Добавление аватара
`{
  "avatar": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg=="
  }`

- Получить токен
`{
  "email": "vasya.pupkin",
  "password": "Qwerty123"
}`

_____
Автор проекта: Ольга Мазурова
