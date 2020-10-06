from common import *

from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

import pandas as pd
from datetime import datetime

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN_PAYMENTS, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.username
    user = check_payments_user(user_id)
    if (user is None):
        send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return
    send(context.bot, chat_id, TEMPLATE_MANAGER_FOUND)

def add(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.username
    user = check_payments_user(user_id)
    if (user is None):
        send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return ConversationHandler.END
    context.user_data["route"] = "add"
    if (len(context.args) == 0):
        send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return apart_num(update, context)

def apart_num(update, context):
    apart = None
    try:
        apart = int(update.message.text)
    except ValueError:
        send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return ConversationHandler.END
    if (apart is None):
        send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return ConversationHandler.END
    context.user_data["apart"] = apart
    if (context.user_data["route"] == "add"):
        return select_renters(update, context)
    elif (context.user_data["route"] == "balance"):
        return show_balance(update, context)
    elif (context.user_data["route"] == "info"):
        return show_info(update, context)
    elif (context.user_data["route"] == "oplata"):
        return select_renters(update, context)
    else:
        return ConversationHandler.END

def select_renters(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    data = read_history() if context.user_data["route"] == "add" else read_oplata()
    data = data.query("apart == {} & name != ''".format(apart))
    if (data.shape[0] == 0):
        send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return ConversationHandler.END
    buttons = []
    for row in data[["name"]].drop_duplicates().sort_values(by=["name"]).itertuples():
        buttons.append("{}".format(row.name))
    reply_markup = ReplyKeyboardMarkup(create_keyboard(buttons), resize_keyboard=True)
    send(context.bot, chat_id, TEMPLATE_SEND_RENTER.format(apart), reply_markup=reply_markup)
    return WAITING_RENTER

def renter(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    renter = update.message.text.replace("'", "")
    data = read_history() if context.user_data["route"] == "add" else read_oplata()
    data = data.query("apart == {} & name == '{}'".format(apart, renter))
    if (data.shape[0] == 0):
        send(context.bot, chat_id, TEMPLATE_ERROR_IN_APART)
        return WAITING_RENTER
    context.user_data["renter"] = renter
    data = data.dropna().reset_index()
    context.user_data["user_id"] = data.at[0, "user_id"] if data.shape[0] > 0 else ""
    if context.user_data["route"] == "add":
        send(context.bot, chat_id, TEMPLATE_SEND_SUM.format(renter, apart), reply_markup=ReplyKeyboardRemove())
        return WAITING_SUM
    elif context.user_data["route"] == "oplata":
        return show_oplata(update, context)
    else:
        return ConversationHandler.END

def add_sum(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    renter = context.user_data["renter"]
    user_id = context.user_data["user_id"]
    params = update.message.text.replace("'", "").split(" ")
    comment = " ".join(params[1:]) if len(params) > 1 else ""
    summa = 0
    try:
        summa = int(params[0])
    except ValueError:
        send(context.bot, chat_id, TEMPLATE_ERROR_SUM)
        return WAITING_SUM
    context.user_data["summa"] = summa
    context.user_data["comment"] = comment
    send(context.bot, chat_id, TEMPLATE_CONFIRM_SUM.format(summa, renter, apart),
        reply_markup=ReplyKeyboardMarkup([[TEMPLATE_YES, TEMPLATE_NO]], resize_keyboard=True))
    return WAITING_CONFIRM_SUM

def confirm_sum(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    renter = context.user_data["renter"]
    user_id = context.user_data["user_id"]
    summa = context.user_data["summa"]
    comment = context.user_data["comment"]
    confirm = update.message.text.replace("'", "").lower()
    if (confirm != "да"):
        send(context.bot, chat_id, TEMPLATE_SEND_SUM.format(renter, apart), reply_markup=ReplyKeyboardRemove())
        return WAITING_SUM
    payments = pd.DataFrame(columns=["date", "apart", "name", "summa", "comment", "manager", "imported"])
    try:
        temp = pd.read_csv("./payments.csv", sep="\t")
        payments = payments.append(temp)
    except IOError:
        pass
    payments.loc[payments.shape[0] + 1] = [
        datetime.today().strftime("%Y-%m-%d %H:%M:%S"),
        renter,
        apart,
        summa,
        comment,
        update.message.from_user.username,
        0
    ]
    payments.to_csv("./payments.csv", sep="\t", index=False, encoding="cp1251")
    send(context.bot, chat_id, TEMPLATE_DATA_SAVED.format(summa, renter, apart), reply_markup=ReplyKeyboardRemove())
    if (user_id != ""):
        subscriptions = pd.read_csv("./subscriptions.csv", sep="\t").query("user_id == '{}'".format(user_id)).reset_index()
        if (subscriptions.shape[0] != 0):
            user = check_user(user_id)
            sender = Updater(token=TOKEN, use_context=True)
            send(sender.bot, str(subscriptions.at[0, "chat_id"]), TEMPLATE_PAYMENT_ACCEPTED[user["lang"]].format(summa, apart))
            send(context.bot, chat_id, TEMPLATE_DATA_SENDED.format(user_id))
    return ConversationHandler.END

def exit(update, context):
    chat_id = update.message.chat.id
    send(context.bot, chat_id, TEMPLATE_EXIT_CONVERSATION, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def balance(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.username
    user = check_payments_user(user_id)
    if (user is None):
        send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return ConversationHandler.END
    context.user_data["route"] = "balance"
    if (len(context.args) == 0):
        send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return apart_num(update, context)

def show_balance(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    data = read_data().query("apart == '{}'".format(apart))
    for row in data.itertuples():
        lang = RU
        text = TEMPLATE_BALANCE[lang].format(row.apart,
            TEMPLATE_DEBT[lang] if (row.balance < 0) else TEMPLATE_PREPAID[lang], -row.balance if (row.balance < 0) else row.balance)
        send(context.bot, chat_id, text)
    return ConversationHandler.END

def info(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.username
    user = check_payments_user(user_id)
    if (user is None):
        send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return ConversationHandler.END
    context.user_data["route"] = "info"
    if (len(context.args) == 0):
        send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return apart_num(update, context)

def show_info(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    lang = RU
    data = read_history().query("apart == '{}'".format(apart))
    if (data.shape[0] > 0):
        buttons = []
        for row in data[["year", "month"]].drop_duplicates().sort_values(by=["year", "month"], ascending=False).head(12).itertuples():
            buttons.append("{} {}".format(MONTHS[lang][row.month - 1], row.year))
        reply_markup = ReplyKeyboardMarkup(create_keyboard(buttons), resize_keyboard=True)
        send(context.bot, chat_id, text = TEMPLATE_SELECT_MONTH[lang][:-1] + TEMPLATE_COMMAND_EXIT, reply_markup=reply_markup)
        return WAITING_MONTH
    else:
        text = TEMPLATE_BILLS_NOT_FOUND[lang]
        send(context.bot, chat_id, text)
        return ConversationHandler.END

def month_info(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    lang = RU
    param = update.message.text.lower().replace("'", "").split(" ")
    if (len(param) == 1):
        param.append(str(datetime.today().year))
    user_id = update.message.from_user.username
    month = -1
    history = read_history()
    try:
        month = [x.lower() for x in MONTHS[lang]].index(param[0]) + 1
        param[0] = MONTHS[lang][month - 1]
    except ValueError:
        pass
    data = history.query("apart == '{}' & month == '{}' & year == '{}'".format(apart, month, param[1]))
    if (data.shape[0] > 0):
        for row in data.itertuples():
            kommunalka = "" if row.kommunalka == 0 else TEMPLATE_KOMMUNALKA[lang].format(row.water, row.electricity, row.garbage, row.total)
            text = TEMPLATE_INFO[lang].format(row.apart, " ".join(param), row.rent, kommunalka)
            send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        text = TEMPLATE_SELECT_AVAILABLE_MONTH[lang][:-1] + TEMPLATE_COMMAND_EXIT
        send(context.bot, chat_id, text)
        return WAITING_MONTH

def oplata(update, context):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.username
    user = check_payments_user(user_id)
    if (user is None):
        send(context.bot, chat_id, TEMPLATE_MANAGER_NOT_FOUND)
        return ConversationHandler.END
    context.user_data["route"] = "oplata"
    if (len(context.args) == 0):
        send(context.bot, chat_id, TEMPLATE_SEND_APART)
        return WAITING_APART
    else:
        update.message.text = context.args[0]
        return apart_num(update, context)

def show_oplata(update, context):
    chat_id = update.message.chat.id
    apart = context.user_data["apart"]
    renter = context.user_data["renter"]
    data = read_oplata().query("name == '{}' & apart == {}".format(renter, apart))
    text = TEMPLATE_PAYMENTS_BY_RENTER.format(renter, apart)
    for row in data.itertuples():
        text += "{} — <b>{}€</b>\n".format(row.date, row.summa)
    send(context.bot, chat_id, text, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



dispatcher.add_handler(CommandHandler('start', start))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('add', add)
    ],
    states={
        WAITING_APART: [
            MessageHandler(Filters.text & ~Filters.command, apart_num),
            CommandHandler('exit', exit)
        ],
        WAITING_RENTER: [
            MessageHandler(Filters.text & ~Filters.command, renter),
            CommandHandler('exit', exit)
        ],
        WAITING_SUM: [
            MessageHandler(Filters.text & ~Filters.command, add_sum),
            CommandHandler('exit', exit)
        ],
        WAITING_CONFIRM_SUM: [
            MessageHandler(Filters.text & ~Filters.command, confirm_sum),
            CommandHandler('exit', exit)
        ]
    },
    fallbacks=[
        CommandHandler('exit', exit)
    ],
    conversation_timeout=60
    ))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('balance', balance)
    ],
    states={
        WAITING_APART: [
            MessageHandler(Filters.text & ~Filters.command, apart_num),
            CommandHandler('exit', exit)
        ]
    },
    fallbacks=[
        CommandHandler('exit', exit)
    ],
    conversation_timeout=60
    ))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('info', info)
    ],
    states={
        WAITING_APART: [
            MessageHandler(Filters.text & ~Filters.command, apart_num),
            CommandHandler('exit', exit)
        ],
        WAITING_MONTH: [
            MessageHandler(Filters.text & ~Filters.command, month_info),
            CommandHandler('exit', exit)
        ]
    },
    fallbacks=[
        CommandHandler('exit', exit)
    ],
    conversation_timeout=60
    ))

dispatcher.add_handler(ConversationHandler(
    entry_points=[
        CommandHandler('oplata', oplata)
    ],
    states={
        WAITING_APART: [
            MessageHandler(Filters.text & ~Filters.command, apart_num),
            CommandHandler('exit', exit)
        ],
        WAITING_RENTER: [
            MessageHandler(Filters.text & ~Filters.command, renter),
            CommandHandler('exit', exit)
        ]
    },
    fallbacks=[
        CommandHandler('exit', exit)
    ],
    conversation_timeout=60
    ))

print("Akacia payments bot started")

updater.start_polling()

updater.idle()
