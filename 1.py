#!pip install langchain-gigachat
#!pip install pytelegrambotapi

#@title Установка библиотек. Сервисные функции
# !pip -q install --upgrade tiktoken
# #!pip -q install langchain openai chromadb
# !pip -q install gspread oauth2client
# !pip install gigachain-cli
#
# # привет Минцифры
# !gigachain install-rus-certs

#GigaChat
from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

import requests
import pathlib
import subprocess
import tempfile
# import ipywidgets as widgets
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

import os
#import openai
import tiktoken
import re



giga = GigaChat(
    credentials="a7eeca6a-6b20-4ff0-8c5f-1b3fe2d3b902",
    scope="GIGACHAT_API_PERS",
    model="GigaChat",
    streaming=False,
    verify_ssl_certs=False,
)

#import
import telebot
import re
import requests
from telebot import types
bot = telebot.TeleBot('ваш токен бота от Telegram');


def load_prompt(url):
    # Extract the document ID from the URL
    match_ = re.search('/document/d/([a-zA-Z0-9-_]+)', url)
    if match_ is None:
        raise ValueError('Invalid Google Docs URL')
    doc_id = match_.group(1)


  # Download the document as plain text
    response = requests.get(f'https://docs.google.com/document/d/{doc_id}/export?format=txt')
    response.raise_for_status()
    text = response.text
    return f'{text}'

from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

def Answer(system, topic):

#"""Пример работы с чатом через gigachain"""
    # Авторизация в сервисе GigaChat
    chat = GigaChat(credentials="Токен Cбера==", verify_ssl_certs=False)

    messages = [
      SystemMessage(
        content=system
      )

        messages.append(HumanMessage(content=topic))
        res = chat(messages)
messages.append(res)
print("User: ", topic)
print("Bot: ", res.content)


return res.content
expert_promt = load_prompt('https://docs.google.com/document/d/1UcXvbMP2snwZ0385fqEmGv0vTzAC7Bs-1aIcsjrMcV8/edit?usp=sharing')

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Здравствуйте, Я Мария Абогада! Я могу давать юридические советы исходя из того как был сформулирован вопрос.
Рекомендую вам проверять полученные вопросы на очной консультации у адвоката, который сможет изучить ваши документы. \