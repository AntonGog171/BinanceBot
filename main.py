from binance.client import Client
import telebot
import margin_operations
import spot_operations
import notifications


TGtoken = "" #removed for privacy :)
key = ''
secret = ''
inputkey = False
inputsecret = False
bot = telebot.TeleBot(TGtoken)
client = Client()
user_ID = int()


@bot.message_handler(commands=['help'])
def helper(message):
	bot.send_message(message.from_user.id, disable_web_page_preview=True, text='/login - ввод своего public и secret ключей для Binance API\n'
																			   '/spot_balance - вывод всех валют на спотовом аккаунте\n'
																			   '/get_spot_asset <имя валюты сокращённо, подробнее: https://bit.ly/3wssA45> - вывод количества определённой валюты на спотовом аккаунте\n'
																			   '/isolated_margin_balance - вывод пар на изолированой марже\n'
																			   '/get_spot_orders_status - вывод всех ордеров на спотовом аккаунте\n'
																			   '/get_isl_margin_orders_status - вывод всех ордеров на изолированой марже')


@bot.message_handler(commands=['login'])
def login(message):
	global inputkey
	inputkey = True
	bot.send_message(user_ID, 'Enter public key:')


@bot.message_handler(commands=['start'])
def start(message):
	global user_ID
	user_ID = message.from_user.id
	bot.send_message(user_ID, 'Type /help for the list of commands')

@bot.message_handler(func=lambda x: inputkey)
def input_key(message):
	global inputkey
	inputkey = False
	global key
	key= message.text
	global inputsecret
	inputsecret = True
	bot.send_message(user_ID, 'Enter secret key:')


@bot.message_handler(func=lambda x: inputsecret)
def input_secret(message):
	global inputsecret
	inputsecret = False
	global secret
	secret = message.text
	global client
	client = Client(key, secret)
	notifications.start_notifications(bot_transfered=bot, client_transfered=client, key_transfered=key, secret_transfered=secret, used_ID_transfered=user_ID)



@bot.message_handler(commands=['spot_balance'])
def spot_balance(message):
	info = spot_operations.spot_balance(client)
	bot.reply_to(message, info)


@bot.message_handler(commands=['isolated_margin_balance'])
def isolated_margin_balance(message):
	info = margin_operations.isolated_margin_balance(client)
	bot.reply_to(message, info)


@bot.message_handler(regexp='[/get_spot_asset] [A-Z]+')
def get_spot_asset(message):
	asset = message.text[16:]
	info = spot_operations.get_spot_asset(asset, client=client)
	bot.reply_to(message, info)


@bot.message_handler(commands=['get_spot_orders_status'])
def get_spot_orders_status(message):
	info = notifications.get_spot_orders_status()
	bot.reply_to(message, info)


@bot.message_handler(commands=['get_isl_margin_orders_status'])
def get_isolated_margin_orders_status(message):
	info = notifications.get_isolated_margin_orders_status()
	bot.reply_to(message, info)


bot.infinity_polling()
