import pandas as pd
import random
import numpy as np


def read_date(path):

    df = pd.read_csv(path, header=0, parse_dates=['timestamp'], dayfirst=True, sep=';', encoding='cp1251')
    return df

def read_file(path):

    df = pd.read_csv(path, header=0, index_col=0, sep=';', encoding='cp1251')
    return df

def randon_staff(staff, room):
    """
    Формируется случайный список фамилий для распределения
    :param staff:
    :param room:
    :return:
    """
    return




def weekly_allocation(staff_list, schedule):
    """
    В рамках функции сформируется дата фрейм, случайно распределяющий нераспределенный на неделю персонал на свободные места в этой неделе.
    """
    return


#Определение переменных
place_number_1 = 8
place_number_2 = 8


#Подготовка датафрема для расписания
path = 'data/work days.csv'
schedule = read_date(path)
schedule['month'] = schedule['timestamp'].dt.month_name()
schedule['week'] = schedule['timestamp'].dt.isocalendar().week
schedule['day_of_week'] = schedule['timestamp'].dt.day_name()
schedule['room'] = 404
schedule_1 = schedule.copy()
schedule_1.loc[:,'room'] = 421


schedule = pd.concat([schedule, schedule_1], ignore_index=True)
schedule['staff'] = 'Free'




dates = list(set(schedule['timestamp'].to_list()))
for d in dates:
    t = schedule.loc[(schedule['room'] == 1) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_1-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_1-1):
        t.loc[i,'place'] = i + 2


    schedule = pd.concat([schedule, t], ignore_index=True)
    t = schedule.loc[(schedule['room'] == 2) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_2-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_2-1):
        t.loc[i,'place'] = i + 2

    schedule = pd.concat([schedule, t], ignore_index=True)



#Бронирование одного места за дежурной сменой и сервис - менеджерами
schedule['staff'].loc[(schedule['room'] == 1) & (schedule['place'] == 1)] = 'Дежурная смена'
schedule['staff'].loc[(schedule['room'] == 2) & (schedule['place'] == 1)] = 'Сервис - менеджер'

#Бронирование свободных мест каждый день
schedule['staff'].loc[schedule['place'] == 8] = 'Бронирование'

#Бронирование свободных мест в пятницу
schedule['staff'].loc[(schedule['day_of_week'] == 'Friday') & (schedule['staff'] == 'Free')] = 'Бронирование'




staff = read_file('data/staff.csv')
condition = read_file('data/condition.csv')


#Чернецова и Пикулеву на понедельник, вторник
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Чернецов Евгений']['room'].values) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 2)] = 'Чернецов Евгений'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Пикулёва Екатерина']['room'].values) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 1)] = 'Пикулёва Екатерина'

#Юдину и Сулименко на среду
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Сулименко Ирина']['room'].values) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 1)] = 'Сулименко Ирина'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Юдина Иветта']['room'].values) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 2)] = 'Юдина Иветта'



a_condition = pd.DataFrame(schedule['week'].unique())
a_condition['a'] = 0
weekly_allocation(staff['staff'].to_list(), schedule)




schedule.drop(columns=['id'], inplace=True)
schedule.to_excel('data/schedule.xlsx')









