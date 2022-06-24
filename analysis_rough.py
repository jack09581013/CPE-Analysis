import pandas as pd
import numpy as np
from datetime import datetime

select_indexes = [0, 1, 2, 3, 4]
my_dates = ['2015-12-22', '2016-12-20', '2017-03-28', '2017-09-26', '2018-03-27']
order = [155, 90, 65, 80, 102]
# schools = ['臺大', '清大', '交大', '成大', '中央', '中興', '中山', '中正', '逢甲']
schools = ['臺大電機', '清大電機', '交大電機', '成大電機', '臺大資工', '清大資工', '交大資工', '成大資工', '中央資工', '中興資工', '中山資工', '中正資工', '逢甲資工']
data = pd.read_pickle('data/data.pkl')

print('Number of people included:', len(data))

for school in schools:
    PRs = []
    count = 0
    for select_index in select_indexes:
        select_date = datetime.strptime(my_dates[select_index], '%Y-%m-%d').date()
        select_data = data[(data['Date'] == select_date) & (data['School'].str.contains(school))].sort_values('Order')
        if len(select_data) > 0:
            order_in_select = (select_data['Order'] > order[select_index]).sum() / len(select_data)
            PR = int(order_in_select * 100)
            PRs.append(PR)
            count += len(select_data)

        # print('PR = {:.0f} ({})'.format(PR, order[select_index]))
        # print(select_data)
        # print()
    if len(PRs) > 0:
        PRs = np.array(PRs, dtype='int32')
        # PR for certain school in distinct dates
        print('[{} {}] PRs = {}, avg = {}'.format(school, count, PRs, PRs.mean()))
    else:
        print('[{}] No Data'.format(school))

print('Average PR: ', PRs.mean())