import time
import os
import telebot
from django.core.mail import send_mail

from celery import shared_task
from django.conf import settings

bot = telebot.TeleBot(os.environ.get("TOKEN"), parse_mode=None)


@shared_task
def send_message(message):
    bot.send_message(int(os.environ.get("CHAT_ID")), message)
    time.sleep(5)
    send_mail('Создание блога',
              message,
              settings.EMAIL_HOST_USER,
              ['chopona09@gmail.com', ],
              fail_silently=False,
              )
