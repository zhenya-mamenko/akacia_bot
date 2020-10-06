import pandas as pd

RU = 0
SR = 1
EN = 2

TOKEN = ""
TOKEN_PAYMENTS = ""

WAITING_MONTH = 666

WAITING_APART = 333
WAITING_RENTER = 334
WAITING_SUM = 335
WAITING_CONFIRM_SUM = 336


MONTHS = {
    RU: ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"],
    SR: ["januar", "februar", "mart", "april", "maj", "jun", "jul", "avgust", "septembar", "oktobar", "novembar", "decembar"],
    EN: ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
}

TEMPLATE_NOT_FOUND = (
    "Вы не найдены в списках жителей Акации. Обратитесь к администрации.\n\n"
    "Nismo našli vas u spisku stanara Akaciji. Javite se administraciji.\n\n"
    "You aren't found in list of Akacia apartments' renters. Please, ask Akacia's management about this situation."
)

TEMPLATE_PAYMENTS_NOT_FOUND = {
    RU: "Не найдены платежи за <b>{0}</b> год. Если вы считаете, что это ошибка, то обратитесь к администрации.\n\n",
    SR: "Nemamo računa za <b>{0}</b> godinu. Ako mislite na grešku pa kontaktirate administraciju.\n\n",
    EN: "Payments for <b>{0}</b> are not found. If you aren't ok with it, please, ask Akacia's management."
}

TEMPLATE_BILLS_NOT_FOUND = {
    RU: "Начисления не найдены. Если вы считаете, что это ошибка, то обратитесь к администрации.\n\n",
    SR: "Nema računa. Ako mislite na grešku pa kontaktirate administraciju.\n\n",
    EN: "Biils for <b>{0}</b> are not found. If you aren't ok with it, please, ask Akacia's management."
}

TEMPLATE_HEADER = {
    RU: "Тук-тук! Настал день арендной платы! :)\n\n",
    SR: "Kuc-kuc! Došao je dan naplate! :)\n\n",
    EN: "Knock-knock! It's a rent payment day! :)\n\n"
}

TEMPLATE_TOTAL = {
    RU: ("По квартире <b>{}</b> за <b>{}</b> начислено:\n— аренда <b>{:.2f}€</b>\n{}"
        "Текущий {} (с учетом предыдущих месяцев) составляет <b>{:.2f}€</b>"),
    SR: ("Po stanu <b>{}</b> za <b>{}</b> uračunato:\n— boravište <b>{:.2f}€</b>\n{}"
        "Trenutni {} (uključuje prethodne periode) je <b>{:.2f}€</b>"),
    EN: ("<b>{1}</b> bills for apartment <b>{0}</b> are:\n— rent <b>{2:.2f}€</b>\n{3}"
        "The current {4} (including previous periods) is <b>{5:.2f}€</b>"),
}

TEMPLATE_FOOTER = {
    RU: "\n\nСпасибо, что живете в Акации! ❤",
    SR: "\n\nHvala vam sto živite u Akaciji! ❤",
    EN: "\n\nThank you for living at Akacia apartments! ❤"
}

TEMPLATE_KOMMUNALKA_MONTH = {
    RU: "\nКоммунальные услуги за <b>{}</b>:\n",
    SR: "\nKomunalije za <b>{}</b>:\n",
    EN: "\nMunicipal services for <b>{}</b>:\n"
}

TEMPLATE_KOMMUNALKA = {
    RU: ("— вода <b>{:.2f}€</b>\n— электричество <b>{:.2f}€</b>\n"
        "— вывоз мусора <b>{:.2f}€</b>\n<u>Всего</u>: <b>{:.2f}€</b>\n\n"),
    SR: ("— voda <b>{:.2f}€</b>\n— struja <b>{:.2f}€</b>\n"
        "— odvoz smeća <b>{:.2f}€</b>\n<u>Ukupno</u>: <b>{:.2f}€</b>\n\n"),
    EN: ("— water <b>{:.2f}€</b>\n— electricity <b>{:.2f}€</b>\n"
        "— garbage disposal <b>{:.2f}€</b>\n<u>Total</u>: <b>{:.2f}€</b>\n\n")
}

