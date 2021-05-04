import pandas as pd
import numpy as np
import random


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




def weekly_condition(staff, schedule, condition, week):
    cond_list = staff[staff[condition] == condition].index
    room = staff.loc[staff[condition] == condition, 'room'].unique()
    #week = schedule['week'].unique()

    for w in week:
        #Находим все уникальные дни недели
        days = schedule.loc[schedule['week'] == w, 'day_of_week'].unique()
        #Перемешиваем их
        np.random.shuffle(days)

        #Для каждого дня
        for d in days:
            #Получаем список свободных мест в дне
            df_days = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) &
                                   (schedule['staff'] == 'Free') & (schedule['room']).isin(room)]


            # Для каждой комнаты количество свободных мест больше или равно количеству персонала, который надо посадить
            # по условию
            flag = []
            for r in room:
                t_1 = len(df_days[df_days['room'] == r])
                t_2 = len(staff.loc[(staff[condition] == condition) & (staff['room'] == r), 'staff'])
                tf = t_1 >= t_2
                flag.append(len(df_days[df_days['room'] == r]) >= len(staff.loc[staff[condition] == condition, 'staff']))
            #И если список свободных мест в этот день этой недели больше чем количество сотрудников
            if False not in flag:
                #Для каждого сотрудника из списка
                for pers_id in cond_list:
                    #Получаем соответствующий по номеру элемент из списка фамилий
                    person = staff.loc[pers_id, 'staff']
                    person_room = staff.loc[pers_id, 'room']
                    #Ищем первое свободное место
                    place = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) &
                                         (schedule['room'] == person_room) & (schedule['staff'] == 'Free'), 'place'].values[0]

                    #И присваеваем фамилию этому рабочему месту
                    schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) &
                                 (schedule['room'] == person_room) & (schedule['place'] == place), 'staff'] = person
                #Завершаем цикл для недели
                break


def weekly_allocation(df_staff, df_schedule):
    """
    В рамках функции сформируется дата фрейм, случайно распределяющий нераспределенный на неделю персонал на свободные места в этой неделе.
    """
    #Для каждой недели присваеваем свободным местам фамилии людей, для которых еще не забранированы места
    for w in df_schedule['week'].unique():
        rooms = randon_staff(df_staff, df_schedule, w)
        for r in np.unique(rooms['room']):
            df_room = df_schedule[(df_schedule['room'] == r) & (df_schedule['staff'] == 'Free')]
            df_week = df_room[(df_room['week'] == w)]
            if df_week.empty:
                continue
            days = np.unique(df_week['day_of_week'])
            for dw in days:
                staff_r = randon_staff(df_staff[df_staff['room'] == r], df_room, w)
                df_place = df_week[df_week['day_of_week'] == dw]
                if df_place.empty:
                    continue
                place = df_place.place.min()
                df_room.staff.loc[(df_room['day_of_week'] == dw) & (df_room['place'] == place)] = \
                    staff_r['staff'].iloc[0] if staff_r['staff'].count() > 0 else 'Бронирование'

            for i in df_room.index:
                df_schedule.staff.loc[i] = df_room.staff.loc[i]
            pass




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
#condition = read_file('data/condition.csv')


#Чернецова и Пикулеву на понедельник, вторник
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Чернецов Евгений']['room'].values[0]) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 2)] = 'Чернецов Евгений'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Пикулёва Екатерина']['room'].values[0]) & (schedule['day_of_week'].isin(['Monday', 'Tuesday'])) & (schedule['place'] == 1)] = 'Пикулёва Екатерина'

#Юдину и Сулименко на среду
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Сулименко Ирина']['room'].values[0]) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 1)] = 'Сулименко Ирина'
schedule['staff'].loc[(schedule['room'] == staff[staff['staff'] == 'Юдина Иветта']['room'].values[0]) & (schedule['day_of_week'].isin(['Wednesday'])) & (schedule['place'] == 2)] = 'Юдина Иветта'

week = schedule['week'].unique()
#Разработчиков и Вилянского вместе
weekly_condition(staff,schedule,'a',week)


"""cond_a_list = staff[staff['a'] == 'a'].index
room = staff.loc[staff['a'] == 'a', 'room'].unique()
week = schedule['week'].unique()
#Для каждой недели
for w in week:
    #Находим все уникальные дни недели
    days = schedule.loc[schedule['week'] == w, 'day_of_week'].unique()
    #Перемешиваем их
    np.random.shuffle(days)

    #Для каждого дня
    for d in days:
        #Получаем список свободных мест в дне
        df_days = schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) &
                               (schedule['staff'] == 'Free') & (schedule['room']).isin(room)]
        l = len(df_days)
        #И если список свободных мест в этот день этой недели больше чем количество разработчиков
        if l >= len(cond_a_list):
            #Получаем номера свободных мест
            place = df_days['place'].values
            #Для каждого элемента из списка рабочих мест
            for i in range(l):
                #Получаем соответствующий по номеру элемент из списка фамилий
                person = staff.loc[cond_a_list[i], 'staff']
                person_room = staff.loc[cond_a_list[i], 'room']
                #И присваеваем фамилию рабочему месту
                schedule.loc[(schedule['week'] == w) & (schedule['day_of_week'] == d) &
                           (schedule['room'] == person_room) & (schedule['place'] == place[i]), 'staff'] = person
            #Завершаем цикл для недели
            break"""



#Пресейлов, сейлов и Слюсаерва раз в две недели
# В первю неделю в любые дни [Ескин, Прохоров, Шаповалов], [Иноземцев, Круть, Черняев]
w1 = week[::2]
weekly_condition(staff, schedule, 'b', w1)
weekly_condition(staff, schedule, 'c', w1)

# Во вторую неделю Ескин, Слюсарев, Сугробов, Круть, Лобов
w2 = week[1::2]
weekly_condition(staff, schedule, 'd', w2)

# Случайно заполняем оставшиеся места
weekly_allocation(staff, schedule)

"""#apply возвращая соответсвующее значение из другого датафрейма.
schedule_temp =  schedule.copy()
schedule_temp['a'] = 0
schedule_temp['a'] = schedule_temp['staff'].apply(staff_condition, axis=1)

schedule_temp = schedule_temp.merge(staff[['staff','a']],how='left', on='staff')
schedule_temp.fillna(0, inplace=True)
schedule_temp['a'] = schedule_temp['a_y']
schedule_temp.drop(columns=['a_x', 'a_y'], inplace=True)

condition_new = condition_base.copy()
condition_new = condition_sum(schedule_temp, condition_new, ['a'])

print(schedule_temp)"""



schedule.to_excel('data/schedule.xlsx')









