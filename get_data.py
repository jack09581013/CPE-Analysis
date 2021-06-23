import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from colorama import Fore, Style

def get_my_dates():
    dates = ['2015-12-22', '2016-12-20', '2017-03-28', '2017-09-26', '2018-03-27']
    return pd.DataFrame([datetime.strptime(x, '%Y-%m-%d').date() for x in dates], columns=['Date'])

def get_all_dates():
    return pd.read_pickle('data/dates.pkl')

data = []
for d in get_all_dates()['Date']:
    res = requests.get('https://cpe.cse.nsysu.edu.tw/cpe/scoreboard/{}'.format(d))
    soup = BeautifulSoup(res.text, "html.parser")

    for e in soup.select('#scoreboard tr'):
        try:
            tds = [x.string for x in e.find_all('td')]
            row = [d,  int(tds[0]), str(tds[1]), str(tds[2]), int(tds[3]), int(tds[4])]
            data.append(row)
        except Exception as err:
            print(f'{Fore.RED}Invalid item: {tds}{Style.RESET_ALL}')
    print('Total number of rows:', len(data))

data = pd.DataFrame(data=data, columns=['Date', 'Order', 'School', 'Name', 'Score', 'Time'])
print(data)
data.to_pickle('data/data.pkl')

