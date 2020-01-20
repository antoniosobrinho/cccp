from cluster.point import Point
import pandas as pd
from cluster.simulated_anneling import SimulatedAnneling

df_main = pd.read_csv('Planos/pinheiro_3805_I_400.csv')

tipos = df_main.groupby("TIPO").groups.keys()

for tipo in tipos:
    df_etapas = df_main.loc[df_main['TIPO'] == tipo]

    etapas  = list(df_etapas.groupby("ETAPA").groups.keys())
    quant_uls = [-1]*len(etapas)
    dvp = [-1]*len(etapas)
    for i in range(len(etapas)):
        df = df_etapas.loc[df_etapas['ETAPA'] == etapas[i]]

        points = list()

        for j, row in df.iterrows():
            point = Point()
            if row['LONGITUDE'] != 0:
                point.x = row['LONGITUDE']
                point.y = row['LATITUDE']
                points.append(point)
            
        sm = SimulatedAnneling()
        solution = sm.cluster(points, 400, etapas[i])
        quant_uls[i] = solution.fit_quant_groups
        dvp[i] = solution.fit_std 
    
    print(etapas)
    print(quant_uls)
    print(dvp)
    arq = open("Resultados/solution"+tipo+".txt", "w+")

    for i in range(len(etapas)):
        arq.write(tipo + " Etapa "+ str(etapas[i]) + ": Quant uls" + str(quant_uls[i]) + " DVP " + str(dvp[i]) + "\n")

    arq.close()