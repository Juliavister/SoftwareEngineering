import requests
from bs4 import BeautifulSoup


url = 'https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

exchangerate_table = soup.find('table', {'class': 'forextable'})
#print(exchangerate_table)

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


for curr_name, rate in currencies.items():
    print(curr_name, rate)
#instead of printing --> connect to a database





