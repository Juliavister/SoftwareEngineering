import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

exchangerate_table = soup.find('table', {'class': 'forextable'})
#print(exchangerate_table)

currencies = {}

for row in exchangerate_table.find_all("tr"):
    cells = row.find_all("td")
    if len(cells) > 0:
        curr_name = cells[1].text.strip()

        if curr_name in ['Polish zloty', 'Turkish lira', 'Norwegian krone', 'US dollar']:
            rate = float(cells[2].text.strip())
            currencies[curr_name] = rate


for curr_name, rate in currencies.items():
    print(curr_name, rate)

#results = pd.DataFrame(rates)
#print(results)



