import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from UtilityFuncs import build_menu

# States
INTRO, PHOTO, INFO, MORE_INFO = range(4)

curious_dict = {
    'YELLOW': ['40 PET plastic bottles can become a wool sweater if you throw them in the right container',
               '80 soda cans result in a bicycle tire if properly recycled',
               '550 aluminum cans become a chair once recycled', '6 briks of milk give rise to a shoebox',
               'To get a recycled cooking pot you need 8 tinned food cans',
               'To get a shirt you only need 22 plastic bottles'],
    'BLUE': ['8 boxes of cereals generate a book of recycled material', 'Paper can be recycled up to 7 times',
             'Magazine paper is the most difficult one to recycle',
             'Recycled paper is often used to make cardboard and wrapping paper, but you can also find sheets of recycled '
             'paper'],
    'GREEN': ['Glass can be recycled infinitely without losing any of its properties',
              'It will usually be transformed into a new container, although household items can also be made, such as a '
              'vase, among many other things',
              'Although they seem to go to the green container, the mirrors, the ashtrays and the dishes go to the green point'],
    'BROWN': ['Compost is the fertilizer formed by the mixture of fermented organic waste and mineral materials',
              'Any vegetable that ends up in the soil and rots with oxygen participation is transformed into compost. '
              'However, the one that does not have the help of oxygen, becomes peat (light coal of earthy and spongy '
              'appearance) and finally in coal by the effect of pressure',
              'It is said that the first compost made by the human being and not nature was made by Sir Albert Howard, '
              'who prepared his compost with a layer of plant material of 15 centimeters',
              'More than 40% of our garbage bags include bio-waste that is one hundred percent usable',
              'Hair, cigarette butts, chewing gum, dust, wipes, etc. should not be deposited in this container'],
    'GREY': [
        'Many times, the question may arise as to whether, having been part of the same bucket, they will not get '
        'together in the garbage trucks. The answer is no. The trucks have a compartment system inside, which allows the '
        'collection of different waste in the same truck without mixing',
        'Are the residues mixed in the recycling plant? No, although it is inevitable that in selective collection, '
        'some arrive at the plant with impurities, but these are separated and removed before treatment'],
    'SPECIAL': [
        'There are 1,739 fixed clean points in Spain, and 189 mobile, being Catalonia and '
        'Castilla la Mancha the autonomous communities that most points possess',
        'The average ratio in Spain of Total Clean Points is 24,445 inhabitants per clean point',
        'The most significant flow by weight of waste at clean points belongs to debris, and in cities, the contribution'
        ' is lower per inhabitant, compared to other places']
}
curious_pic_dict = {
    'YELLOW': [r'./Curious/Yellow1.jpg', r'./Curious/Yellow2.jpg',
               r'./Curious/Yellow3.jpg', r'./Curious/Yellow4.jpg',
               r'./Curious/Yellow5.jpg', r'./Curious/Yellow6.jpg'],
    'BLUE': [r'./Curious/Blue1.jpg'],
    'GREEN': [],
    'BROWN': [],
    'GREY': [],
    'SPECIAL': []
}

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


# Dumpers info
def yellow_info(update, context):
    update.message.reply_text(
        "Inside the yellow container, we must deposit: plastic bottles and containers, metal containers and briks such as:")
    update.message.reply_text('- Plastic bottles\n- Cans\n- Plastic, metal and sheet metal caps\n- Aluminum trays\n'
                              '- Film and aluminum foil\n- Aerosol sprays\n- Deodorant cans\n- Plastic bags '
                              '(except garbage bags)\n- Tubs and yogurt lids\n- Briks: of milk, juices, soups, etc.\n'
                              '- Cork trays\n- Toothpaste tubes')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
                             reply_markup=yesno_y_markup)
    return MORE_INFO


def blue_info(update, context):
    update.message.reply_text("The blue container is the container intended for recycling paper and cardboard \
        containers. Among these wastes are:")
    update.message.reply_text('- Paper or cardboard bags\n- Cardboard boxes\n- Shoe boxes\n- Cardboard egg cups\n'
                              '- Notebooks\n- Promotional leaflet\n- Paper\n- Gift Paper\n- Newspapers\n- Magazine\n'
                              '- Envelopes\n- Cardboard tubes of toilet paper and kitchen')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
                             reply_markup=yesno_bl_markup)
    return MORE_INFO


def green_info(update, context):
    update.message.reply_text(
        "The green container is the container for the recycling of glass. Among these wastes are:")
    update.message.reply_text('- Glass bottles (juices, soft drinks, wines, spirits, ciders, sauces, oil, etc.)\n'
                              '- Glass jars (both for drinks and canned food, as for perfumes, colognes, etc.')
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
    update.message.reply_text(
        "All organic waste must be deposited, that is, those compounds of biodegradable matter such as:")
    update.message.reply_text('- Remains of fruit and vegetables\n- Leftovers of meat and fish\n- Eggshells, shellfish, '
                              'nuts, etc.\n- Other remains of meals\n- Coffee grounds and infusions\n- Cork stoppers '
                              'that do not have plastic additives\n- Matches and sawdust\n- Kitchen paper and dirty napkins\n'
                              '- Small traces of gardening.')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
                             reply_markup=yesno_br_markup)
    return MORE_INFO


def special_info(update, context):
    update.message.reply_text("It serves to deposit all waste that is not accepted in ordinary containers:")
    update.message.reply_text('- Tires\n- Fluorescent and mercury vapor lamps\n- Solvents\n- Paints and varnishes\n'
                              '- Batteries\n- Appliances containing dangerous substances\n- Used mineral oils\n'
                              '- Furniture and others\n- Appliances that do not contain hazardous substances\n'
                              '- Electronic scrap (computers, small appliances, electronic devices, etc.)')
    context.bot.send_message(chat_id=update.message.chat_id, text="More info?",
                             reply_markup=yesno_sp_markup)
    return MORE_INFO


def yellow_curious(update, context):
    random_number = random.randint(0, len(curious_dict['YELLOW']) - 1)

    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['YELLOW'][random_number])
    if random_number < len(curious_pic_dict['YELLOW']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['YELLOW'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_y_markup)

    return


def blue_curious(update, context):
    random_number = random.randint(0, len(curious_dict['BLUE']) - 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['BLUE'][random_number])
    if random_number < len(curious_pic_dict['BLUE']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['BLUE'][random_number], 'rb'))

    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_bl_markup)

    return


def green_curious(update, context):
    random_number = random.randint(0, len(curious_dict['GREEN']) - 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['GREEN'][random_number])
    if random_number < len(curious_pic_dict['GREEN']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['GREEN'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_green_markup)

    return


def grey_curious(update, context):
    random_number = random.randint(0, len(curious_dict['GREY']) - 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['GREY'][random_number])
    if random_number < len(curious_pic_dict['GREY']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['GREY'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_grey_markup)

    return


def brown_curious(update, context):
    random_number = random.randint(0, len(curious_dict['BROWN']) - 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['BROWN'][random_number])
    if random_number < len(curious_pic_dict['BROWN']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['BROWN'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_br_markup)

    return


def special_curious(update, context):
    random_number = random.randint(0, len(curious_dict['SPECIAL']) - 1)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text=curious_dict['SPECIAL'][random_number])
    if random_number < len(curious_pic_dict['SPECIAL']):
        context.bot.send_photo(chat_id=update.callback_query.message.chat_id,
                               photo=open(curious_pic_dict['SPECIAL'][random_number], 'rb'))
    context.bot.send_message(chat_id=update.callback_query.message.chat_id, text="More info?",
                             reply_markup=yesno_sp_markup)

    return
