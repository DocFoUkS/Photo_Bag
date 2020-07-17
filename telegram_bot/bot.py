import logging
import telebot
import time
import threading

from telegram_bot import config as c

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s' +
    ' - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


class Telegram_BOT():
    def __init__(self):
        if c.BOT_START == 0:
            self.bot = telebot.TeleBot(c.API_KEY)
            threading.Thread(target=self.bot_polling_start).start()
            c.BOT_START = 1

    def bot_polling_start(self):
        while True:
            try:
                self.bot.polling(none_stop=False)
            except Exception as err:
                logging.info("TELEGRAMBOT ERROR: " + str(err))
                time.sleep(3)
                logging.info("TELEGRAMBOT RESTART")

    def send_message(self, message):
        logging.info("SENDING MESSAGE: " + str(message['text']))
        for send_try in range(3):
            try:
                self.bot.send_message(message['chat_id'], str(message['text']))
                logging.info("DONE")
                break

            except Exception as err:
                logging.info(
                    "TELEGRAM ERROR WHEN SENDING WELCOME ANSWER TO " +
                    str(message['chat_id']) + ": " + str(err))
                time.sleep(3)
