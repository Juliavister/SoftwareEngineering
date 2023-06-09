
import requests
from bs4 import BeautifulSoup
import datetime
import db

# Set up connection to Azure SQL Database
# in the db.py file

# Parse the website and extract exchange rates
url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

exchangerate_table = soup.find('table', {'class': 'forextable'})

date_element = soup.find('div', {'class': 'content-box'})
unwanted_sentence = date_element.find('p', string='All currencies quoted against the euro (base currency)')
if unwanted_sentence is not None:
    unwanted_sentence.decompose()
date_string = date_element.text.strip()

currencies = {'date': date_string}
for row in exchangerate_table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        curr_name = cells[1].text.strip()

        if curr_name in ['Polish zloty', 'Turkish lira', 'Norwegian krone', 'US dollar']:
            rate = float(cells[2].text.strip())
            currencies[curr_name] = rate

# Insert data into the database
date_obj = datetime.datetime.strptime(date_string, '%d %B %Y')
formatted_date = date_obj.strftime('%Y-%m-%d')

table_names = {
    'US dollar': 'USD',
    'Norwegian krone': 'NOK',
    'Turkish lira': 'TL',
    'Polish zloty': 'PLN',
}
for curr_name, rate in currencies.items():
    if curr_name != 'date' and curr_name in table_names:
        table_name = table_names[curr_name]
        sql = f"""MERGE INTO {table_name} AS t
                  USING (VALUES ('{formatted_date}', {rate})) AS s(theDate, Rate)
                  ON t.theDate = s.theDate
                  WHEN MATCHED THEN
                    UPDATE SET t.Rate = s.Rate
                  WHEN NOT MATCHED THEN
                    INSERT (theDate, Rate) VALUES (s.theDate, s.Rate);"""
        db.cursor.execute(sql)


db.cnxn.commit()



# Close the database connection
db.cursor.close()
db.cnxn.close()
