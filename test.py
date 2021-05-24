import pandas as pd
import numpy as np
from lib import *
pd.options.mode.chained_assignment = None

df = read_date('data/schedule.csv')
df_staff = read_file('data/staff.csv')

df_upd = df.loc[df['timestamp'] >= np.datetime64('2021-05-17')]

# Очищаем все места кроме дежурной смены и сервис менеджеров
df_upd['staff'].loc[~df_upd['place'].isin(['Дежурная смена', 'Сервис - менеджер'])] = 'Free'
# ставим на первую неделю дежурную смену и сервис - менеджеров на четверг, пятницу

# сервис - менеджер в среду, четверг и пятницу
df_upd['staff'].loc[(df_upd['day_of_week'].isin(['Wednesday', 'Friday', 'Thursday'])) & (df_upd['room'] == 421) & (df_upd['place'] == 1)] = 'Сервис - менеджер'
df_upd['staff'].loc[(df_upd['room'] == 404) & (df_upd['place'] == 1)] = 'Дежурная смена'





# Чернецов и Прохоов каждый день.
days = df_upd['timestamp'].unique()
for d in days:
    insert_person(df_staff.loc[27], df_upd, d)
    insert_person(df_staff.loc[29], df_upd, d)


# Пикулева и Панкратов во вторник
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Tuesday'].unique()
for d in days:
    insert_person(df_staff.loc[28], df_upd, d)
    insert_person(df_staff.loc[8], df_upd, d)

#Норматов четверг
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Thursday'].unique()
for d in days:
    insert_person(df_staff.loc[14], df_upd, d)

#Старков среда
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Wednesday'].unique()
for d in days:
    insert_person(df_staff.loc[9], df_upd, d)


# Сейлы и пресейлы в среду в 404
sl_ps = df_staff.loc[df_staff['fg'].isin(['ps','sl'])]
sl_ps['room'] = 404
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Wednesday'].unique()
insert_group(sl_ps, days, df_upd)

# Инженеры эксплуатации во вторник
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Tuesday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'en'], days, df_upd)

# Архитекторы и продукты четверг
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Thursday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'ar'], days, df_upd)
insert_group(df_staff.loc[df_staff['fg'] == 'pr'], days, df_upd)

# Сервис менеджеры, платформенные, партнерские в понедельник
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Monday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'sm'], days, df_upd)
insert_group(df_staff.loc[df_staff['fg'] == 'psl'], days, df_upd)
insert_group(df_staff.loc[df_staff['fg'] == 'arp'], days, df_upd)

# Аналитиков и разрабов в пятницу
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Friday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'ba'], days, df_upd)
insert_group(df_staff.loc[df_staff['fg'] == 'dv'], days, df_upd)


# Остальных случайно
weeks = df_upd['week'].unique()
for w in weeks:
    t = df_upd['staff'].loc[df_upd['week'] == w].unique()
    staffs = df_staff.loc[~df_staff['staff'].isin(t)]
    days = df_upd['timestamp'].loc[df_upd['week'] == w].unique()
    for index, person in staffs.iterrows():
         random_insert_person(person, days, df_upd)


# Праздники
hol_days = [np.datetime64('2021-05-10')]
holidays(hol_days, df_upd)

# Все строки с Free в Бронирование
df_upd['staff'].loc[df_upd['staff'] == 'Free'] = 'Бронирование'

df['staff'].loc[df_upd.index] = df_upd.loc[:,'staff']
df.to_excel('data/upd_schedule.xlsx')



