# Счётчик посещений

Автор: Сычев Иван Валерьевич ФТ-204-2

## Описание

Сайт на FastAPI для просмотра смешных гивок (пока только главная страница и две страницы с гифками).
Сделано API для получения статистики о посещениях сайта:

* количество посещений за день/месяц/год/всего
* количество уникальных посещений за день/месяц/год/всего

Чтобы начать отслеживать конкретную страницу сайта, нужно всего лишь указать декоратор `@session_counter` на 
методах обработки путей FastAPI.

## Требования

* Использование FastAPI
* Рабочий сайт
* Для этого сайта API получения статистики посещений за день/месяц/год/всего, поддержка статистики 
уникальных пользователей
* REST API
* При перезапуске сервера статистика не теряется

## Сайт

* Главная страница `/`
* Первая гифка `/lowPollyFloppa`
* Вторая гифка `/dancingPolishCow`

## Примеры запросов к API статистики о посещениях

* Статистика за все время (и уникальная, и обычная) `/api/v1/statistics/sessionCount`
* Статистика за все время (уникальная) `/api/v1/statistics/sessionCount?unique=true`
* Статистика за все время (обычная) `/api/v1/statistics/sessionCount?unique=false`
* Вернет 422 `/api/v1/statistics/sessionCount?unique=123`
* Статистика за 07-11-2022, за 11-2022, за 2022 (и уникальная, и обычная) `/api/v1/statistics/sessionCount/07-11-2022`
* Статистика за 07-11-2022, за 11-2022, за 2022 (уникальная) `/api/v1/statistics/sessionCount/07-11-2022?unique=true`
* Статистика за 07-11-2022, за 11-2022, за 2022 (обычная) `/api/v1/statistics/sessionCount/07-11-2022?unique=false`
* Вернет 422 `/api/v1/statistics/sessionCount/abc`

## Состав

* Запуск приложения из `main.py`
* Тесты `tests/test_main.http`
* Получение и запись информации в базу данных `sql_app/crud.py`
* Работа с базой данных `sql_app/database.py`
* Модели sqlalchemy `sql_app/models.py`
* Модели pydantic `sql_app/schemas.py`
* Главная страница `html/root.html`
* Первая страница `html/low_polly_floppa.html`
* Вторая страница `html/polish_cow.html`

## Тесты

API можно проверить через `test_main.http`, или через встроенные в FastAPI OpenAPI или swagger
