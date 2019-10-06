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
import time

<<<<<<< HEAD
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup   
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
=======
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from ImageRecognition import CNN
from functools import partial
>>>>>>> 4b4ffe400e83ce6bd78284ca2a6aeb94beb2a198

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('PepxBot')

'''
Token ID of the bot
'''
TOKEN_PEPXBOT = '870743532:AAGXJayURrkNWU0FkePr7GK5k6FPkY156Z4'

'''
Configuration of states, default values, etc.
'''
INTRO, PHOTO, INFO, MORE_INFO = range(4)

dumpster_keyboard = [['Containers\n'+u'\U0001F49B', 'Paper\n'+u'\U0001F499'],
                     ['Glass\n'+u'\U0001F49A', 'Other\n'+u'\U0001F95A'],
                     ['Organic\n'+u'\U0001F45D', 'Green Point\n'+u'\U0000267B'],
                     ['Take a pic\n'+u'\U0001F4F8']]
dumpsters = ReplyKeyboardMarkup(dumpster_keyboard, one_time_keyboard=True)
def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])
    return menu

yesno_y_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_y"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_y_markup = InlineKeyboardMarkup(build_menu(yesno_y_keyboard, n_cols=2))

yesno_bl_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_bl"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_bl_markup = InlineKeyboardMarkup(build_menu(yesno_bl_keyboard, n_cols=2))

yesno_green_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_green"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_green_markup = InlineKeyboardMarkup(build_menu(yesno_green_keyboard, n_cols=2))
yesno_grey_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_grey"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_grey_markup = InlineKeyboardMarkup(build_menu(yesno_grey_keyboard, n_cols=2))
yesno_br_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_br"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_br_markup = InlineKeyboardMarkup(build_menu(yesno_br_keyboard, n_cols=2))
yesno_sp_keyboard = [
    InlineKeyboardButton("Yes", callback_data="yes_sp"),
    InlineKeyboardButton("No", callback_data="No")
]
yesno_sp_markup = InlineKeyboardMarkup(build_menu(yesno_sp_keyboard, n_cols=2))

    
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


# Bot states' handlers

def option_menu(update, context):
    if not update.callback_query:
        update.message.reply_text("How can I help you?", reply_markup=function_chooser)
    else:
        context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='How can I help you?', reply_markup=function_chooser)

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
    update.message.reply_text('Ok! Which dumpster would you like to know about?', reply_markup=dumpsters)

    return INFO


def process_photo(update, context, learner):
    # Retrieve image from telegram server
    filename = update.message.photo[-1].file_id
    image_path = os.path.join(r'C:\Users\Mephistopheles\Pictures', filename + '.jpg')
    context.bot.getFile(filename).download(image_path)

    # Predict with learner
    prediction_result = learner.predict(image_path)
    update.message.reply_text(prediction_result)

    return option_menu(update, context)


# Dumpers info
def yellow_info(update, context):
    update.message.reply_text("Inside the yellow container, we must deposit: plastic bottles and containers, metal containers and briks such as:")
    update.message.reply_text('- Plastic bottles\n- Cans\n- Plastic, metal and sheet metal caps\
        \n- Aluminum trays\n- Film and aluminum foil\n- Aerosol sprays\n- Deodorant cans\n- Plastic bags (except garbage bags)\
        \n- Tubs and yogurt lids\n- Briks: of milk, juices, soups, etc.\n- Cork trays\n- Toothpaste tubes')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_y_markup)
    return MORE_INFO


def blue_info(update, context):
    update.message.reply_text("The blue container is the container intended for recycling paper and cardboard \
        containers. Among these wastes are:")
    update.message.reply_text('- Paper or cardboard bags\n- Cardboard boxes\n- Shoe boxes\n- Cardboard egg cups\n- Notebooks\
        \n- Promotional leaflet\n- Paper\n- Gift Paper\n- Newspapers\n- Magazine\n- Envelopes\n- Cardboard tubes of toilet paper and kitchen')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_bl_markup)
    return MORE_INFO


def green_info(update, context):
    update.message.reply_text("The green container is the container for the recycling of glass. Among these wastes are:")
    update.message.reply_text('- Glass bottles (juices, soft drinks, wines, spirits, ciders, sauces, oil, etc.)\n\
        - Glass jars (both for drinks and canned food, as for perfumes, colognes, etc.')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_green_markup)
    return MORE_INFO


def grey_info(update, context):
    update.message.reply_text("¿What should I deposit in the GRAY container?\n")
    update.message.reply_text('- Fraction remainder (waste for which there is no specific container on public roads)')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_grey_markup)
    return MORE_INFO


def brown_info(update, context):
    update.message.reply_text("All organic waste must be deposited, that is, those compounds of biodegradable matter such as:")
    update.message.reply_text('- Remains of fruit and vegetables\n- Leftovers of meat and fish\n- Eggshells, shellfish, nuts, etc.\n\
        - Other remains of meals\n- Coffee grounds and infusions\n- Cork stoppers that do not have \
        plastic additives\n- Matches and sawdust\n- Kitchen paper and dirty napkins\n- Small traces of gardening.')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_br_markup)
    return MORE_INFO


def special_info(update, context):
    update.message.reply_text("It serves to deposit all waste that is not accepted in ordinary containers:")
    update.message.reply_text('- Tires\n- Fluorescent and mercury vapor lamps\n- Solvents\n- Paints and varnishes\n- Batteries\n\
        - Appliances containing dangerous substances\n- Used mineral oils\n- Furniture and others\n- Appliances that do \
        not contain hazardous substances\n- Electronic scrap (computers, small appliances, electronic devices, etc.)')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
reply_markup=yesno_sp_markup)
    return MORE_INFO


def yellow_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata amarilla')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_y_markup)

    return


def blue_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata azul')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_bl_markup)

    return


def green_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata green')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_green_markup)

    return


def grey_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata grey')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_grey_markup)

    return


def brown_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata marron')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_br_markup)

    return


def special_curious(update, context):
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text='Patata especial, como Ralph Wiggum. SOY ESPECIAAL!')
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_sp_markup)

    return

yesno_dict = {'yes_y': yellow_curious, 'yes_bl': blue_curious, 'yes_green': green_curious, 
'yes_grey': grey_curious, 'yes_br': brown_curious, 'yes_sp': special_curious, 'No': None}

def inline_handler(update, context):
    if yesno_dict[str(update.callback_query.data)] is not None:
        yesno_dict[str(update.callback_query.data)](update, context)
        return MORE_INFO
    else:
        return INTRO

def main():
    #Init learner that will predict the waste dumper
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
            INFO: [MessageHandler(Filters.regex('Containers\n'+u'\U0001F49B'), yellow_info),
                   MessageHandler(Filters.regex('Paper\n'+u'\U0001F499'), blue_info),
                   MessageHandler(Filters.regex('Glass\n'+u'\U0001F49A'), green_info),
                   MessageHandler(Filters.regex('Other\n'+u'\U0001F95A'), grey_info),
                   MessageHandler(Filters.regex('Organic\n'+u'\U0001F45D'), brown_info),
                   MessageHandler(Filters.regex('Green Point\n'+u'\U0000267B'), special_info),
                   MessageHandler(Filters.regex('Take a pic\n'+u'\U0001F4F8'), photo_query)],
            MORE_INFO: [CallbackQueryHandler(inline_handler)]


        },
        fallbacks=[MessageHandler(Filters.regex('^Exit$'), exit)]

    )

    dp.add_handler(conv_handler)
    #dp.add_handler(CallbackQueryHandler(inline_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
