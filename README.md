# Техническое задание

> будет дополняться

## Tetris

Онлайн тетрис с таблицей рекордов и Турнирами.

## Возможности пользователей

* Регистрация для сохранения своих рекордов и отображения в общей таблице
* Игра в Tetris
* Вызов других пользователей (с предложение побить рекорд)
* Прохождение Турнира

## Виды игр
### Классическая игра в тетрис
Игра  представляет собой страницу сайта с полем для игры и управляется стрелками клавиатуры. Рядом с игровым полем в режими реального времени выводится таблица последних рекордов по всем игрокам и личным рекордом (если пользователь зарегистрирован).

### Турнир
Турнир представляет собой комнату (отдельную страницу сайта для каждого турнира), в которой находятся игроки. Каждому игроку предоставляется соперник. Они играют по одной партии, и победитель (набравший наибольшее количество очков) переходит к следующему раунду, а проигравший выбывает. Так продолжается до победы одного участника в финале.

### Вызов
Является по сути одним раундом в турнире между двумя игроками. 

## Стек технологий
* Python Flask для реализации бэкенда
* HTML+CSS+JS для реализации фроненда
* База данных SQLite (модуль SQLAlchemy для работы в Python) для хранения данных