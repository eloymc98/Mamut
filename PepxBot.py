#!/usr/bin/env
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
"""
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
import os

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('PepxBot')

'''
Token ID of the bot
'''
TOKEN_PEPXBOT = '870743532:AAGXJayURrkNWU0FkePr7GK5k6FPkY156Z4'

'''
Configuration of states, default values, etc.
'''
INTRO, PHOTO, INFO = range(3)

dumpster_keyboard = [['Yellow', 'Blue'],
                     ['Green', 'Grey'],
                     ['Brown', 'Special']
                     ['Photo']]
dumpsters = ReplyKeyboardMarkup(dumpster_keyboard, one_time_keyboard=True)

function_keyboard = [['Where do I dump it?', 'What should I throw in each dumpster?']]
function_chooser = ReplyKeyboardMarkup(function_keyboard)

'''
Utility functions
'''


def easter_egg(update, context):
    emojis_cringe = '\U0001F630'[:-4]
    return


# Resolve message data to a readable name
def get_name(user):
    try:
        name = user.first_name
    except (NameError, AttributeError):
        try:
            name = user.username
        except (NameError, AttributeError):
            logger.info("No username or first name.. wtf")
            return ""

    return name


'''
Bot states' handlers
'''


def option_menu(update, context):
    update.message.reply_text("How can I help you?", reply_markup=function_chooser)

    return INTRO


def start(update, context):
    logger.info('User has connected to PepxBot: /start')
    user_id = update.message.from_user.id
    name = get_name(update.message.from_user)
    context.bot.send_message(chat_id=update.message.chat_id, text=("Welcome " + name + " ! My name is Pepx"))
    logger.info('Name of user is: ' + name + " and its ID is " + str(user_id))

    return option_menu(update, context)


def photo_query(update, context):
    update.message.reply_text('Ok! Send me a picture of the waste, please.')

    return PHOTO


def dumpster_select(update, context):
    update.message.reply_text('Ok! Which dumpster would you like to know about?', reply_markup=dumpster_keyboard)

    return INFO


def process_photo(update, context):
    path = r'C:\Users\Mephistopheles\Pictures'
    filename = update.message.photo[-1].file_id
    context.bot.getFile(filename).download(os.path.join(path, filename + '.jpg'))
    update.message.reply_text()

    return option_menu(update, context)


# Dumpers info
def yellow_info(update, context):
    update.message.reply_text("y")

    return INFO


def blue_info(update, context):
    update.message.reply_text("b")

    return INFO


def green_info(update, context):
    update.message.reply_text("gree")

    return INFO


def grey_info(update, context):
    update.message.reply_text("g")

    return INFO


def brown_info(update, context):
    update.message.reply_text("")

    return INFO


def special_info(update, context):
    update.message.reply_text("s")

    return INFO


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    updater = Updater(token=TOKEN_PEPXBOT, use_context=True, workers=50)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler('start', start)],

        states={
            INTRO: [MessageHandler(Filters.regex('^Where do I dump it?'), photo_query),
                    MessageHandler(Filters.regex('^What should I throw in each dumpster?'), dumpster_select)],
            PHOTO: [MessageHandler(Filters.photo, process_photo),
                    MessageHandler(Filters.all, photo_query)],
            INFO: [MessageHandler(Filters.regex('[Y|y]ellow'), yellow_info),
                   MessageHandler(Filters.regex('[B|b]lue'), blue_info),
                   MessageHandler(Filters.regex('[G|g]reen'), green_info),
                   MessageHandler(Filters.regex('[G|g]rey'), grey_info),
                   MessageHandler(Filters.regex('[B|b]rown'), brown_info),
                   MessageHandler(Filters.regex('[S|s]pecial'), special_info),
                   MessageHandler(Filters.regex('Photo'), photo_query)]

        },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]

    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
