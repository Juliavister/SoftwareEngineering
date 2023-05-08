import matplotlib.pyplot as plt
import io
import db

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




# Convert the dates from strings to datetime objects

# Create a line graph of currency rates over time
plt.plot(dates, rates)

# Set the title and axis labels
plt.title(f'{currency} Exchange Rate')
plt.xlabel('Date')
plt.ylabel('Exchange Rate')

# Display the graph
plt.show()

# Save the graph to a bytes buffer
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)

# Initialize the Telegram bot
#bot_token = 'your_bot_token_here'
# chat_id = 'your_chat_id_here'
# bot = telegram.Bot(token=bot_token)

# Send the graph to the bot
# bot.send_photo(chat_id=chat_id, photo=buf)