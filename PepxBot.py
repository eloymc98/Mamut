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
from functools import partial

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler

from ImageRecognition import CNN
from InfoFuncs import *
from UtilityFuncs import *

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('PepxBot')

'''
Token ID of the bot
'''
TOKEN_PEPXBOT = '870743532:AAGXJayURrkNWU0FkePr7GK5k6FPkY156Z4'

'''
Configuration of states, default values, etc.
'''

dumpster_keyboard = [['Containers\n' + u'\U0001F49B', 'Paper\n' + u'\U0001F499'],
                     ['Glass\n' + u'\U0001F49A', 'Other\n' + u'\U0001F95A'],
                     ['Organic\n' + u'\U0001F45D', 'Green Point\n' + u'\U0000267B'],
                     ['Take a pic\n' + u'\U0001F4F8']]
dumpsters = ReplyKeyboardMarkup(dumpster_keyboard, one_time_keyboard=True)

function_keyboard = [['Where do I dump it?', 'What should I throw in each dumpster?']]
function_chooser = ReplyKeyboardMarkup(function_keyboard)


# Bot states' handlers

def option_menu(update, context):
    if not update.callback_query:
        update.message.reply_text("How can I help you?", reply_markup=function_chooser)
    else:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='How can I help you?',
                                 reply_markup=function_chooser)

    return INTRO


def start(update, context):
    logger.info('User has connected to EcoBot: /start')
    user_id = update.message.from_user.id
    name = get_name(update.message.from_user)
    context.bot.send_message(chat_id=update.message.chat_id, text=("Welcome " + name + " ! My name is EcoBot"+u'\U0001F30D'))
    logger.info('Name of user is: ' + name + " and its ID is " + str(user_id))

    return option_menu(update, context)


def exit_chat(update, context):
    update.message.reply_text("See you next time")
    logger.info('User ' + get_name(update.message.from_user) + ' finish with AideBot')
    return ConversationHandler.END


def photo_query(update, context):
    update.message.reply_text('Ok! Send me a picture of the waste, please.')

    return PHOTO


def dumpster_select(update, context):
    update.message.reply_text('Ok! Which dumpster would you like to know about?', reply_markup=dumpsters)

    return INFO


def process_photo(update, context, learner):
    # Retrieve image from telegram server
    filename = update.message.photo[-1].file_id
    image_path = os.path.join(r'C:\Users\Mephistopheles\Pictures', filename + '.jpg')
    context.bot.getFile(filename).download(image_path)

    # Predict with learner
    prediction_result = learner.predict_image(image_path)
    update.message.reply_text(prediction_result)
    update.message.reply_text('\U0001F609')

    return option_menu(update, context)


yesno_dict = {'yes_y': yellow_curious, 'yes_bl': blue_curious, 'yes_green': green_curious,
              'yes_grey': grey_curious, 'yes_br': brown_curious, 'yes_sp': special_curious, 'No': None}


def inline_handler(update, context):
    if yesno_dict[str(update.callback_query.data)] is not None:
        yesno_dict[str(update.callback_query.data)](update, context)
        logger.info("buenos días")
        return MORE_INFO

    else:
        logger.info("malos días")
        return option_menu(update, context)


def main():
    # Init learner that will predict the waste dumper
    learner = CNN()

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
            PHOTO: [MessageHandler(Filters.photo, partial(process_photo, learner=learner)),
                    MessageHandler(Filters.all, photo_query)],
            INFO: [MessageHandler(Filters.regex('Containers\n' + u'\U0001F49B'), yellow_info),
                   MessageHandler(Filters.regex('Paper\n' + u'\U0001F499'), blue_info),
                   MessageHandler(Filters.regex('Glass\n' + u'\U0001F49A'), green_info),
                   MessageHandler(Filters.regex('Other\n' + u'\U0001F95A'), grey_info),
                   MessageHandler(Filters.regex('Organic\n' + u'\U0001F45D'), brown_info),
                   MessageHandler(Filters.regex('Green Point\n' + u'\U0000267B'), special_info),
                   MessageHandler(Filters.regex('Take a pic\n' + u'\U0001F4F8'), photo_query)],
            MORE_INFO: [CallbackQueryHandler(inline_handler)]

        },
        fallbacks=[MessageHandler(Filters.regex('^[E|e]xit$'), exit_chat)]

    )


    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
