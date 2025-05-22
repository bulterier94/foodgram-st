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

![image](https://github.com/user-attachments/assets/431fb0b4-b983-4e89-8e8f-33847b06ce0c)

- Пользователь **находится на главной странице**. Он **видит список всех рецептов**:

![image](https://github.com/user-attachments/assets/987d620c-0be9-4ddf-90d7-b6fb795c5bc7)

- Пользователь может **зайти на страницу рецепта**:

![image](https://github.com/user-attachments/assets/a1ec72b8-5e73-45c2-b2aa-e87d2efc2311)

- Пользователь может **редактировать рецепт**, если он принадлежит пользователю:

![image](https://github.com/user-attachments/assets/c0ac468c-2ea7-49cd-8f90-0fc45b0b940b)

- Пользователь может **добавить рецепт в избранное** и **удалить его оттуда**:

![image](https://github.com/user-attachments/assets/40974b08-debf-4973-872a-17274f7ea9a7)

- Пользователь может **добавить рецепт в список покупок** и **удалить его оттуда**:

![image](https://github.com/user-attachments/assets/c14eecbd-dd6f-4e41-b085-e524d1ec4816)

- Пользователь может **скопировать прямую ссылку на рецепт**:

![image](https://github.com/user-attachments/assets/d0ffddcb-d410-42d7-8737-687d668db014)

- Пользователь может **зайти на рецепт другого пользователя** и **подписаться на автора**, а также **отписаться от него**:

![image](https://github.com/user-attachments/assets/245b91b9-9f2d-4b7f-985f-408536f6a10c)

- Пользователь может **посмотреть список своих подписок**:

![image](https://github.com/user-attachments/assets/f6e405a0-bd82-4d34-ae35-d099a936323c)

- Пользователь может **посмотреть свой список избранных рецептов**:

![image](https://github.com/user-attachments/assets/8349d9ca-8502-493a-8629-edb88637f751)

- Пользователь может **посмотреть свой список покупок**:

![image](https://github.com/user-attachments/assets/be86c9b9-de34-4348-ab41-1fe4703d8307)

- Пользователь может **скачать свой список покупок**:

![image](https://github.com/user-attachments/assets/674e321a-bfd6-47bf-96d5-704ce968b600)



















