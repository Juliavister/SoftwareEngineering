from db import connection
import db

# THE LATEST CURRENCY
cur = connection.cursor()
latest = []

# Query each table and retrieve the latest row
for table_name in ['USD', 'PLN', 'NOK', 'TL']:
    cur.execute(f"SELECT TOP 1 * FROM {table_name} ORDER BY theDate DESC")
    result = cur.fetchone()
    latest.append(result)

rates = {"EUR": 1, "USD": latest[0][0], "PLN": latest[1][0], "NOK": latest[2][0], "TRY": latest[3][0]}


# ALL DATA WITH THE DATES FOR THE GRAPH AND THE PREDICTION

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




cur.close()
connection.close()
