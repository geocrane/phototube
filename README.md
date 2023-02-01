# PhotoTube
**Бэкенд для социальной сети для фотографов.

#### Реализованы следюущие функции:
- Администрирование сайта, управление пользователями, сообщениями, группами, подписками.
- Регистрация, авторизация пользователя, сброс пароля по почте.
- Создания поста, включая загрузку изображения, описание и выбор жанра.
- Редактирование поста его автором.
- Оставления комментариев под постами сторонних пользователей.
- Подписка на посты избранных авторов.
- Фильтрация сообщений по группам, пользователям, избранным авторам.
- Пагинация, кэширование страниц
- Тестирование перечисленных функций с помощью Unittest.

Работа выполнена с использованием языка Python 3.7 и фреймворка Django 2.2.16.


#### Используемые технологии и библиотеки:
+ Python 3.7
+ Django 2.2.16
+ SQLite3
+ Unittest


#### Установка:
Создать виртуальное окружение:
```sh
$ python -m venv venv
```
Установить зависимости:
```sh
$ pip install -r requirements.txt
```
Примененить миграции:
```sh
$ python manage.py migrate
```
Запустить сервер-разработчика:
```sh
$ python manage.py runserver
```
Приложение в браузере по адресу:
```sh
http://127.0.0.1:8000/
```


##### Разработчик: [Сергей Журавлев](https://github.com/geocrane)