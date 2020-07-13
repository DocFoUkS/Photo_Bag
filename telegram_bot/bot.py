import logging
import telebot
import time
import threading

import settings

logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s' +
    ' - %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')


class TelegramBot():
    def __init__(self):
        self.bot = telebot.TeleBot(settings.API_KEY)
        threading.Thread(target=self.bot_polling_start).start()

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
