import telebot
from binance.client import Client
import threading
import time

first_spot_update = True
first_isolated_margin_update = True
bot = telebot
client = Client()
old_spot_status_info = 'All orders are completed.'
old_isolated_margin_status_info = 'All orders are completed'


class Notification(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        while True:
            if secret != "":
                update_spot_status()
                update_isolated_margin_status()
            time.sleep(5)


def start_notifications(bot_transfered, client_transfered, key_transfered, secret_transfered, used_ID_transfered):
    global bot
    bot = bot_transfered
    global client
    client = client_transfered
    global key
    key = key_transfered
    global secret
    secret = secret_transfered
    global user_ID
    user_ID = used_ID_transfered
    spot_notification = Notification(1, "Notification")
    spot_notification.start()


def update_spot_status():
    orders = client.get_open_orders()
    info = ""
    for i in orders:
        info += f'{i["symbol"]}. '
        info += f'Side: {i["side"]}. '
        info += f'Type: {i["type"]}. '

        if i['type'] == 'STOP-LIMIT':
            info += f'Stop: {i["stopPrice"]}. '

        info += f'Limit: {i["price"]}. '
        info += f'Quantity: {i["origQty"]}.\n'

    global old_spot_status_info
    global first_spot_update
    if info == '':
        info = 'All orders are completed.'
    if info != old_spot_status_info:
        if not first_spot_update:
            bot.send_message(user_ID, 'Updated spot orders:\n' + info)
        else:
            first_spot_update = False
        old_spot_status_info = info


def get_spot_orders_status():
    return old_spot_status_info


def update_isolated_margin_status():
    accinfo=client.get_isolated_margin_account()
    info=''
    for i in accinfo['assets']:
        if float(i["baseAsset"]["totalAsset"]) + float(i["quoteAsset"]["totalAsset"]) == 0:
            continue

        symbol = str(i['baseAsset']['asset']) + str(i['quoteAsset']['asset'])
        magrin_infos = client.get_open_margin_orders(symbol=symbol, isIsolated=True)
        for magrin_info in magrin_infos:# тут массив на 1 элемент, цикл чисто как костыль
            pair_info = symbol + '. '
            pair_info += f'Side: {magrin_info["side"]}. '
            pair_info += f'Type: {magrin_info["type"]}. '

            if magrin_info['type'] == 'STOP-LIMIT':
                info += f'Stop: {magrin_info["stopPrice"]}. '

            pair_info += f'Limit: {magrin_info["price"]}. '
            pair_info += f'Quantity: {magrin_info["origQty"]}.\n'
            info += pair_info

    global first_isolated_margin_update
    global old_isolated_margin_status_info

    if info == '':
        info = 'All orders are completed.'
    if info != old_isolated_margin_status_info:
        if not first_isolated_margin_update:
            bot.send_message(user_ID, 'Updated isolated margin orders:\n' + info)
        else:
            first_isolated_margin_update = False
        old_isolated_margin_status_info = info


def get_isolated_margin_orders_status():
    return old_isolated_margin_status_info
