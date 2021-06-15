from lib import *
pd.options.mode.chained_assignment = None

df = read_date('data/schedule.csv')
df_staff = read_file('data/staff.csv')

df_upd = df.loc[df['timestamp'] >= np.datetime64('2021-06-14')]

# Очищаем места для бронирования
df_upd['staff'].loc[df_upd['staff'] == 'Бронирование'] = 'Free'


# Освобождаем понедельник


# Добавляем нового sl в понедельник
dates = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Wednesday']
for d in dates:
    insert_person(df_staff.loc[59], df_upd, d)

# Добавляем нового pr во вторник
dates = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Thursday']
for d in dates:
    insert_person(df_staff.loc[58], df_upd, d)

holidays([np.datetime64('2021-06-14')], df_upd)

# Все строки с Free в Бронирование
df_upd['staff'].loc[df_upd['staff'] == 'Free'] = 'Бронирование'

df['staff'].loc[df_upd.index] = df_upd.loc[:,'staff']
df.to_excel('data/upd_schedule.xlsx')



