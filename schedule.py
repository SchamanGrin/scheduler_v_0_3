import pandas as pd
import random
import numpy as np


def read_date(path):

    df = pd.read_csv(path, header=0,
                     names=['id','timestamp'], parse_dates=['timestamp'], dayfirst=True, sep=';', encoding='cp1251')
    return df

def read_staff(path):

    df = pd.read_csv(path, header=0, index_col=0,
                     names=['id','staff'], sep=';', encoding='cp1251')
    return df

def randon_staff(staff):
    random.shuffle(staff)
    for str in staff:
        yield str


def weekly_allocation(staff_list, room, schedule):
    weeks_end = schedule['week'][schedule['room'] == room].max()
    weeks_start = schedule['week'][schedule['room'] == room].min()
    place_count = schedule['place'][schedule['room'] == room].max()
    for i in range(weeks_start, weeks_end):
        free_place = schedule.loc[(schedule['room'] == room) & (schedule['week'] == i) & (schedule['place'] != place_count)
                                           & (schedule['staff'] == 'Бронирование') & (schedule['day_of_week'] != 'Friday') ]

        staff_in_schedule = schedule['staff'].loc[(schedule['room'] == room) & (schedule['week'] == i)
                                                  & (schedule['staff'] != 'Бронирование')].to_list()
        staff_list = list(set(staff_list) - set(staff_in_schedule))
        staf_iter = randon_staff(staff_list)
        for place in free_place.index:
            try:
                schedule.loc[place, 'staff'] = next(staf_iter)
            except Exception as e:
                break


    print()

#Определение переменных
place_number_1 = 8
place_number_2 = 8


#Подготовка датафрема для расписания
path = 'data/work days.csv'
schedule = read_date(path)
schedule['month'] = schedule['timestamp'].dt.month_name()
schedule['week'] = schedule['timestamp'].dt.isocalendar().week
schedule['day_of_week'] = schedule['timestamp'].dt.day_name()
schedule['room'] = 1
schedule_1 = schedule.copy()
schedule_1.loc[:,'room'] = 2


schedule = pd.concat([schedule, schedule_1], ignore_index=True)
schedule['place'] = 1
schedule['staff'] = 'Бронирование'

#Составление расписания
schedule['staff'].loc[(schedule['room'] == 1) & (schedule['place'] == 1)] = 'Дежурная смена'
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['place'] == 1)] = 'Сервис - менеджер'

dates = list(set(schedule['timestamp'].to_list()))
for d in dates:
    t = schedule.loc[(schedule['room'] == 1) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_1-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_1-1):
        t.loc[i,'place'] = i + 2

    t.loc[:,'staff'] = 'Бронирование'
    schedule = pd.concat([schedule, t], ignore_index=True)
    t = schedule.loc[(schedule['room'] == 2) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_2-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_2-1):
        t.loc[i,'place'] = i + 2
    t.loc[:,'staff'] = 'Бронирование'
    schedule = pd.concat([schedule, t], ignore_index=True)



room_1 = read_staff('data/room_1.csv')
room_2 = read_staff('data/room_2.csv')

#Чернецова и Пикулеву на понедельник, вторник
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 2)] = 'Чернецов Евгений'
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 1)] = 'Пикулёва Екатерина'

#Юдину и Сулименко на среду
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 1)] = 'Сулименко Ирина'
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 2)] = 'Юдина Иветта'



room_1['staff'].to_list()


weekly_allocation(room_1['staff'].to_list(),1,schedule)
weekly_allocation(room_2['staff'].to_list(),2,schedule)

schedule.drop(columns=['id'], inplace=True)
schedule.to_excel('schedule.xlsx')









