import pandas as pd

def read_file(path):

    df = pd.read_csv(path, header=0, index_col=0, sep=';', encoding='cp1251')
    return df

staff = read_file('data/staff.csv')

d = staff['room'].loc[staff['staff'] == 'Чернецов Евгений']
print(d)