from gigachat import GigaChat
import telebot
from telebot import types
import requests
import re

# Инициализация бота
botTimeWeb = telebot.TeleBot('7463534277:AAHZ29LmrJIwzFTPmJ5h-s1UzmjJ3Brzoi4')

# Словари для хранения состояния пользователей
user_status = {}  # Статус пользователя (тестирование, обучение и т.д.)
user_scores = {}  # Баллы пользователей за тест
current_question_index = {}  # Текущий вопрос в тесте

# Промпт и ссылка на Google Docs
google_docs_url = "https://docs.google.com/document/d/1itjBPTT3Dhw1ANRsw_Q8OtiyFl2hSK7RqX9Ogp4NCUQ/edit?usp=sharing"
prompt_text = ""  # Текст промпта будет загружен из Google Docs

# Функция для загрузки промпта из Google Docs
def load_prompt(url):
    """Загружает текст промпта из Google Docs."""
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)

    try:
        response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке документа: {e}")
        return ""

# Загружаем промпт при старте
prompt_text = load_prompt(google_docs_url)

# Список вопросов и ответов для теста
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

# Обработка команды /start
@botTimeWeb.message_handler(commands=['start'])
def startBot(message):
    """Обработка команды /start."""
    first_mess = f"Привет, <b>{message.from_user.first_name}</b>!\nЯ бот, который помогает с изучением языка С++ и отслеживает твой прогресс. Выберите, с чего хотите начать."
    markup = types.InlineKeyboardMarkup()
    button_hochutest = types.InlineKeyboardButton(text='Узнать свой уровень', callback_data='test')
    button_nehochutest = types.InlineKeyboardButton(text='Обучиться с нуля', callback_data='nol')
    button_help = types.InlineKeyboardButton(text='Инструкция', callback_data='help')

    markup.add(button_hochutest, button_nehochutest, button_help)
    botTimeWeb.send_message(message.chat.id, first_mess, parse_mode='html', reply_markup=markup)

# Обработка команды /help
@botTimeWeb.message_handler(commands=['help'])
def help_command(message):
    """Обработка команды /help."""
    show_help(message.chat.id)

def show_help(chat_id):
    """Отправляет инструкцию по использованию бота."""
    instruction = """
    📚 Методичка-инструкция по использованию бота:

    1. Запуск бота и начало работы:
       - Напишите команду /start.
       - Выберите одну из кнопок:
         - "Узнать свой уровень" — пройти тест.
         - "Обучиться с нуля" — начать обучение.

    2. Прохождение теста:
       - Бот задаст вам 10 вопросов по C++.
       - Выбирайте правильные ответы, нажимая на кнопки.
       - В конце теста бот покажет ваш результат и уровень знаний.

    3. Начало обучения:
       - После теста или выбора "Обучиться с нуля" бот готов отвечать на ваши вопросы.
       - Задавайте вопросы, например: "Что такое указатели?" или "Как работают циклы?".

    4. Использование функционала бота:
       - Бот объясняет темы, помогает с заданиями и отвечает на вопросы.
       - Вы можете уточнять: "Объясни подробнее" или "Ответь кратко".

    5. Повторение и закрепление знаний:
       - Попросите бота повторить тему: "Напомни про функции".
       - Пройдите тест снова, чтобы проверить прогресс.

    🚀 Советы:
    - Если бот не понимает ваш запрос, переформулируйте его.
    - Используйте команду /test, чтобы снова пройти тест.
    """
    markup = types.InlineKeyboardMarkup()
    button_start = types.InlineKeyboardButton(text='Начать', callback_data='start')
    button_test = types.InlineKeyboardButton(text='Пройти тест', callback_data='test')
    button_learn = types.InlineKeyboardButton(text='Обучиться с нуля', callback_data='nol')
    markup.add(button_start, button_test, button_learn)
    botTimeWeb.send_message(chat_id, instruction, parse_mode='Markdown', reply_markup=markup)

