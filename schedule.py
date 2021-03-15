import pandas as pd
import random
import numpy as np


def read_date(path):

    df = pd.read_csv(path, header=0, parse_dates=['timestamp'], dayfirst=True, sep=';', encoding='cp1251')
    return df

def read_file(path):

    df = pd.read_csv(path, header=0, index_col=0, sep=';', encoding='cp1251')
    return df

def staff_condition(p):
    """
    Функция, подставляющая значения условия в соответствующую строку
    """
    t = staff.loc[(staff['staff'] == p['staff']), 'a']
    return t



def randon_staff(staff, schedule, week):
    """
    Формируется случайный список фамилий для распределения
    :param staff:
    :param room:
    :return:
    """

    sch_staff = np.unique(schedule.loc[(schedule['week'] == week) & (schedule['staff'] != 'Free'), 'staff'].values)
    staff = staff.loc[~staff['staff'].isin(sch_staff)].sample(frac=1).reset_index(drop=True)

    return staff

def condition_sum(schedule, condition, cond_colum):
    room = schedule['room'].unique()
    week = schedule['week'].unique()

    t = pd.DataFrame(columns=['room', 'week', 'day_of_week', 'sum_a'])
    for r in room:
        for w in week:
            day = schedule.loc[schedule['week'] == w ,'day_of_week'].unique()
            for d in day:
                q = pd.Series([r, w, d, schedule[(schedule['room'] == r) & (schedule['week'] == w) & (schedule['day_of_week'] == d)].a.sum()], index=t.columns)
                t = t.append(q, ignore_index=True)
    return t



def weekly_allocation(staff, schedule):
    """
    В рамках функции сформируется дата фрейм, случайно распределяющий нераспределенный на неделю персонал на свободные места в этой неделе.
    """
    #Для каждой недели присваеваем свободным местам фамилии людей, для которых еще не забранированы места
    for w in schedule['week'].unique():
        r_staff = randon_staff(staff, schedule, w)
        for r in np.unique(r_staff['room']):
            staff_r = r_staff.loc[r_staff['room'] == r]
            count_free_place = schedule.loc[(schedule['week'] == w) & (schedule['staff'] == 'Free') & (schedule['room'] == r), 'staff'].count()

            if staff_r['staff'].count() < count_free_place:
                t = pd.DataFrame(np.repeat([['Бронирование',r, 0]], count_free_place - staff_r['staff'].count(), axis=0), columns=staff_r.columns)
                staff_r = pd.concat([staff_r, t], ignore_index=True)

            schedule.loc[(schedule['week'] == w) & (schedule['staff'] == 'Free') & (schedule['room'] == r), 'staff'] = staff_r.iloc[:count_free_place,0].values


#Определение переменных
place_number_1 = 8
place_number_2 = 8


#Подготовка датафрема для расписания
path = 'data/date.csv'
schedule = read_date(path)
schedule['month'] = schedule['timestamp'].dt.month_name()
schedule['week'] = schedule['timestamp'].dt.isocalendar().week
schedule['day_of_week'] = schedule['timestamp'].dt.day_name()
schedule['room'] = 404
schedule['place'] = 1
schedule_1 = schedule.copy()
schedule_1.loc[:,'room'] = 421


schedule = pd.concat([schedule, schedule_1], ignore_index=True)
schedule['staff'] = 'Free'




dates = list(set(schedule['timestamp'].to_list()))
for d in dates:
    t = schedule.loc[(schedule['room'] == 404) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_1-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_1-1):
        t.loc[i,'place'] = i + 2


    schedule = pd.concat([schedule, t], ignore_index=True)
    t = schedule.loc[(schedule['room'] == 421) & (schedule['timestamp'] == d)].copy()
    t = pd.DataFrame(np.repeat(t.values, place_number_2-1, axis=0), columns=t.columns).astype(t.dtypes)

    for i in range(place_number_2-1):
        t.loc[i,'place'] = i + 2

    schedule = pd.concat([schedule, t], ignore_index=True)



#Бронирование одного места за дежурной сменой и сервис - менеджерами
schedule['staff'].loc[(schedule['room'] == 404) & (schedule['place'] == 1)] = 'Дежурная смена'
schedule['staff'].loc[(schedule['room'] == 421) & (schedule['place'] == 1)] = 'Сервис - менеджер'

#Бронирование свободных мест каждый день
schedule['staff'].loc[schedule['place'] == 8] = 'Бронирование'

#Бронирование свободных мест в пятницу
schedule['staff'].loc[(schedule['day_of_week'] == 'Friday') & (schedule['staff'] == 'Free')] = 'Бронирование'




staff = read_file('data/staff.csv')
condition = read_file('data/condition.csv')


#Чернецова и Пикулеву на понедельник, вторник
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Чернецов Евгений']['room'].values[0]) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 2)] = 'Чернецов Евгений'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Пикулёва Екатерина']['room'].values[0]) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 1)] = 'Пикулёва Екатерина'

#Юдину и Сулименко на среду
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Сулименко Ирина']['room'].values[0]) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 1)] = 'Сулименко Ирина'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Юдина Иветта']['room'].values[0]) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 2)] = 'Юдина Иветта'



condition_base = pd.DataFrame(schedule[['room','week', 'day_of_week']], columns=['room', 'week', 'day_of_week'])
condition_base['a'] = 0



schedule_temp =  schedule.copy()
schedule_temp['a'] = 0

weekly_allocation(staff, schedule_temp)
#apply возвращая соответсвующее значение из другого датафрейма.
schedule_temp['a'] = schedule_temp['staff'].apply(staff_condition, axis=1)

schedule_temp = schedule_temp.merge(staff[['staff','a']],how='left', on='staff')
schedule_temp.fillna(0, inplace=True)
schedule_temp['a'] = schedule_temp['a_y']
schedule_temp.drop(columns=['a_x', 'a_y'], inplace=True)

condition_new = condition_base.copy()
condition_new = condition_sum(schedule_temp, condition_new, ['a'])

print(schedule_temp)



schedule.to_excel('data/schedule.xlsx')









