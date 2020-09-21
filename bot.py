from common import *

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import pandas as pd
from datetime import date

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    user_id = update.message.from_user.username
    chat_id = update.message.chat.id
    user = check_user(user_id)
    if (user is None):
        send(context.bot, update.effective_chat.id, TEMPLATE_NOT_FOUND)
        return
    text = TEMPLATE_START[user["lang"]]
    subscriptions = pd.DataFrame(columns=["user_id", "chat_id"])
    try:
        temp = pd.read_csv("./subscriptions.csv", sep="\t")
        subscriptions = subscriptions.append(temp)
    except IOError:
        pass
    if (subscriptions.query("user_id == '{}'".format(user_id)).shape[0] == 0):
        subscriptions.loc[subscriptions.shape[0] + 1] = [user_id, chat_id]
    subscriptions.to_csv("./subscriptions.csv", sep="\t", index=False)
    send(context.bot, update.effective_chat.id, text)

def stop(update, context):
    user_id = update.message.from_user.username
    user = check_user(user_id)
    if (user is None):
        send(context.bot, update.effective_chat.id, TEMPLATE_NOT_FOUND)
        return
    text = TEMPLATE_STOP[user["lang"]]
    subscriptions = pd.DataFrame(columns=["user_id", "chat_id"])
    try:
        temp = pd.read_csv("./subscriptions.csv", sep="\t")
        subscriptions = subscriptions.append(temp)
    except IOError:
        pass
    if (subscriptions.query("user_id == '{}'".format(user_id)).shape[0] == 1):
        subscriptions = subscriptions.where(subscriptions["user_id"] != user_id).dropna()
    subscriptions.to_csv("./subscriptions.csv", sep="\t", index=False)
    send(context.bot, update.effective_chat.id, text)

def oplata(update, context):
    user_id = update.message.from_user.username
    user = check_user(user_id)
    if (user is None):
        send(context.bot, update.effective_chat.id, TEMPLATE_NOT_FOUND)
        return
    lang = user["lang"]
    year = str(date.today().year)
    if (len(context.args) != 0):
        try:
            year = str(context.args[0]).replace("'", "")
        except ValueError:
            pass
    data = read_oplata().query("user_id == '{}' & year == '{}'".format(user_id, year))
    if (data.shape[0] > 0):
        apartment = ""
        for row in data.itertuples():
            if (row.apart != apartment):
                if (apartment != ""):
                    send(context.bot, update.effective_chat.id, text)
                apartment = row.apart
                text = TEMPLATE_PAYMENTS[lang].format(year, apartment)
            text += "{} — <b>{}€</b>\n".format(row.date, row.summa)
        send(context.bot, update.effective_chat.id, text)
    else:
        text = TEMPLATE_PAYMENTS_NOT_FOUND[lang].format(year)
        send(context.bot, update.effective_chat.id, text)

def balance(update, context):
    user_id = update.message.from_user.username
    user = check_user(user_id)
    if (user is None):
        send(context.bot, update.effective_chat.id, TEMPLATE_NOT_FOUND)
        return
    data = read_data().query("user_id == '{}'".format(user_id))
    for row in data.itertuples():
        lang = row.lang
        text = TEMPLATE_BALANCE[lang].format(row.apart,
            TEMPLATE_DEBT[lang] if (row.balance < 0) else TEMPLATE_PREPAID[lang], -row.balance if (row.balance < 0) else row.balance)
        send(context.bot, update.effective_chat.id, text)

def info(update, context):
    user_id = update.message.from_user.username
    user = check_user(user_id)
    if (user is None):
        send(context.bot, update.effective_chat.id, TEMPLATE_NOT_FOUND)
        return
    lang = user["lang"]
    data = read_history().query("user_id == '{}'".format(user_id))
    if (data.shape[0] > 0):
        buttons = []
        for row in data[["year", "month"]].drop_duplicates().sort_values(by=["year", "month"], ascending=False).head(9).itertuples():
            buttons.append("{} {}".format(MONTHS[lang][row.month - 1], row.year))
        reply_markup = ReplyKeyboardMarkup(create_keyboard(buttons), resize_keyboard=True)
        if (len(context.args) != 0):
            text = context.args[0]
            if (len(context.args) > 1):
                text += " " + context.args[1]
            else:
                text += " " + str(date.today().year)
            update.message.text = text
            return month_info(update, context)
        text = TEMPLATE_SELECT_MONTH[lang]
        send(context.bot, update.effective_chat.id, text, reply_markup=reply_markup)
        return WAITING_MONTH
    else:
        text = TEMPLATE_BILLS_NOT_FOUND[lang]
        send(context.bot, update.effective_chat.id, text)
        return ConversationHandler.END

def month_info(update, context):
    param = update.message.text.lower().replace("'", "").split(" ")
    if (len(param) == 1):
        param.append(str(date.today().year))
    user_id = update.message.from_user.username
    month = -1
    history = read_history()
    lang = history.query("user_id == '{}'".format(user_id)).reset_index().at[0, "lang"]
    try:
        month = [x.lower() for x in MONTHS[lang]].index(param[0]) + 1
        param[0] = MONTHS[lang][month - 1]
    except ValueError:
        pass
    data = history.query("user_id == '{}' & month == '{}' & year == '{}'".format(user_id, month, param[1]))
    if (data.shape[0] > 0):
        for row in data.itertuples():
            lang = row.lang
            kommunalka = "" if row.kommunalka == 0 else TEMPLATE_KOMMUNALKA[lang].format(row.water, row.electricity, row.garbage, row.total)
            text = TEMPLATE_INFO[lang].format(row.apart, " ".join(param), row.rent, kommunalka)
            send(context.bot, update.effective_chat.id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_MONTH[lang]
        send(context.bot, update.effective_chat.id, text)
        return WAITING_MONTH


dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('stop', stop))
dispatcher.add_handler(CommandHandler('oplata', oplata))
dispatcher.add_handler(CommandHandler('balance', balance))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('info', info)
    ],
    states={
        WAITING_MONTH: [MessageHandler(Filters.text & ~Filters.command, month_info)]
    },
    fallbacks=[],
    conversation_timeout=60
    ))

print("Akacia bot started")

updater.start_polling()

updater.idle()
