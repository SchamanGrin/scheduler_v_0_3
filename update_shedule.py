import pandas as pd
import numpy as np

def read_excel(path):
    return pd.read_excel(path, header=0, index_col=0)

def read_file(path):

    df = pd.read_csv(path, header=0, index_col=0, sep=';', encoding='cp1251')
    return df


def replace_day(w,d,c_staff, upd_schedule):
    # Добавляем нужного сотрудника на первое свободное место недели w дня d
    r = staff.loc[staff['staff'] == c_staff, 'room'].values
    place = min(upd_schedule.loc[(upd_schedule['week'] == w) & (upd_schedule['day_of_week'].isin(d))
                                 & (upd_schedule['staff'] == 'Бронирование') & (upd_schedule['room'].isin(r)), 'place'].values)

    upd_schedule['staff'].loc[(upd_schedule['week'] == w) & (upd_schedule['day_of_week'].isin(d)) &
                     (upd_schedule['place'] == place) & (upd_schedule['room'].isin(r))] = c_staff

    old_place = upd_schedule.loc[(upd_schedule['week'] == w) & (~upd_schedule['day_of_week'].isin(d)) &
                                          (upd_schedule['staff'] == c_staff), 'place'].values
    old_day = upd_schedule.loc[(upd_schedule['week'] == w) & (~upd_schedule['day_of_week'].isin(d)) &
                                       (upd_schedule['staff'] == c_staff), 'day_of_week'].values

    upd_schedule['staff'].loc[(upd_schedule['week'] == w) & (upd_schedule['day_of_week'].isin(old_day)) &
                              (upd_schedule['place'].isin(old_place) & upd_schedule['room'].isin(r))] = 'Бронирование'


def insert_staff(c_staff, ):
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


upd_schedule = read_excel('data/schedule.xlsx')
staff = read_file('data/staff.csv')




#Викторию и Фаустов вместе
weeks = upd_schedule['week'].unique()

for w in weeks:
    d_1 = upd_schedule.loc[(upd_schedule['staff'] == 'Фаустов Антон') & (upd_schedule['week'] == w), 'day_of_week'].values
    d_2 = upd_schedule.loc[(upd_schedule['staff'] == 'Романенко Виктория') & (upd_schedule['week'] == w), 'day_of_week'].values
    r_1 = staff.loc[staff['staff'] == 'Фаустов Антон', 'room'].values
    r_2 = staff.loc[staff['staff'] == 'Романенко Виктория', 'room'].values

    if (d_1 and d_2) and (d_1[0] != d_2[0]):
        free_place_1 = upd_schedule.loc[(upd_schedule['staff'] == 'Бронирование') & (upd_schedule['week'] == w)
                            & (upd_schedule['day_of_week'].isin(d_1)) & upd_schedule['room'].isin(r_1), 'staff'].count()
        free_place_2 = upd_schedule.loc[(upd_schedule['staff'] == 'Бронирование') & (upd_schedule['week'] == w)
                                        & (upd_schedule['day_of_week'].isin(d_2)) & upd_schedule['room'].isin(r_2), 'staff'].count()
        if free_place_1 >= free_place_2:
            replace_day(w,d_1, 'Романенко Виктория', upd_schedule)
        else:
            replace_day(w,d_2, 'Фаустов Антон', upd_schedule)



#Убрать из графика дежурную смену
ds = ['Илюхин Даниил', 'Карташов Федор', 'Мажулин Сергей', 'Макарский Артём', 'Спиряев Егор']
upd_schedule['staff'].loc[upd_schedule['staff'].isin(ds)] = 'Бронирование'

#Выпилить себя до апреля
upd_schedule['staff'].loc[(upd_schedule['staff'] == 'Богословский Илья') &
                          (upd_schedule['timestamp'] <= np.datetime64('2021-04-20'))] = 'Бронирование'


sort_place(upd_schedule)
upd_schedule.drop(['id'], axis=1, inplace=True)
upd_schedule.to_excel('data/upd_schedule.xlsx', sheet_name='data')