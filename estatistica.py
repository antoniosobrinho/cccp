import pandas as pd
from cluster.simulated_anneling import SimulatedAnneling
import numpy as np 
import matplotlib.pyplot as plt 
import math

def distance(x, y , center):
    distance = math.pow(float(x) - float(center['x']),2) + math.pow(float(y) - float(center['y']),2)
    distance = math.sqrt(distance)

    return distance

def getLabes(x, y, centers):
    
    labes = [-1] * len(x)
    distance_to_center = float("inf")
    for j in range(len(x)):
        for i in range(len(centers)):
            center = centers[i]
            d = distance(x[j], y[j], center)
            if d < distance_to_center:
                distance_to_center = d
                labes[j] = i
        distance_to_center = float("inf")

    return labes

df_main = pd.read_csv('Planos/PINHEIRO3665_M.csv')

for j in range(2,3):
    df = df_main.loc[df_main['TIPO'] == 'U']
    df = df_main.loc[df_main['ETAPA'] == j]


    dataset = list()

    for i, row in df.iterrows():
        if row['LONGITUDE'] != 0:
            dataset.append([row['LONGITUDE'], 
                row['LATITUDE']])

    x = list()
    y = list()


    """centers_arq = open("centers.txt", "r+")
    centers = list()

    for center_arq in centers_arq:
        center_arq = center_arq.split(',')
        center = {'x':float(center_arq[0]), 'y': float(center_arq[1])}
        centers.append(center)"""



    for point in  dataset:
        x.append(point[0])
        y.append(point[1])
   
    print(i)
    arq = open("Resultados2/labels"+str(j)+".txt", "r+")
    labels = list()

    for line in arq:
        labels.append(int(line))

    #labes = getLabes(x, y, centers)


    fig = plt.figure()
    ax = fig.add_subplot(111)

    scatter = ax.scatter(x,y,s=50, c=labels)

    ax.set_xlabel('x')
    ax.set_ylabel('y')

    plt.colorbar(scatter)

    plt.show()

    df = df.groupby('UL').count()

    print(df)