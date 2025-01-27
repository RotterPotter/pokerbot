from bs4 import BeautifulSoup
import requests
import json

url = 'https://flopturnriver.com/poker-strategy/texas-holdem-expected-value-hand-charts-7-players-19151/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
table = table = soup.find('table')

rows = table.find_all('tr')
data = {}
positions = {
    1: "SB", 
    2: "BB", 
    3: "UTG", 
    4: "LJ", 
    5: "HJ", 
    6: "CO",
    7: "BTN"
}

for row in rows[3:]:
  cols = row.find_all(['td', 'th'])
  cols = ["".join(col.text.strip().split(" ")) for col in cols]
  print(cols)
  for index, position in positions.items():
    if data.get(cols[0], None) is None:
      data[cols[0]] = {}
    data[cols[0]][positions[index]] = cols[index]

with open(r'..\preflop_suggestions.json', "w") as f:   
  json.dump(data, f)