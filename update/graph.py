import matplotlib.pyplot as plt
import io
import db
from datetime import datetime, date


def send_currency_exchange_graph(cr):
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

    currencies = cr

    # Create a subplot for each currency if there is more than one currency
    if len(currencies) > 1:
        num_plots = len(currencies)
        fig, axes = plt.subplots(num_plots, 1, figsize=(12, 6 * num_plots), sharex=True)

        # Plot the exchange rates for each currency
        for i, currency in enumerate(currencies):
            rates = data[currency]['rates']
            dates = data[currency]['dates']
            dates = [datetime.strptime(str(d), '%Y-%m-%d').strftime('%m-%d') for d in dates]
            axes[i].plot(dates, rates, linewidth=2.0)
            axes[i].set_title(f'{currency} Exchange Rate')
            axes[i].set_ylabel('Exchange Rate')

        # Set the x-axis label
        axes[-1].set_xlabel('Date')

    # Otherwise, just plot the exchange rates for the single currency
    else:
        currency = currencies[0]
        rates = data[currency]['rates']
        dates = data[currency]['dates']
        dates = [datetime.strptime(str(d), '%Y-%m-%d').strftime('%m-%d') for d in dates]
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(dates, rates, linewidth=2.0)
        ax.set_title(f'{currency} Exchange Rate')
        ax.set_ylabel('Exchange Rate')
        ax.set_xlabel('Date')

    # Create a bytes buffer and save the graph to it
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Close the plot to free up memory
    plt.close()

    # Return the buffer
    return buf.getvalue()