import telebot
from config import *
from logic import *
import os

bot = telebot.TeleBot(TOKEN)

# Тут будем хранить выбранный цвет для каждого пользователя
user_colors = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который может показывать города на карте. Напиши /help для списка команд.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id, "Доступные команды:\n"
                                    "/show_city [город]\n"
                                    "/remember_city [город]\n"
                                    "/show_my_cities\n"
                                    "/set_color [цвет]\n"
                                    "/distance [город1] [город2]")


@bot.message_handler(commands=['set_color'])
def handle_set_color(message):
    user_id = message.chat.id
    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(user_id, "Используй так: /set_color red (или другой цвет)")
        return
    color = parts[1]
    user_colors[user_id] = color
    bot.send_message(user_id, f"Цвет маркеров изменён на {color}!")

@bot.message_handler(commands=['show_city'])
def handle_show_city(message):
    city_name = message.text.split()[-1]
    user_id = message.chat.id
    color = user_colors.get(user_id, 'red')  # По умолчанию red
    try:
        manager.create_grapf(f'{user_id}.png', [city_name], marker_color=color)
        if os.path.exists(f'{user_id}.png'):
            with open(f'{user_id}.png', 'rb') as map:
                bot.send_photo(user_id, map)
        else:
            bot.send_message(message.chat.id, "Не удалось создать карту для города.")
    except Exception as e:
        bot.send_message(message.chat.id, f"Ошибка при создании карты: {e}")

@bot.message_handler(commands=['remember_city'])
def handle_remember_city(message):
    user_id = message.chat.id
    city_name = message.text.split()[-1]
    if manager.add_city(user_id, city_name):
        bot.send_message(message.chat.id, f'Город {city_name} успешно сохранен!')
    else:
        bot.send_message(message.chat.id, 'Такого города я не знаю. Убедись, что он написан на английском!')

@bot.message_handler(commands=['show_my_cities'])
def handle_show_visited_cities(message):
    user_id = message.chat.id
    cities = manager.select_cities(user_id)
    color = user_colors.get(user_id, 'red')
    if cities:
        try:
            manager.create_grapf(f'{user_id}_cities.png', cities, marker_color=color)
            if os.path.exists(f'{user_id}_cities.png'):
                with open(f'{user_id}_cities.png', 'rb') as map:
                    bot.send_photo(user_id, map)
            else:
                bot.send_message(user_id, "Не удалось создать карту для ваших городов.")
        except Exception as e:
            bot.send_message(user_id, f"Ошибка при создании карты: {e}")
    else:
        bot.send_message(user_id, "У вас пока нет сохраненных городов.")

@bot.message_handler(commands=['distance'])
def handle_distance(message):
    user_id = message.chat.id
    parts = message.text.split()
    if len(parts) != 3:
        bot.send_message(user_id, "Используй так: /distance city1 city2")
        return

    city1 = parts[1]
    city2 = parts[2]
    color = user_colors.get(user_id, 'red')

    try:
        path = f'{user_id}_distance.png'
        result = manager.draw_distance(path, city1, city2, marker_color=color, line_color='blue')
        if result and os.path.exists(path):
            with open(path, 'rb') as map:
                bot.send_photo(user_id, map)
        else:
            bot.send_message(user_id, "Не удалось построить маршрут. Проверь названия городов!")
    except Exception as e:
        bot.send_message(user_id, f"Ошибка при создании карты маршрута: {e}")


if __name__ == "__main__":
    manager = DB_Map(DATABASE)
    bot.polling()


