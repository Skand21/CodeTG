import telebot

botTimeWeb = telebot.TeleBot('7463534277:AAHZ29LmrJIwzFTPmJ5h-s1UzmjJ3Brzoi4')

from telebot import types

# Обработка команды /start
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"Привет, <b>{message.from_user.first_name}</b>!\nЯ бот, который помогает с изучением языка С++ и отслеживает твой прогресс. Выберите с чего хотите начать"
    markup = types.InlineKeyboardMarkup()
    button_hochutest = types.InlineKeyboardButton(text='Узнать свой уровень', callback_data='test')
    button_nehochutest = types.InlineKeyboardButton(text='Обучиться с нуля', callback_data='nol')

    markup.add(button_hochutest)
    markup.add(button_nehochutest)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

#1

# Обработка нажатия на кнопки "Учитель" и "Ученик"
@botTimeWeb.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'test':
        # Если выбрано "Учитель", просим ввести код
        botTimeWeb.send_message(call.message.chat.id, ".")
        botTimeWeb.register_next_step_handler(call.message, get_teacher_code)
        for question in range(1,11):
            text = f"Вопрос {question}"
            markup = types.InlineKeyboardMarkup()
            button_hochutest = types.InlineKeyboardButton(text='Узнать свой уровень', callback_data='test')
            button_nehochutest = types.InlineKeyboardButton(text='Обучиться с нуля', callback_data='nol')

            markup.add(button_hochutest)
            markup.add(button_nehochutest)
            botTimeWeb.send_message(call.message.chat.id, text, parse_mode='html', reply_markup=markup)
    elif call.data == 'nol':
        # Если выбран "Ученик", просим ввести класс
        botTimeWeb.send_message(call.message.chat.id, "")
        botTimeWeb.register_next_step_handler(call.message, get_student_class)

# Обработка ввода кода учителя
def get_teacher_code(message):
    teacher_code = message.text
    # Здесь вы можете добавить логику для проверки кода учителя
    if teacher_code == "1234":  # Пример кода
        botTimeWeb.send_message(message.chat.id, "Код подтвержден! Добро пожаловать, учитель.")
    else:
        botTimeWeb.send_message(message.chat.id, "Неверный код. Попробуйте еще раз.")
        botTimeWeb.register_next_step_handler(message, get_teacher_code)

# Обработка ввода класса ученика
def get_student_class(message):
    student_class = message.text
    botTimeWeb.send_message(message.chat.id, f"Отлично! Ты в {student_class} классе. Добро пожаловать!")

# Запуск бота
botTimeWeb.polling(none_stop=True)