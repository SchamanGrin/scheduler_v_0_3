import pandas as pd
import numpy as np
from lib import *
pd.options.mode.chained_assignment = None

df = read_date('data/schedule.csv')
df_staff = read_file('data/staff.csv')

df_upd = df.loc[df['timestamp'] >= np.datetime64('2021-05-11')]

# Очищаем все места кроме дежурной смены и сервис менеджеров
df_upd['staff'].loc[~df_upd['place'].isin(['Дежурная смена', 'Сервис - менеджер'])] = 'Free'
# ставим на первую неделю дежурную смену и сервис - менеджеров на четверг, пятницу

# сервис - менеджер в среду, четверг и пятницу
df_upd['staff'].loc[(df_upd['day_of_week'].isin(['Wednesday', 'Friday', 'Thursday'])) & (df_upd['room'] == 421) & (df_upd['place'] == 1)] = 'Сервис - менеджер'
df_upd['staff'].loc[(df_upd['room'] == 404) & (df_upd['place'] == 1)] = 'Дежурная смена'
df_upd['staff'].loc[(df_upd['day_of_week'] == 'Tuesday') & (df_upd['room'] == 404) & (df_upd['place'] == 1)] == df_staff['staff'].loc[28]

# 10го только дежурная смена
df['staff'].loc[(df['timestamp'] == np.datetime64('2021-05-11')) & (df['staff'] != 'Дежурная смена')] = 'Бронирование'


# Чернецов и Прохоов каждый день.
days = df_upd['timestamp'].unique()
for d in days:
    insert_person(df_staff.loc[27], df_upd, d)
    insert_person(df_staff.loc[29], df_upd, d)

# Сейлы и пресейлы во вторник
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Tuesday'].unique()
insert_group(df_staff.loc[df_staff['fg'].isin(['ps','sl'])], days, df_upd)

# Инженеры эксплуатации в среду
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Wednesday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'en'], days, df_upd)

# Архитекторы и продукты четверг
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Thursday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'ar'], days, df_upd)
insert_group(df_staff.loc[df_staff['fg'] == 'pr'], days, df_upd)

# Сервис менеджеры понедельник
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Monday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'sm'], days, df_upd)

# Аналитиков в пятницу
days = df_upd['timestamp'].loc[df_upd['day_of_week'] == 'Friday'].unique()
insert_group(df_staff.loc[df_staff['fg'] == 'ba'], days, df_upd)

# Разрабов где поместятся
weeks = df_upd['week'].unique()
random_insert_group(df_staff.loc[df_staff['fg'] == 'dv'], weeks, df_upd)

# Панкратова не в среду
for w in weeks:
    days = df_upd['timestamp'].loc[(df_upd['day_of_week'] != 'Wednesday') & (df_upd['week'] == w)].unique()
    random_insert_person(df_staff.loc[8], days, df_upd)

# Остальных случайно
"""for w in weeks:
    t = df_upd['staff'].loc[df_upd['week'] == w].unique()
    staffs = df_staff.loc[~df_staff['staff'].isin(t)]
    days = df_upd['timestamp'].loc[df_upd['week'] == w].unique()
    for person in staffs:
        print(person)
        #random_insert_person(person, days, df_upd)"""


# Все строки с Free в Бронирование
df_upd['staff'].loc[df_upd['staff'] == 'Free'] = 'Бронирование'

df['staff'].loc[df_upd.index] = df_upd.loc[:,'staff']
df.to_excel('data/upd_schedule.xlsx')



