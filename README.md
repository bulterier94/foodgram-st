# Проект "Foodgram"

---

## Клонирование проекта

Клонируйте репозиторий на вашу локальную машину:

```sh
https://github.com/bulterier94/foodgram-st.git
````

После выполнения этой команды появится в директории, откуда была выполнена команда, появится директория `foodgram-st`, в которой содержится проект.

---

## Запуск проекта

Перейдите в директорию `foodgram-st/infra`:

```sh
cd foodgram-st/infra
```

Создайте файл окружения `.env`.
Это можно сделать на основе примера `.env.example`:

```sh
cp .env.example .env
```

Пример содержания файла `.env`:

```env
DJANGO_SECRET_KEY=Your-Super-Secret-Key

DJANGO_CORS_ALLOWED_ORIGINS=http://localhost:3000
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_DEBUG=false

DB_NAME=example_db
DB_USER=example_db_user
DB_PASSWORD=example_password
DB_HOST=db
DB_PORT=5432

NGINX_PORT=80
BACKEND_PORT=8000
```

Находясь в этой же директории, запустите Docker контейнеры:

```sh
docker compose up -d --build
```

Убедиться, что все необходимые сервисы были запущены, можно с помощью команды:

```sh
docker ps
```

![image](https://github.com/user-attachments/assets/eb5b8264-032e-427c-9617-048f14d0fec2)


Приложение будет доступно по адресу:
**[http://localhost](http://localhost)**

---

##  Остановка проекта

Чтобы остановить и удалить все контейнеры и тома, выполните команду:

```sh
docker compose down -v
```

---

## База данных

Изначально в базу данных загружена фикстура с ингредиентами для приготовления рецептов:

```json
{
  "model": "ingredients.ingredient",
  "pk": 1,
  "fields": {
    "name": "абрикосовое варенье",
    "measurement_unit": "г"
  }
}
```

---

##  Сценарий использования

- Пользователь может **зарегистрировать новый аккаунт**:

![image](https://github.com/user-attachments/assets/b6406f36-28d2-4251-a2b5-eb03295a555e)

- Пользователь может **войти в существующий аккаунт**:

![image](https://github.com/user-attachments/assets/79d6f98b-c164-4403-9d45-88128e721c9c)

- Пользователь может **установить и удалить свою аватарку**:

![image](https://github.com/user-attachments/assets/4b152557-a00b-416b-bfb2-93dae56bf67f)

- Пользователь может **сменить свой пароль**:

![image](https://github.com/user-attachments/assets/b6288e36-1eeb-40c3-bd30-6c33e07b238f)

- Пользователь может **создать свой рецепт**:

![image](https://github.com/user-attachments/assets/27ee5d56-3658-4928-b866-ad6783c03098)

- Пользователь **находится на главной странице**. Он **видит список всех рецептов**:

![image](https://github.com/user-attachments/assets/fe83b850-77d0-4bd2-8738-bb74434caebc)

- Пользователь может **зайти на страницу рецепта**:

![image](https://github.com/user-attachments/assets/d120ed81-db95-4af2-98d8-52bacd649461)

- Пользователь может **редактировать рецепт**, если он принадлежит пользователю:

![image](https://github.com/user-attachments/assets/2a57f96d-1bd5-483f-9069-2a97cf545ffa)

- Пользователь может **добавить рецепт в избранное** и **удалить его оттуда**:

![image](https://github.com/user-attachments/assets/d9671330-ac14-4980-80b0-dfdc5c444abb)

- Пользователь может **добавить рецепт в список покупок** и **удалить его оттуда**:

![image](https://github.com/user-attachments/assets/74c79346-b5a3-4fd8-b74c-07f4439b18e6)

- Пользователь может **скопировать прямую ссылку на рецепт**:

![image](https://github.com/user-attachments/assets/c75d92ce-7b89-4c79-b44e-5cd758da7b04)

- Пользователь может **зайти на рецепт другого пользователя** и **подписаться на автора**, а также **отписаться от него**:

![image](https://github.com/user-attachments/assets/916fa208-055b-48a0-a2e4-6b1c030c5609)

- Пользователь может **посмотреть список своих подписок**:

![image](https://github.com/user-attachments/assets/378c4446-cd62-40e4-8b46-860fd7d25434)

- Пользователь может **посмотреть свой список избранных рецептов**:

![image](https://github.com/user-attachments/assets/0330aa42-dbda-4574-b07c-b6111e9fb6df)

- Пользователь может **посмотреть свой список покупок**:

  ![image](https://github.com/user-attachments/assets/9125628f-9046-4d8a-a4b8-e4cd138eb431)

- Пользователь может **скачать свой список покупок**:

![image](https://github.com/user-attachments/assets/674e321a-bfd6-47bf-96d5-704ce968b600)



















