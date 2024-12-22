from gigachat import GigaChat
import telebot
from telebot import types
import requests
import re

botTimeWeb = telebot.TeleBot('7463534277:AAHZ29LmrJIwzFTPmJ5h-s1UzmjJ3Brzoi4')
user_status = {}
user_scores = {}  # Новый словарь для хранения баллов каждого пользователя

# Промпт (будет загружен из Google Docs)
prompt_text = ""

# Ссылка на Google Docs документ с промптом
google_docs_url = "https://docs.google.com/document/d/1itjBPTT3Dhw1ANRsw_Q8OtiyFl2hSK7RqX9Ogp4NCUQ/edit?usp=sharing"
result_test = 'у пользователя нулевой уровень и знание языка'
first_giga = 0
# Функция для загрузки промпта из Google Docs
def load_prompt(url):
    # Извлекаем ID документа из URL
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)

    # Загружаем документ как обычный текст
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()  # Проверяем, что запрос успешен
    text = response.text
    return text


# Загружаем промпт при старте бота (но не выводим его сразу пользователю)
prompt_text = load_prompt(google_docs_url)

# Список вопросов и ответов
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
    global result_test
    user_id = call.from_user.id
    if call.data == 'test':
        current_question_index[user_id] = 0  # Начинаем с первого вопроса
        user_status[user_id] = 'testing'  # Устанавливаем статус тестирования
        user_scores[user_id] = 0  # Сброс баллов для нового теста
        ask_question(call.message.chat.id, user_id)
    elif call.data == 'nol':
        botTimeWeb.send_message(call.message.chat.id, "Отлично, начинаем с нуля!")
        user_status[user_id] = 'ready'  # Устанавливаем статус обучения
    elif call.data == 'marat':
        start_Giga(result_test) #приди пжлст
        user_status[user_id] = 'ready'
    elif call.data in ['true', 'false']:
        check_answer(call)

# Функция для задания вопроса
def ask_question(chat_id, user_id):
    index = current_question_index.get(user_id, 0)
    global result_test
    if index < len(questions):
        question = questions[index]
        text = question["text"]
        markup = types.InlineKeyboardMarkup()

        # Добавляем ответы как кнопки
        for answer in question["answers"]:
            markup.add(types.InlineKeyboardButton(text=answer["text"], callback_data=answer["callback_data"]))

        botTimeWeb.send_message(chat_id, text, parse_mode='html', reply_markup=markup)

    else:
        result = user_scores[user_id]
        botTimeWeb.send_message(chat_id, f"Тест завершен! Ваш результат: {result} / {len(questions)}")
        result_test = define_level(result)
        botTimeWeb.send_message(chat_id, result_test)

        neperv_mess = "КРАСАВА МАРАТ, ты прошёл тест, нажимай кнопку и начинай обучение"
        markup = types.InlineKeyboardMarkup()
        button_obuchenijemarata = types.InlineKeyboardButton(text='НАЧАТЬ ОБУЧЕНИЕ', callback_data='marat')
        markup.add(button_obuchenijemarata)

        botTimeWeb.send_message(chat_id, neperv_mess, parse_mode='html', reply_markup=markup)

# Функция для проверки ответа
def check_answer(call):
    user_id = call.from_user.id
    index = current_question_index.get(user_id, 0)

    # Проверка, что индекс находится в пределах списка вопросов
    if index >= len(questions):
        botTimeWeb.send_message(call.message.chat.id, "Тест завершен!")
        botTimeWeb.send_message(call.message.chat.id, define_level(user_scores[user_id]))
        return

    # Убираем клавиатуру после выбора ответа
    botTimeWeb.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    correct_answer = questions[index]["correct"]

    if call.data == correct_answer:
        botTimeWeb.send_message(call.message.chat.id, "Правильный ответ!")
        user_scores[user_id] += 1  # Увеличиваем баллы для конкретного пользователя
    else:
        botTimeWeb.send_message(call.message.chat.id, "Неправильный ответ.")

    # Переход к следующему вопросу
    current_question_index[user_id] += 1
    ask_question(call.message.chat.id, user_id)

def define_level(correctotveti):
    if correctotveti == 1 or correctotveti == 2 or correctotveti == 3:
        return('Вы новичок')
    elif correctotveti == 4 or correctotveti == 5 or correctotveti == 6:
        return('Вы знаете что-то, но вы далеко не Виталик Бутерин')
    elif correctotveti == 7 or correctotveti == 8:
        return('Вы много знаете, но есть ещё над чем работать')
    elif correctotveti == 9 or correctotveti == 10:
        return('Вы всё знаете! Для изучения нового ИИ выдаст вам самые сложные задачи')


@botTimeWeb.message_handler(content_types=['text'])
def start_Giga(message):
    global first_giga
    user_id = message.from_user.id

    if first_giga == 0:
        first_giga = 1
        try:
            with GigaChat(
                    credentials="YTdlZWNhNmEtNmIyMC00ZmYwLThjNWYtMWIzZmUyZDNiOTAyOmQyMDQxNTRjLTNlOGYtNGFmNy1iOTFmLTU0NGE1OGFjMjg1Yg==",
                    verify_ssl_certs=False) as giga:
                response = giga.chat(prompt_text)
                print(prompt_text)
        except Exception as e:
            botTimeWeb.send_message(message.chat.id, f"Произошла ошибка вида: {e}. Попробуйте позже!")
            print(f"Произошла ошибка: {e}.")

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
                botTimeWeb.send_message(message.chat.id, bot_reply,
                                        parse_mode='Markdown')  # Отправка ответа пользователю
        except Exception as e:
            botTimeWeb.send_message(message.chat.id, f"Произошла ошибка вида: {e}. Попробуйте позже!")
            print(f"Произошла ошибка: {e}.")
    else:
        botTimeWeb.send_message(message.chat.id,
                                "Я пока не понимаю этой команды. Завершите тестирование, чтобы продолжить!")


def print_Giga(message):
    user_message = message  # Текст от пользователя
    # Вызов GigaChat для получения ответа
    with GigaChat(
            credentials="YTdlZWNhNmEtNmIyMC00ZmYwLThjNWYtMWIzZmUyZDNiOTAyOmQyMDQxNTRjLTNlOGYtNGFmNy1iOTFmLTU0NGE1OGFjMjg1Yg==",
            verify_ssl_certs=False) as giga:
        response = giga.chat(user_message)
        bot_reply = response.choices[0].message.content  # Ответ от GigaChat
        print(bot_reply)
# Запуск бота
if __name__ == "__main__":
    print_Giga('привет, какого цвета солнце?)')
    print("Бот запущен и ожидает сообщения...")
    try:
        botTimeWeb.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")
