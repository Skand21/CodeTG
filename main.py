from gigachat import GigaChat
import telebot
from telebot import types

botTimeWeb = telebot.TeleBot('7463534277:AAHZ29LmrJIwzFTPmJ5h-s1UzmjJ3Brzoi4')
user_status = {}

# Список вопросов и ответов
correctotveti = 0
questions = [
    {"text": "Что такое переменная в C++?", "correct": "true", "answers": [
        {"text": "Переменная - это место в памяти, где хранится значение", "callback_data": "true"},
        {"text": "Переменная - это название программы", "callback_data": "false"},
        {"text": "Переменная используется только для ввода данных", "callback_data": "false"},
        {"text": "Переменная - это то же самое, что и функция", "callback_data": "false"},
    ]},
    {"text": "Какой тип данных используется для хранения целых чисел в C++?", "correct": "true", "answers": [
        {"text": "int", "callback_data": "true"},
        {"text": "char", "callback_data": "false"},
        {"text": "float", "callback_data": "false"},
        {"text": "bool", "callback_data": "false"},
    ]},
    {"text": "Что означает оператор '==' в C++?", "correct": "true", "answers": [
        {"text": "Присвоение значения", "callback_data": "false"},
        {"text": "Сравнение на равенство", "callback_data": "true"},
        {"text": "Логическое И", "callback_data": "false"},
        {"text": "Увеличение значения", "callback_data": "false"},
    ]},
    {"text": "Какой из следующих циклов используется для выполнения кода определённое количество раз?", "correct": "true", "answers": [
        {"text": "for", "callback_data": "true"},
        {"text": "while", "callback_data": "false"},
        {"text": "if", "callback_data": "false"},
        {"text": "switch", "callback_data": "false"},
    ]},
    {"text": "Какой символ используется для завершения строки кода в C++?", "correct": "true", "answers": [
        {"text": ":", "callback_data": "false"},
        {"text": ";", "callback_data": "true"},
        {"text": ".", "callback_data": "false"},
        {"text": ",", "callback_data": "false"},
    ]},
    {"text": "Как создать функцию в C++?", "correct": "true", "answers": [
        {"text": "void функция()", "callback_data": "true"},
        {"text": "function функция()", "callback_data": "false"},
        {"text": "create функция()", "callback_data": "false"},
        {"text": "func функция()", "callback_data": "false"},
    ]},
    {"text": "Какой оператор используется для вывода текста на экран?", "correct": "true", "answers": [
        {"text": "cout", "callback_data": "true"},
        {"text": "cin", "callback_data": "false"},
        {"text": "printf", "callback_data": "false"},
        {"text": "write", "callback_data": "false"},
    ]},
    {"text": "Какой тип данных может хранить только два значения: true или false?", "correct": "true", "answers": [
        {"text": "bool", "callback_data": "true"},
        {"text": "int", "callback_data": "false"},
        {"text": "string", "callback_data": "false"},
        {"text": "double", "callback_data": "false"},
    ]},
    {"text": "Какой оператор используется для увеличения значения переменной на 1?", "correct": "true", "answers": [
        {"text": "++", "callback_data": "true"},
        {"text": "--", "callback_data": "false"},
        {"text": "+=", "callback_data": "false"},
        {"text": "*=", "callback_data": "false"},
    ]},
    {"text": "Что делает функция main() в C++?", "correct": "true", "answers": [
        {"text": "Запускает выполнение программы", "callback_data": "true"},
        {"text": "Завершает выполнение программы", "callback_data": "false"},
        {"text": "Выводит текст на экран", "callback_data": "false"},
        {"text": "Создает переменную", "callback_data": "false"},
    ]}
]
# Переменная для отслеживания текущего вопроса
current_question_index = {}

# Обработка команды /start
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    first_mess = f"Привет, <b>{message.from_user.first_name}</b>!\nЯ бот, который помогает с изучением языка С++ и отслеживает твой прогресс. Выберите, с чего хотите начать."
    markup = types.InlineKeyboardMarkup()
    button_hochutest = types.InlineKeyboardButton(text='Узнать свой уровень', callback_data='test')
    button_nehochutest = types.InlineKeyboardButton(text='Обучиться с нуля', callback_data='nol')

    markup.add(button_hochutest)
    markup.add(button_nehochutest)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

