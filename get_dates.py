import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


res = requests.get('https://cpe.cse.nsysu.edu.tw/history.php')
soup = BeautifulSoup(res.text, "html.parser")

dates = []

for e in soup.select('table.mtable tr'):
    try:
        date_td = e.find_all('td')[0].string
        dates.append(datetime.strptime(date_td, '%Y/%m/%d').date())
    except Exception as err:
        print(err)

dates = pd.DataFrame(dates, columns=['Date'])
dates.to_pickle('data/dates.pkl')

print(dates)