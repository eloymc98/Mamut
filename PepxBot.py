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
import random

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup   
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from ImageRecognition import CNN
from functools import partial

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
curious_dict = {
    'YELLOW': ['40 PET plastic bottles can become a fleece if you throw them in the right container','80 soda cans result in a bicycle tire if properly recycled','550 aluminum cans become a chair once recycled','6 briks of milk give rise to a shoebox','To get a recycled cooking pot you need 8 canning cans','To get a shirt you only need 22 plastic bottles'],
    'BLUE': ['8 boxes of cereals generate a book of recycled material','Paper can be recycled up to 7 times','Magazine paper is the most difficult one to recycle','Recycled paper is often used to make cardboard and wrapping paper, but you can also find sheets of recycled paper'],
    'GREEN': ['Glass can be recycled infinitely without losing any of its properties','It will usually be transformed into a new container, although household items can also be made, such as a vase, among many other things','Although they seem to go to the green container, the mirrors, the ashtrays and the dishes go to the green point'],
    'BROWN': ['Compost is the fertilizer formed by the mixture of fermented organic waste and mineral materials','Any vegetable that ends up in the soil and rots with oxygen participation is transformed into compost. However, the one that does not have the help of oxygen, becomes peat (light coal of earthy and spongy appearance) and finally in coal by the effect of pressure','It is said that the first compost made by the human being and not nature was made by Sir Albert Howard, who prepared his compost with a layer of plant material of 15 centimeters','More than 40% of our garbage bags include bio-waste that is one hundred percent usable','Hair, cigarette butts, chewing gum, dust, wipes, etc. should not be deposited in this container'],
    'GREY': ['Many times, the question may arise as to whether, having been part of the same bucket, they will not get together in the garbage trucks. The answer is no. The trucks have a compartment system inside, which allows the collection of different waste in the same truck without mixing','Are the residues mixed in the recycling plant? No, although it is inevitable that in selective collection, some arrive at the plant with impurities, but these are separated and removed before treatment'],
    'SPECIAL': ['There are 1,739 fixed clean points in Spain, and 189 mobile, being and Catalonia in the first place, and in second Castilla la Mancha, the autonomous communities that most possess','The average ratio in Spain of Total Clean Points is 24,445 inhabitants per clean point','The most significant flow by weight of waste at clean points belongs to debris, and in cities, the contribution is lower per inhabitant compared to other places']
}
curious_pic_dict = {
    'YELLOW': [r'/media/eric/64C7-8922/Curious/Yellow1.jpg',r'/media/eric/64C7-8922/Curious/Yellow2.jpg',r'/media/eric/64C7-8922/Curious/Yellow3.jpg',r'/media/eric/64C7-8922/Curious/Yellow4.jpg',r'/media/eric/64C7-8922/Curious/Yellow5.jpg',r'/media/eric/64C7-8922/Curious/Yellow6.jpg'],
    'BLUE': [r'/media/eric/64C7-8922/Curious/Blue1.jpg'],
    'GREEN': [],
    'BROWN': [],
    'GREY': [],
    'SPECIAL': []
}
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
    prediction_result = learner.predict_image(image_path)
    update.message.reply_text(prediction_result)
    update.message.reply_text('\U0001F609')

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
    random_number= random.randint(0, len(curious_dict['YELLOW'])-1)

    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['YELLOW'][random_number])
    if random_number< len(curious_pic_dict['YELLOW']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['YELLOW'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_y_markup)

    return


def blue_curious(update, context):
    random_number= random.randint(0, len(curious_dict['BLUE'])-1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['BLUE'][random_number])
    if random_number< len(curious_pic_dict['BLUE']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['BLUE'][random_number], 'rb'))

    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_bl_markup)

    return


def green_curious(update, context):
    random_number= random.randint(0, len(curious_dict['GREEN'])-1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['GREEN'][random_number])
    if random_number< len(curious_pic_dict['GREEN']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['GREEN'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_green_markup)

    return


def grey_curious(update, context):
    random_number= random.randint(0, len(curious_dict['GREY'])-1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['GREY'][random_number])
    if random_number< len(curious_pic_dict['GREY']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['GREY'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_grey_markup)

    return


def brown_curious(update, context):
    random_number= random.randint(0, len(curious_dict['BROWN'])-1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['BROWN'][random_number])
    if random_number< len(curious_pic_dict['BROWN']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['BROWN'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_br_markup)

    return


def special_curious(update, context):
    random_number= random.randint(0, len(curious_dict['SPECIAL'])-1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['SPECIAL'][random_number])
    if random_number< len(curious_pic_dict['SPECIAL']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id, photo=open(curious_pic_dict['SPECIAL'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",reply_markup=yesno_sp_markup)

    return

yesno_dict = {'yes_y': yellow_curious, 'yes_bl': blue_curious, 'yes_green': green_curious, 
'yes_grey': grey_curious, 'yes_br': brown_curious, 'yes_sp': special_curious, 'No': None}

def inline_handler(update, context):
    if yesno_dict[str(update.callback_query.data)] is not None:
        yesno_dict[str(update.callback_query.data)](update, context)
        logger.info("buenos días")
        return MORE_INFO
    else:
        logger.info("malos días")
        return INTRO

def main():
    #Init learner that will predict the waste dumper
    # learner = CNN()

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
            # PHOTO: [MessageHandler(Filters.photo, partial(process_photo, learner=learner)),
            #         MessageHandler(Filters.all, photo_query)],
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
