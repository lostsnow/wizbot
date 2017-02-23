# -*- coding: utf-8 -*-

import requests
import os
import logging
from datetime import datetime
from telegram import InlineQueryResultLocation, InlineQueryResultArticle, InputTextMessageContent, ParseMode

logger = logging.getLogger(__name__)

# Define handlers.
def help(bot, update):
    text = '_help_'
    bot.sendMessage(update.message.chat_id, text=text,
        parse_mode=ParseMode.MARKDOWN)

def start(bot, update):
    text = '*start*'
    bot.sendMessage(update.message.chat_id, text=text,
        parse_mode=ParseMode.MARKDOWN)

def inline_query(bot, update):
    query = update.inline_query.query.strip()

    if not query:
        bot.answerInlineQuery(update.inline_query.id, results=[InlineQueryResultArticle(id=0,
            title="keyword required",
            input_message_content=InputTextMessageContent("keyword required!"))])
        return

    # query for data

    data = [
        {
            "identifier": 1,
            "latitude": 22.301015,
            "longitude": 114.171766,
            "title": "老夫子",
            "input_message_content": InputTextMessageContent('''# *Address*\n151-157 Nathan Road, Tsim Sha Tsui, Hong Kong
# *latlng*\n22.301015, 114.171766''',
                parse_mode=ParseMode.MARKDOWN)
        },
        {
            "identifier": 2,
            "latitude": 39.902933,
            "longitude": 116.504286,
            "title": "黑狮子",
            "input_message_content": InputTextMessageContent('''# *Address*\nShimen East Road, Chaoyang, Beijing, China, 100124
# *latlng*\n39.902933, 116.504286''',
                parse_mode=ParseMode.MARKDOWN)
        }
    ]

    results = [InlineQueryResultLocation(id=item['identifier'],
        latitude=item['latitude'],
        longitude=item['longitude'],
        input_message_content=item['input_message_content'],
        title=item['title'].rstrip('\\'))
        for item in data]
    bot.answerInlineQuery(update.inline_query.id, results=results)

def error(bot, update, error):
    logger.warn('update "%s" caused error "%s"' % (update, error))


def collect_feedback(bot, update):
    chosen_query = update.chosen_inline_result.query.strip()
    result_id = update.chosen_inline_result.result_id.strip()
    user_id = update.chosen_inline_result.from_user.id
    date_time = str(datetime.utcnow())
    fout = 'logs/feedback.log'
    with open(fout, 'a') as f:
        f.write(date_time + ',' + str(user_id) + ',' + result_id +
            ',' + chosen_query + '\n')