# Обработка нажатия на кнопки
@botTimeWeb.callback_query_handler(func=lambda call: True)
def handle_query(call):
    """Обработка нажатий на кнопки."""
    user_id = call.from_user.id
    if call.data == 'test':
        current_question_index[user_id] = 0  # Начинаем с первого вопроса
        user_status[user_id] = 'testing'  # Устанавливаем статус тестирования
        user_scores[user_id] = 0  # Сброс баллов для нового теста
        ask_question(call.message.chat.id, user_id)
    elif call.data == 'nol':
        user_status[user_id] = 'ready'  # Устанавливаем статус обучения
        botTimeWeb.send_message(call.message.chat.id, "Отлично, начинаем с нуля! Что конкретно тебя интересует?")
    elif call.data == 'marat':
        user_status[user_id] = 'ready'
    elif call.data == 'help':
        show_help(call.message.chat.id)
    elif call.data == 'start':
        startBot(call.message)
    elif call.data in ['true', 'false']:
        check_answer(call)

def ask_question(chat_id, user_id):
    """Задаёт пользователю следующий вопрос."""
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
        # Тест завершён
        result = user_scores[user_id]
        result_test = define_level(result)
        botTimeWeb.send_message(chat_id, f"Тест завершен! Ваш результат: {result} / {len(questions)}")
        botTimeWeb.send_message(chat_id, result_test)

        # Предложение начать обучение
        markup = types.InlineKeyboardMarkup()
        button_obuchenijemarata = types.InlineKeyboardButton(text='НАЧАТЬ ОБУЧЕНИЕ', callback_data='marat')
        markup.add(button_obuchenijemarata)
        botTimeWeb.send_message(chat_id, "КРАСАВА МАРАТ, ты прошёл тест, нажимай кнопку и начинай обучение", parse_mode='html', reply_markup=markup)

def check_answer(call):
    """Проверяет ответ пользователя и переходит к следующему вопросу."""
    user_id = call.from_user.id
    index = current_question_index.get(user_id, 0)

    if index >= len(questions):
        botTimeWeb.send_message(call.message.chat.id, "Тест завершен!")
        botTimeWeb.send_message(call.message.chat.id, define_level(user_scores[user_id]))
        return

    # Убираем клавиатуру после выбора ответа
    botTimeWeb.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    correct_answer = questions[index]["correct"]
    if call.data == correct_answer:
        botTimeWeb.send_message(call.message.chat.id, "Правильный ответ!")
        user_scores[user_id] += 1
    else:
        botTimeWeb.send_message(call.message.chat.id, "Неправильный ответ.")

    # Переход к следующему вопросу
    current_question_index[user_id] += 1
    ask_question(call.message.chat.id, user_id)

def define_level(correctotveti):
    """Определяет уровень пользователя на основе количества правильных ответов."""
    if correctotveti <= 3:
        return "Вы новичок"
    elif 4 <= correctotveti <= 6:
        return "Вы знаете что-то, но вы далеко не Виталик Бутерин"
    elif 7 <= correctotveti <= 8:
        return "Вы много знаете, но есть ещё над чем работать"
    elif correctotveti >= 9:
        return "Вы всё знаете! Для изучения нового ИИ выдаст вам самые сложные задачи"

# Обработка текстовых сообщений
@botTimeWeb.message_handler(content_types=['text'])
def handle_text(message):
    """Обработка текстовых сообщений."""
    user_id = message.from_user.id
    if user_status.get(user_id) == 'ready':  # Проверяем, завершил ли пользователь тест
        user_message = f"ОТВЕЧАЙ ТОЛЬКО ЗА 4 АБЗАЦА. {message.text}"
        botTimeWeb.send_message(message.chat.id, "Ваш запрос отправляется на обработку...")

        try:
            with GigaChat(credentials="YTdlZWNhNmEtNmIyMC00ZmYwLThjNWYtMWIzZmUyZDNiOTAyOmQyMDQxNTRjLTNlOGYtNGFmNy1iOTFmLTU0NGE1OGFjMjg1Yg==", verify_ssl_certs=False) as giga:
                response = giga.chat(user_message)
                bot_reply = response.choices[0].message.content
                bot_reply = bot_reply.replace('###', '')
                botTimeWeb.send_message(message.chat.id, bot_reply, parse_mode='Markdown')
        except Exception as e:
            botTimeWeb.send_message(message.chat.id, f"Произошла ошибка: {e}. Попробуйте позже!")
    else:
        botTimeWeb.send_message(message.chat.id, "Завершите тестирование, чтобы продолжить!")

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен и ожидает сообщения...")
    try:
        botTimeWeb.polling(none_stop=True, interval=0)
    except KeyboardInterrupt:
        print("Бот остановлен вручную.")