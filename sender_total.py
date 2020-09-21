from common import *
from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

updater = Updater(token=TOKEN, use_context=True)

subscriptions = pd.read_csv("./subscriptions.csv", sep="\t")
data_all = read_data().merge(subscriptions, on="user_id").reset_index().sort_values(by=["user_id"])

def get_text(row):
    lang = row.lang
    kommunalka = "" if row.kommunalka == 0 else TEMPLATE_KOMMUNALKA[lang].format(row.water, row.electricity, row.garbage, row.total)
    text = TEMPLATE_TOTAL[lang].format(row.apart, MONTHS[lang][row.month - 1], row.rent, kommunalka,
        TEMPLATE_DEBT[lang] if (row.balance < 0) else TEMPLATE_PREPAID[lang], -row.balance if (row.balance < 0) else row.balance).replace("\n\n", "\n")
    return text

print("Начинается отправка сообщений для подписчиков\n")
sent = [];
for user_row in data_all.itertuples():
    user_id = user_row.user_id
    lang = user_row.lang
    if user_id not in sent:
        sent.append(user_id)
        data = data_all.query("user_id == '{}'".format(user_id)).reset_index()
        chat_id = str(data.at[0, "chat_id"])
        if (data.shape[0] > 1):
            send(updater.bot, chat_id, TEMPLATE_HEADER[lang])
            for row in data.itertuples():
                text = get_text(row)
                send(updater.bot, chat_id, text)
            send(updater.bot, chat_id, TEMPLATE_FOOTER[lang])
        elif (data.shape[0] == 1):
            for row in data.itertuples():
                text = get_text(row)
            send(updater.bot, chat_id, TEMPLATE_HEADER[lang] + text + TEMPLATE_FOOTER[lang])
        print("* {} — отправлено".format(user_id))
