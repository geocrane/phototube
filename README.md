<h1 align="center">PhotoTube</a></h1>
<p align="center">**Бэкенд социальной сети для фотографов.**</p>

<p align="center"><img src="https://img.shields.io/badge/made%20by-geocrane-green">
<img src=https://img.shields.io/badge/Python-%203.7-blue>
<img src=https://img.shields.io/badge/Django%20-%202.2.16-red>
</p>

## Реализовано:
- Администрирование сайта, управление пользователями, сообщениями, группами, подписками.
- Регистрация, авторизация пользователя, сброс пароля по почте.
- Создания поста, включая загрузку изображения, описание и выбор жанра.
- Редактирование поста его автором.
- Оставления комментариев под постами сторонних пользователей.
- Подписка на посты избранных авторов.
- Фильтрация сообщений по группам, пользователям, избранным авторам.
- Пагинация, кэширование страниц
- Тестирование перечисленных функций с помощью Unittest.

## Используется:
- Python 3.7
- Django 2.2.16
- SQLite 3

## Запуск проекта (на примере Linux):
Cклонируйте репозиторий на локальный пк:
```
git clone https://github.com/geocrane/phototube.git
```
Войдите в склонированный репозиторий.
Для запуска на локальном сервере поочередно выполните:
```
python3 -m venv venv

source venv/bin/activate

python3 -m pip install --upgrade pip

pip install -r requirements.txt

cd phototube

python3 manage.py migrate

python3 manage.py runserver
```

Приложение в браузере по адресу:
```sh
http://127.0.0.1:8000/
```



<h3 align="center">developed by: Sergey S. Zhuravlev</h5>