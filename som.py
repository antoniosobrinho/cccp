import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd

df = pd.read_csv('BACABAL_OTIMIZADO_V_INST_ANSELMO.csv')

df = df.loc[df['TIPO'] == 'U']
df = df.loc[df['ETAPA'] == 1]


dataset = list()

for i, row in df.iterrows():
    if row['LONGITUDE'] != 0:
        dataset.append([row['LONGITUDE'], 
            row['LATITUDE']])