TEMPLATE_DEBT = {
    RU: "долг",
    SR: "dug",
    EN: "debt"
}

TEMPLATE_PREPAID = {
    RU: "аванс",
    SR: "bilans",
    EN: "advance payment"
}

TEMPLATE_BALANCE = {
    RU: "По квартире <b>{}</b> текущий {} (с учетом предыдущих месяцев) составляет <b>{:.2f}€</b>",
    SR: "Po stanu <b>{}</b> trenutni {} (uključuje prethodne periode) je <b>{:.2f}€</b>",
    EN: "For apartment <b>{}</b> the current {} (including previous periods) is <b>{:.2f}€</b>"
}

TEMPLATE_INFO = {
    RU: "По квартире <b>{}</b> за <b>{}</b> начислено:\n— аренда <b>{:.2f}€</b>\n{}",
    SR: "Po stanu <b>{}</b> za <b>{}</b> uračunato:\n— boravište <b>{:.2f}€</b>\n{}",
    EN: "<b>{1}</b> bills for apartment <b>{0}</b> are:\n— rent <b>{2:.2f}€</b>\n{3}"
}

TEMPLATE_PAYMENTS = {
    RU: "За <b>{}</b> год по квартире <b>{}</b> поступило оплат:\n\n",
    SR: "Za <b>{}</b> godinu po stanu <b>{}</b> ima računa:\n\n",
    EN: "These payments were received in <b>{}</b> for apartment <b>{}</b>:\n\n",
}

TEMPLATE_START = {
    RU: "Вы подписаны на получение сообщений от Акации. Для остановки подписки отправьте /stop",
    SR: "Vi ste potpisani na obaveštenje od Akaciji. Za prekid pošaljite poruku /stop",
    EN: "You are subscribed to the message list from the Akacia apartments. Send /stop to stop your subscription."
}

TEMPLATE_STOP = {
    RU: "Вы отписаны от получения сообщений от Акации. Для начала подписки отправьте /start",
    SR: "Prekinuli ste obaveštenje od Akaciji. Za potpisku pošaljite poruku /start",
    EN: "You are unsubscribed from the Akacia apartments' message list. Send /start to start your subscription."
}

TEMPLATE_SELECT_MONTH = {
    RU: "Отправьте месяц, за который хотите получить информацию по начислениям.",
    SR: "Izaberite mesec koji je potreban za izvod računa.",
    EN: "Send the month for which you want to get information on bills."
}

TEMPLATE_SELECT_AVAILABLE_MONTH = {
    RU: "Выберите один из доступных месяцев.",
    SR: "Izaberite dostupan mesec.",
    EN: "Select month with available data."
}

