import pandas as pd
import numpy as np
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

select_indexes = [1, 2, 3, 4]
my_dates = ['2015-12-22', '2016-12-20', '2017-03-28', '2017-09-26', '2018-03-27']
all_dates = pd.read_pickle('data/dates.pkl')
order = [155, 90, 65, 80, 102]
# schools = ['臺大', '清大', '交大', '成大', '中央', '中興', '中山', '中正', '逢甲', '輔仁']
schools = ['臺大電機', '清大電機', '交大電機', '成大電機', '臺大資工', '清大資工', '交大資工', '成大資工', '中央資工', '中興資工', '中山資工', '中正資工', '逢甲資工']
data = pd.read_pickle('data/data.pkl')

print('Number of dates included:', len(all_dates))
print('Number of people included:', len(data))

PRs = []
for select_index in select_indexes:
    select_date = datetime.strptime(my_dates[select_index], '%Y-%m-%d').date()
    select_data = data[data['Date'] == select_date]
    if len(select_data) > 0:
        order_in_select = (select_data['Order'] > order[select_index]).sum() / len(select_data)
        PR = order_in_select * 100
        PRs.append(PR)

avg_PR = np.array(PRs).mean()

print('My PRs:', PRs)
print('Average PR:', avg_PR)
print()

for school in schools:
    result = []
    for select_date in all_dates['Date']:
        select_data = data[(data['Date'] == select_date) & (data['School'].str.contains(school))]
        total = len(data[data['Date'] == select_date])
        if len(select_data) > 0:
            select_PRs = (1 - select_data['Order']/total)*100
            win_count = (select_PRs < avg_PR).sum()
            PR_in_select = int(win_count / len(select_data) * 100)
            count = len(select_data)
            result.append([PR_in_select, count, win_count])

    if len(PRs) > 0:
        result = pd.DataFrame(result, columns=['PR', 'Count', 'WinCount'], dtype='int32')
        # PR for certain school in distinct dates
        avg_PR_school = int(result['WinCount'].sum() / result['Count'].sum() * 100)
        print('[{} {}] Avg PR = {}'.format(school, result['Count'].sum(),  avg_PR_school))
        print(result.T)
    else:
        print('[{}] No Data'.format(school))
    print()

