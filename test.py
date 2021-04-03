import pandas as pd
import numpy as np

def read_excel(path):
    return pd.read_excel(path, header=0, index_col=0)

def read_file(path):

    df = pd.read_csv(path, header=0, index_col=0, sep=';', encoding='cp1251')
    return df

def insert_staff(c_staff, day_of_week=[]):

    return


def sort_place(schedule):
    #Переносим "Бронирование" на последние места дня
    week = schedule['week'].unique()

    for w in week:
        days = schedule.loc[schedule['week'] == w, 'day_of_week'].unique()
        for d in days:
            rooms = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d), 'room'].unique()
            for r in rooms:
                places = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d)
                                      & (schedule['room'] == r), 'place'].unique()
                flag = True
                while flag:
                    flag = False
                    for p in places[:-1]:
                        s_1 = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d)
                                           & (schedule['place'] == p) & (schedule['room'] == r)]
                        s_2 = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) & (schedule['place'] == (p+1)) & (schedule['room'] == r)]
                        if s_1['staff'].values == 'Бронирование' and s_2['staff'].values != 'Бронирование':
                            schedule['staff'].loc[(schedule['week'] == w) & (schedule['day_of_week'] == d)
                                                  & (schedule['place'] == p) & (schedule['room'] == r)] = s_2['staff'].values
                            schedule['staff'].loc[(schedule['week'] == w) & (schedule['day_of_week'] == d)
                                                  & (schedule['place'] == (p+1)) & (schedule['room'] == r)] = 'Бронирование'
                            flag = True



staff = read_file('data/staff.csv')

# Все места в 421 заменяются на бронирование 12.04.2021, кроме Сулименко, Юдиной, Пикулевой, Чернецова, Юрченко
untouched_list = ['Пикулёва Екатерина', 'Сулименко Ирина', 'Сервис - менеджер', 'Чернецов Евгений']

schedule = read_excel('data/schedule.xlsx')

#Получаем все места в 421 кроме тех, кто в списке untouched_list
upd_421 = schedule.loc[(schedule['room'] == 421) & (schedule['timestamp'] >= np.datetime64('2021-04-12')) & (~schedule['staff'].isin(untouched_list))]

# Ставим на все места Free
upd_421.loc['staff'] = 'Free'

upd_421.loc[upd_421['place'] == 8] = 'Бронирование'

print(1)