TEMPLATE_YES = "Да"
TEMPLATE_NO = "Нет. НЕТ! Срочная отмена!1!"
TEMPLATE_MANAGER_NOT_FOUND = "https://www.youtube.com/watch?v=7OBx-YwPl8g"
TEMPLATE_MANAGER_FOUND = "Отправьте команду /add для добавления новой записи о внесении денег."
TEMPLATE_ERROR_IN_APART = "Неверный номер квартиры, имя жильца или нет записей о проживании."
TEMPLATE_COMMAND_EXIT = " или отправьте /exit."
TEMPLATE_SEND_APART = "Отправьте номер квартиры" + TEMPLATE_COMMAND_EXIT
TEMPLATE_SEND_RENTER = "Отправьте имя арендатора из квартиры <b>{}</b>" + TEMPLATE_COMMAND_EXIT
TEMPLATE_SEND_SUM = "Отправьте сумму, принятую от <b>{}</b> из квартиры <b>{}</b>" + TEMPLATE_COMMAND_EXIT
TEMPLATE_ERROR_SUM = "Неверная сумма. Отправьте целое число [и комментарий после пробела]."
TEMPLATE_EXIT_CONVERSATION = "Вы вышли из диалога. " + TEMPLATE_MANAGER_FOUND
TEMPLATE_CONFIRM_SUM = "Внести <b>{}€</b> от <b>{}</b> в счёт оплаты квартиры <b>{}</b>?"
TEMPLATE_DATA_SAVED = "Данные об оплате <b>{}€</b> от <b>{}</b> из квартиры <b>{}</b> сохранены."
TEMPLATE_DATA_SENDED = "Пользователю <b>{}</b> было отправлено об этом сообщение."
TEMPLATE_PAYMENTS_BY_RENTER = "От <b>{}</b> по квартире <b>{}</b> поступило оплат:\n\n"
TEMPLATE_PAYMENT_ACCEPTED = {
    RU: "Сумма <b>{}€</b> по квартире <b>{}</b> будет зачислена на ваш счёт в течение суток. Спасибо за своевременную оплату!",
    SR: "Iznos od <b>{}€</b> za stan <b>{}</b> biće uplaćen na vaš račun u toku dana. Zahvaljujemo na redovnoj uplati!",
    EN: "Payment <b>{}€</b> for apartment <b>{}</b> will be placed on your account during 24h. Thank you for paying in time!"
}

def create_keyboard(buttons):
    result = []
    for i in range(int(len(buttons) / 3) + 1):
        if (len(buttons) <= 3):
            result.append(buttons)
            break
        result.append(buttons[:3])
        buttons = buttons[3:]
    return result

def read_data():
    return pd.read_csv("./data.txt", sep="\t", encoding="cp1251").query("user_id != ''").dropna()\
        .replace(to_replace=r"^([-\d]+)[,](\d+)$", value="\g<1>.\g<2>", regex=True)\
        .astype({"rent": "float32", "water": "float32", "electricity": "float32", "garbage": "float32",
            "total": "float32", "balance": "float32", "lang": "int", "apart": "int"})

def read_oplata():
    oplata = pd.read_csv("./oplata.txt", sep="\t", encoding="cp1251")
    oplata["user_id"] = oplata["user_id"].fillna("")
    oplata["lang"] = oplata["lang"].fillna(0)
    oplata = oplata.dropna()\
        .replace(to_replace=r"^\s*(\S+)\s*$", value="\g<1>", regex=True)\
        .astype({"lang": "int", "apart": "int"})
    oplata["year"] = oplata["date"].apply(lambda x: x[-4:])
    oplata = oplata.sort_values(by=["user_id", "apart", "year", "month"])
    return oplata

def read_history():
    history = pd.read_csv("./history.txt", sep="\t", encoding="cp1251")\
        .replace(to_replace=r"^([-\d]+)[,](\d+)$", value="\g<1>.\g<2>", regex=True)\
        .drop(columns=["date", "pre"])
    history["user_id"] = history["user_id"].fillna("")
    history["lang"] = history["lang"].fillna(0)
    history = history.dropna()\
        .astype({"rent": "float32", "water": "float32", "electricity": "float32", "garbage": "float32",
                 "lang": "int", "year": "int", "month": "int", "apart": "int"})
    history["total"] = history["rent"] + history["water"] + history["electricity"] + history["garbage"]
    history = history.sort_values(by=["user_id", "apart", "year", "month"], ascending=[True, True, False, False])
    return history

def read_users():
    users = pd.read_csv("./users.txt", sep="\t", encoding="cp1251")
    return users

def check_user(user_id):
    users = read_users().query("user_id == '{}'".format(user_id)).dropna().reset_index()\
        .astype({"lang": "int", "apart": "int"})
    return users.loc[0] if users.shape[0] > 0 else None

def send(bot, chat_id, text, reply_markup=None):
    bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML", reply_markup=reply_markup)

def check_payments_user(user_id):
    users = pd.read_csv("./managers.txt", names=["user_id"], sep="\t", encoding="cp1251")\
        .query("user_id == '{}'".format(user_id)).reset_index()
    return users.loc[0] if users.shape[0] > 0 else None
