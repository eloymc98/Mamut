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
INTRO, PHOTO, INFO, YELLOW, BLUE, GREEN, GREY, BROWN, SPECIAL = range(9)

dumpster_keyboard = [['Yellow', 'Blue'],
                      ['Green', 'Grey'],
                      ['Brown', 'Special']]
dumpsters = ReplyKeyboardMarkup(dumpster_keyboard, one_time_keyboard=True)

function_keyboard = [['Where do I dump it?', 'What should I throw in each dumpster?']]
function_chooser = ReplyKeyboardMarkup(function_keyboard)

'''
Utility functions
'''


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
    update.message.reply_text('Ok! Which dumpster would you like to know about?')

    return INFO

def process_photo(update, context):
    caca = update.message.from_user
    logger.info(caca)
    update.message.reply_text('\U0001F601')

    return option_menu(update, context)


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
            #INFO: [MessageHandler(Filters.regex('[Y|y]ellow'), yellow_info),
            #      MessageHandler(Filters.regex('[B|b]lue'), blue_info),
            #     MessageHandler(Filters.regex('[G|g]reen'), ),
            #       MessageHandler(Filters.regex('[G|g]rey'), ),
            #       MessageHandler(Filters.regex('[B|b]rown'), ),
            #       MessageHandler(Filters.regex('[S|s]pecial'), )]
            #                                      intr_medicine)],
            #           YELLOW: [MessageHandler(Filters.text, send_new_medicine)],
            #           BLUE: [MessageHandler(Filters.regex('^YES$'), choose_function),
            #                  MessageHandler(Filters.regex('^NO$'), intr_medicine)
            #                 ],
            #        GREEN: [MessageHandler(Filters.regex('^YES$'), choose_function),
            #               MessageHandler(Filters.regex('^NO$'), delete_reminder)
            #              ],
            #     GREY: [MessageHandler(Filters.text, get_medicine_CN)],
            #    BROWN: [MessageHandler(Filters.regex('^YES$'), choose_function)]
            #   SPECIAL: [MessageHandler()]'''
        },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]

    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
