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

    currencies = ['USD', 'TRY', 'NOK']

    # Create a subplot for each currency
    num_plots = len(currencies)
    fig, axes = plt.subplots(num_plots, 1, figsize=(12, 6*num_plots), sharex=True)

    # Plot the exchange rates for each currency
    for i, currency in enumerate(currencies):
        rates = data[currency]['rates']
        dates = data[currency]['dates']
        axes[i].plot(dates, rates, linewidth=2.0)
        axes[i].set_title(f'{currency} Exchange Rate')
        axes[i].set_ylabel('Exchange Rate')

    # Set the x-axis label
    axes[-1].set_xlabel('Date')

    # Show the graph
    plt.show()

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