# Обработка нажатия на кнопки "Узнать уровень" и "Обучиться с нуля"
@botTimeWeb.callback_query_handler(func=lambda call: True)
def handle_query(call):
    user_id = call.from_user.id
    if call.data == 'test':
        current_question_index[user_id] = 0  # Начинаем с первого вопроса
        user_status[user_id] = 'testing'  # Устанавливаем статус тестирования
        ask_question(call.message.chat.id, user_id)
    elif call.data == 'nol':
        botTimeWeb.send_message(call.message.chat.id, "Отлично, начинаем с нуля!")
        user_status[user_id] = 'learning'  # Устанавливаем статус обучения
    elif call.data in ['true', 'false']:
        check_answer(call)


# Функция для задания вопроса
def ask_question(chat_id, user_id):
    index = current_question_index.get(user_id, 0)
    if index < len(questions):
        question = questions[index]
        text = question["text"]
        markup = types.InlineKeyboardMarkup()

        # Добавляем ответы как кнопки
        for answer in question["answers"]:
            markup.add(types.InlineKeyboardButton(text=answer["text"], callback_data=answer["callback_data"]))

        botTimeWeb.send_message(chat_id, text, parse_mode='html', reply_markup=markup)

    else:
        botTimeWeb.send_message(chat_id, f"Тест завершен! Ваш результат: {correctotveti} / 10")
        botTimeWeb.send_message(chat_id, define_level(correctotveti))
        user_status[user_id] = 'ready'  # Устанавливаем статус готовности



# Функция для проверки ответа
def check_answer(call):
    global correctotveti
    user_id = call.from_user.id
    index = current_question_index.get(user_id, 0)

    # Проверка, что индекс находится в пределах списка вопросов
    if index >= len(questions):
        botTimeWeb.send_message(call.message.chat.id, "Тест завершен!")
        botTimeWeb.send_message(call.message.chat.id, define_level(correctotveti))
        return

    # Убираем клавиатуру после выбора ответа
    botTimeWeb.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    correct_answer = questions[index]["correct"]

    if call.data == correct_answer:
        botTimeWeb.send_message(call.message.chat.id, "Правильный ответ!")
        correctotveti += 1
    else:
        botTimeWeb.send_message(call.message.chat.id, "Неправильный ответ.")

    # Переход к следующему вопросу
    current_question_index[user_id] += 1
    ask_question(call.message.chat.id, user_id)

def define_level(correctotveti):
    if correctotveti == 1 or correctotveti == 2 or correctotveti == 3:
        return('Вы новичок')
    elif correctotveti == 4 or correctotveti == 5 or correctotveti == 6:
        return('Вы знаете что - то, но вы далеко не Виталик Бутерин')
    elif correctotveti == 7 or correctotveti == 8:
        return('Вы много знаете, но есть ещё над чем работать')
    elif correctotveti == 9 or correctotveti == 10:
        return('Вы всё знаете! Для изучения нового ИИ выдаст вам самые сложные задачи ')



@botTimeWeb.message_handler(content_types=['text'])
def start_Giga(message):
    user_id = message.from_user.id
    if user_status.get(user_id) == 'ready':  # Проверяем, завершил ли пользователь тест
        print("Включили тест с запросом:", message.text)
        user_message = message.text  # Текст от пользователя
        botTimeWeb.send_message(message.chat.id, "Ваш запрос отправляется на обработку...")

        # Вызов GigaChat для получения ответа
        try:
            with GigaChat(
                    credentials="YTdlZWNhNmEtNmIyMC00ZmYwLThjNWYtMWIzZmUyZDNiOTAyOmQyMDQxNTRjLTNlOGYtNGFmNy1iOTFmLTU0NGE1OGFjMjg1Yg==",
                    verify_ssl_certs=False) as giga:
                response = giga.chat(user_message)
                bot_reply = response.choices[0].message.content  # Ответ от GigaChat
                botTimeWeb.send_message(message.chat.id, bot_reply, parse_mode='Markdown')  # Отправка ответа пользователю
        except Exception as e:
            botTimeWeb.send_message(message.chat.id, f"Произошла ошибка вида: {e}. Попробуйте позже!")
            print(f"Произошла ошибка: {e}.")
    else:
        botTimeWeb.send_message(message.chat.id, "Я пока не понимаю этой команды. Завершите тестирование, чтобы продолжить!")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и ожидает сообщения...")
    try:
        botTimeWeb.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")