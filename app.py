# -*- coding: utf-8 -*-

import os
import logging
import traceback
from configparser import ConfigParser

from flask import Flask, request
import telegram
from telegram.ext import Updater, ChosenInlineResultHandler
from telegram.ext import CommandHandler, CallbackQueryHandler, InlineQueryHandler

import cmd

app = Flask(__name__)
botName = "@wiztest_bot"

# configuration
config = ConfigParser()
config.read_file(open('config.ini'))

TOKEN = config['DEFAULT']['token']
HOST = config['DEFAULT']['webhook_host']

# enable logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log to file
# logging.basicConfig(level=logging.DEBUG
#     filename=os.path.join(os.path.dirname(__file__), 'logs/app.log'),
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# global bot
bot = telegram.Bot(token=TOKEN)

updater = Updater(TOKEN)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", cmd.start))
dp.add_handler(CommandHandler("help", cmd.help))
dp.add_handler(CommandHandler("xxoo", cmd.xxoo))
dp.add_handler(CallbackQueryHandler(cmd.callback_query))
dp.add_handler(InlineQueryHandler(cmd.inline_query))
dp.add_handler(ChosenInlineResultHandler(cmd.collect_feedback))
dp.add_error_handler(cmd.error)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        logging.info("hello, telegram")
        return "hello"

@app.route("/set_webhook", methods=['GET'])
def set_webhook():
    s = bot.setWebhook("{}/hook/".format(HOST) + TOKEN)
    if s:
        logging.info("{} webhook setup ok".format(botName))
        return "{} webhook setup ok".format(botName)
    else:
        logging.error("{} webhook setup failed".format(botName))
        return "{} webhook setup failed".format(botName)

@app.route('/remove_webhook', methods=['GET'])
def remove_webhook():
    s = bot.setWebhook('')
    if s:
        logging.info("{} webhook removed ok".format(botName))
        return "{} webhook removed ok".format(botName)
    else:
        logging.error("{} webhook removed failed".format(botName))
        return "{} webhook removed failed".format(botName)

@app.route("/hook/" + TOKEN, methods=["POST"])
def webhook():
    if request.method == "POST":
        try:
            update = telegram.Update.de_json(request.get_json(force=True), bot)
            # logging.info("calling {}".format(update.message))
            dp.process_update(update)
        except Exception:
            bot.sendMessage(update.message.chat_id, text="command execute error")
            logging.error("calling error {}\n".format(update.message) + traceback.format_exc())
            return traceback.format_exc()
        return "ok"

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9012)
