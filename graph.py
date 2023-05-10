import matplotlib.pyplot as plt
import io
import db
import telegram
from datetime import datetime, date


def send_currency_exchange_graph(bot_token, chat_id):
    # Retrieve the data from the database
    db.cursor.execute("""
        SELECT 'USD' as currency, Rate, theDate FROM USD
        UNION ALL
        SELECT 'NOK' as currency, Rate, theDate FROM NOK
        UNION ALL
        SELECT 'TRY' as currency, Rate, theDate FROM TL
        UNION ALL
        SELECT 'PLN' as currency, Rate, theDate FROM PLN
        ORDER BY theDate ASC
    """)
    results = db.cursor.fetchall()

    # Store the data in a dictionary
    data = {}
    for row in results:
        currency = row[0]
        rate = row[1]
        date = row[2]
        if currency not in data:
            data[currency] = {'rates': [], 'dates': []}
        data[currency]['rates'].append(rate)
        data[currency]['dates'].append(date)

    # Specify the currency to graph
    currency = 'USD'

    # Extract the rates and dates for the specified currency
    rates = data[currency]['rates']
    dates = data[currency]['dates']

    # Convert the dates from strings to datetime objects and format them to 'MM-DD'
    dates = [datetime.strptime(str(d), '%Y-%m-%d').strftime('%m-%d') for d in dates]

    # Create a line graph of currency rates over time
    plt.plot(dates, rates)

    # Set the title and axis labels
    plt.title(f'{currency} Exchange Rate')
    plt.xlabel('Date')
    plt.ylabel('Exchange Rate')

    # Save the graph to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Initialize the Telegram bot
    bot = telegram.Bot(token=bot_token)

    # Send the graph to the bot
    bot.send_photo(chat_id=chat_id, photo=buf)

    # Close the database connection
    db.cursor.close()
    db.connection.close()
