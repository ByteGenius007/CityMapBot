# CityMapBot


Это Telegram-бот, который показывает города на карте 🌍  
Ты можешь сохранять любимые города и потом смотреть их на карте!

## Что умеет бот

- Показать карту города `/show_city [город]`
- Запомнить город `/remember_city [город]`
- Показать все твои города на карте `/show_my_cities`

## Установка

1. Склонируй репозиторий:

```bash
git clone https://github.com/ByteGenius007/show_cities.git
cd CityMapBot
````

2. Установи зависимости:

```bash
pip install -r requirements.txt
```

3. Добавь файл `config.py` и запиши в него токен и имя базы данных:

```python
TOKEN = 'твой_токен_бота'
DATABASE = 'database.db'
```

4. Запусти бота:

```bash
python bot.py
```

## Структура проекта

```
CityMapBot/
├── bot.py          # Основной код бота
├── config.py       # Настройки (токен и БД)
├── logic.py        # Логика работы с картами и базой
├── requirements.txt # Список библиотек
```

## Зависимости

* `pyTelegramBotAPI`
* `matplotlib`
* `sqlite3`

## Как работает

Бот рисует карту, отмечает твои города и отправляет тебе фотку. Всё просто и понятно!

---


