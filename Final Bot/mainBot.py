import telebot
import BOT_KEY
import graph
import prediction
import data

bot = telebot.TeleBot(BOT_KEY.KEY)

# main menu keyboard creation
menu_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    telebot.types.KeyboardButton("Exchange"),
    telebot.types.KeyboardButton("Rates"),
    telebot.types.KeyboardButton("Graphs"),
    telebot.types.KeyboardButton("Prediction")
)

# takes keys from rates dictionary made in db.py file and uses them to create keys for currencies
currency_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    *[telebot.types.KeyboardButton(currency) for currency in data.rates.keys()]
)
graph_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    *[telebot.types.KeyboardButton(currency) for currency in data.rates.keys() if currency != "EUR"]
).add(
    telebot.types.KeyboardButton("None")
)

pred_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    *[telebot.types.KeyboardButton(currency) for currency in data.rates.keys()  if currency != "EUR"]
)


# used to start/reset bot
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome to the currency converter bot! Please select an option:",
                     reply_markup=menu_keyboard)


# after "Exchange" is either sent by a button click or manually user is asked question below
@bot.message_handler(func=lambda message: message.text == "Exchange")
def handle_exchange(message):
    bot.send_message(message.chat.id, "How much do you want to convert?")
    bot.register_next_step_handler(message, handle_exchange_amount)


# user gave a number, now this function sends a message asking [...] and showing a keyboard with currency codes
def handle_exchange_amount(message):
    amount = float(message.text)
    bot.send_message(message.chat.id,
                     f"From which currency do you want to convert {amount:.2f}? Please select from the options below:",
                     reply_markup=currency_keyboard)
    # passing all we got so far to the function below
    bot.register_next_step_handler(message, handle_exchange_source, amount)


# again a currency codes keyboard is shown, user picks one
def handle_exchange_source(message, amount):
    source_currency = message.text
    bot.send_message(message.chat.id,
                     f"What currency do you want to convert {amount:.2f} {source_currency} to? Please select from the options below:",
                     reply_markup=currency_keyboard)
    # and everything is passed to the function below
    bot.register_next_step_handler(message, handle_exchange_target, amount, source_currency)


# here all collected data is converted into what user will see in the end
def handle_exchange_target(message, amount, source_currency):
    target_currency = message.text
    conversion_rates = data.rates
    rate = conversion_rates[target_currency] / conversion_rates[source_currency]  # conversion rate is calculated here
    converted_amount = amount * rate
    # final response with converted value
    bot.send_message(message.chat.id,
                     f"{amount:.2f} {source_currency} is equivalent to {converted_amount:.2f} {target_currency}")
    # after the work is done user sees menu keys again so there's no need to use /start
    bot.send_message(message.chat.id, "What else can I help you with?", reply_markup=menu_keyboard)


# handling user picking "Rates" option and is shown a currency code keyboard, after clicking one function bellow is triggered
@bot.message_handler(func=lambda message: message.text == "Rates")
def handle_rates(message):
    bot.send_message(message.chat.id, "Please select the source currency:", reply_markup=currency_keyboard)
    bot.register_next_step_handler(message, handle_rates_source)


# user clicks a button for their target currency
def handle_rates_source(message):
    source_currency = message.text
    bot.send_message(message.chat.id, f"Please select the target currency for {source_currency}:",
                     reply_markup=currency_keyboard)
    bot.register_next_step_handler(message, handle_rates_target, source_currency)


# previous function sends both target and source here, this function calculates rate
def handle_rates_target(message, source_currency):
    target_currency = message.text
    conversion_rates = data.rates
    # here
    exchange_rate = conversion_rates[target_currency] / conversion_rates[source_currency]
    # and sends it to the chat
    bot.send_message(message.chat.id,
                     f"The exchange rate between {source_currency} and {target_currency} is {exchange_rate:.4f}")
    # and shows menu keyboard again
    bot.send_message(message.chat.id, "What else can I help you with?", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: message.text == "Graphs")
def handle_exchange(message):
    # bot.send_photo(chat_id=message.chat.id, photo=graph.send_currency_exchange_graph("X"))
    bot.send_message(message.chat.id, "What currency do you want to graph?", reply_markup=currency_keyboard)
    currency = []
    bot.register_next_step_handler(message, handle_graph_currencies, currency)


def handle_graph_currencies(message, currency):
    curr = message.text
    if curr != "No":
        if curr == "EUR":
            bot.send_message(message.chat.id, "Graphing for EUR is not available. Please choose another currency.", reply_markup=graph_keyboard)
            bot.register_next_step_handler(message, handle_graph_currencies, currency)
        else:
            currency.append(curr)
            bot.send_message(message.chat.id, "What other currency do you want to graph?", reply_markup=graph_keyboard)
            bot.register_next_step_handler(message, handle_graph_currencies, currency)
    else:
        bot.send_photo(chat_id=message.chat.id, photo=graph.send_currency_exchange_graph(currency))
        # and shows menu keyboard again
        bot.send_message(message.chat.id, "What else can I help you with?", reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: message.text == "Prediction")
def handle_predictions(message):
    bot.send_message(message.chat.id, "Predictions are EUR based, ")
    bot.send_message(message.chat.id, "Which currency do you want predictions about?", reply_markup=pred_keyboard)
    bot.register_next_step_handler(message, handle_currency_predictions)


def handle_currency_predictions(message):
    currency = message.text
    if currency == "EUR":
        bot.send_message(message.chat.id, "Predictions for EUR is not available. Please choose another currency.",reply_markup=pred_keyboard)
        bot.register_next_step_handler(message, handle_currency_predictions, currency)
    else:
        predictions = prediction.send_currency_predict(currency)
        bot.send_message(message.chat.id, f"Based on linear regression calculations {currency}/EUR will be {predictions:.2f} this week.")
        bot.send_message(message.chat.id, "What else can I help you with?", reply_markup=menu_keyboard)

# bot start
bot.polling()

# keys basically send set messages to the chat and message.text collects them and puts in variables, so they can be used
# that's why user can also just send a message manually and if for some reason keyboard doesn't show, if the message
# is correct everything will work if not it'll be just ignored until correct message is provided. What I used for buttons
# works only on mobile, stuff that theoretically should work both on mobile and web app doesn't work in neither of those
# places (and didn't work in class too) and this version looks nicer.
