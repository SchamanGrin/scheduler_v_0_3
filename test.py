import pandas as pd
import numpy as np

def func(p):

    z = t_t['staff'].loc[(t_t['staff'] == p['staff']) & (t_t['staff'] == p['staff'])].count()
    t_t.iloc[i,'staff'] = 'Temp'
    i += 1
    return z

t = pd.DataFrame(np.repeat([['Бронирование', 1]], 5, axis=0), columns=['staff','a'])
t = pd.concat([t, pd.DataFrame(np.repeat([['Фамилия', 1]], 5, axis=0), columns=['staff','a'])]).reset_index(drop=True)
t_t = t.copy()


print(t)