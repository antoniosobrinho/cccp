from sklearn.cluster import MeanShift
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

np_dataset = np.array(dataset)

clustering = MeanShift(bandwidth=0.002, n_jobs=-1).fit(np_dataset)

x = list()
y = list()

for point in  dataset:
    x.append(point[0])
    y.append(point[1])

print(len(set(clustering.labels_)))


fig = plt.figure()
ax = fig.add_subplot(111)

scatter = ax.scatter(x,y,c=clustering.labels_,s=50)

ax.set_xlabel('x')
ax.set_ylabel('y')

for i,j in clustering.cluster_centers_:
    ax.scatter(i,j,s=50,c='red',marker='+')

plt.colorbar(scatter)


plt.show()
