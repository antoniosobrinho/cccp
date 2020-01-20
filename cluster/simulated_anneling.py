from geopy.distance import geodesic
from cluster.point import Point
from cluster.solution import Solution
from sklearn.cluster import KMeans

import numpy as np
import statistics
import random
import math
import copy

class SimulatedAnneling(object):

    def __init__(self, temperature=1000000):

        self.temperature = temperature
        self.count_not_valid = 0
        self.alfa = 0.9
        self.min_groups = float("inf")
        self.prob_less_groups = 0.2

    def euclidian_distance(self, a, b):
        distance = 0
        for i in range(len(a)):
            distance += math.pow(a[i] - b[i],2)

        distance = math.sqrt(distance)

        return distance

    def distaces(self, a, b, distance_name):
        distance = None

        if distance_name == 'geodesic':
            distance = geodesic(a, b).km
        else:
            distance = self.euclidian_distance(a, b)
        return distance
    
    def calc_fit(self, solution, points, fix_cost, distance_name, capacity):

        centers = solution.centers
        solution.isValid = True
        quant_p_in_g = [0]*len(centers)

        np_centers = np.empty([len(centers), 2])
        for i in range(len(centers)):
            np_centers[i] = [centers[i]['x'], centers[i]['y']]

        kmeans = KMeans(
            n_init=1,
            max_iter= 1,
            n_jobs= -1,
            init= np_centers,
            n_clusters= len(centers),
            precompute_distances = True
        ).fit(self.np_points)

        k_label = kmeans.labels_

        for label in k_label:
            quant_p_in_g[label] += 1
        
        """for p in points:
            dist = float('inf')
            group = -1
            for i in range(len(centers)):
                dist_to_c = self.distaces([p.x, p.y], [centers[i]['x'], centers[i]['y']], distance_name=distance_name)
                if dist_to_c < dist:
                    dist = dist_to_c
                    group = i
            quant_p_in_g[group] += 1
         """ 

        for i in range(len(quant_p_in_g)):
            if quant_p_in_g[i] > capacity:
                solution.isValid = False  
                break
            
        solution.points_in_groups = quant_p_in_g
        solution.fit_quant_groups = fix_cost*len(centers)
        if len(quant_p_in_g) == 1:
            solution.fit_std = quant_p_in_g[0]
        else:
            solution.fit_std = statistics.stdev(quant_p_in_g)

        if solution.isValid and (len(solution.centers) < self.min_groups):
            self.min_groups = len(solution.centers)

        solution.labels = k_label
        return solution

    def mutation(self, solution, x_min, x_max, y_min, y_max, num_decimal_part_x, num_decimal_part_y):

        x = round(random.uniform(x_min, x_max), num_decimal_part_x)
        y = round(random.uniform(y_min, y_max), num_decimal_part_y)
        #solução acima da capacidade
        if not solution.isValid:
            self.count_not_valid += 1   
            #Acrescenta um centro caso tenha encontrado 10 soluções invalidas e há validas com mais centros
            if self.count_not_valid > 10 and self.min_groups > len(solution.centers):
                solution.centers.append({'x': x, 'y':y})
                self.count_not_valid = 0
            #modifica o centro do grupo com capacidade mais distante da máxima
            else:
                """ more_diff = 0
                dif = -1       
                for i in range(len(solution.centers)):
                    if more_diff < abs(solution.points_in_groups[i]-self.capacity):
                        more_diff = abs(solution.points_in_groups[i]-self.capacity)
                        dif = i
                solution.centers[dif] = {'x': x, 'y':y}"""
                #pega o grupo com menor quantidade de pontos    
                less = float("inf")
                less_position = -1       
                for i in range(len(solution.centers)):
                        if less > solution.points_in_groups[i]:
                            less = solution.points_in_groups[i]
                            less_position = i
                solution.centers[less_position] = {'x': x, 'y':y}
        #solução dentro da capacidade
        else:
            #pega o grupo com menor quantidade de pontos    
            less = float("inf")
            less_position = -1       
            for i in range(len(solution.centers)):
                    if less > solution.points_in_groups[i]:
                        less = solution.points_in_groups[i]
                        less_position = i

            prob_less_groups = random.random()
            #muda a posição do menor grupo
            if prob_less_groups > self.prob_less_groups:          
                solution.centers[less_position] = {'x': x, 'y':y}
            #retira o menor grupo
            else:
                del solution.centers[less_position]
                del solution.points_in_groups[i]


        return solution


    def cluster(self, points, capacity, etapa, fix_cost=1, quant_grups=None, distance_name='geodesic'):
        
        x_max = float('-inf')
        y_max = float('-inf')
        x_min = float('inf')
        y_min = float('inf')
        num_decimal_part_x = 7
        num_decimal_part_y = 7
        self.capacity = capacity
        self.np_points = np.empty([len(points), 2])

        """pega maior e menor x e y"""
        for i in range(len(points)):
            
            """decimal = str(points[i].x - int(points[i].x))[1:]
            if len(decimal) > num_decimal_part_x:
                num_decimal_part_x = len(decimal)
            
            decimal = str(points[i].y - int(points[i].y))[1:]
            if len(decimal) > num_decimal_part_y:
                num_decimal_part_y = len(decimal)"""
            
            if points[i].x > x_max:
                x_max=points[i].x
            elif points[i].x < x_min:
                x_min = points[i].x

            if points[i].y > y_max:
                y_max=points[i].y
            elif points[i].y < y_min:
                y_min = points[i].y
            
            self.np_points[i] = [points[i].x, points[i].y]

        solution = Solution()

        """cria 1 centro inicial"""
        x = round(random.uniform(x_min, x_max), num_decimal_part_x)
        y = round(random.uniform(y_min, y_max), num_decimal_part_y)
        center = {'x': x, 'y':y}
        solution.centers.append(center)
       
        solution = self.calc_fit(solution, points, fix_cost, distance_name, capacity)

        best_solution = solution

        print("Actual solution: " + str(solution.fit_quant_groups) + " STD: " + str(solution.fit_std))
        print("Best solucion groups: " + str(best_solution.fit_quant_groups) + " STD: " + str(best_solution.fit_std))

        while self.temperature > 1:
            
            for i in range(100):
                new_solution = self.mutation(solution, x_min, x_max, y_min, y_max, num_decimal_part_x, num_decimal_part_y)
                new_solution = self.calc_fit(new_solution, points, fix_cost, distance_name, capacity)

                if new_solution.isValid:  

                    if best_solution.isValid == False:
                        best_solution = copy.copy(new_solution)

                    #Nova solução com menos grupo que a melhor encontrada e é valida
                    if new_solution.fit_quant_groups < best_solution.fit_quant_groups:
                            best_solution = copy.copy(new_solution)
                            solution = copy.copy(new_solution)
                    
                    #Nova solução com a mesma quantidade de grupos que a melhor encontrada mas com std menor
                    elif (new_solution.fit_quant_groups == best_solution.fit_quant_groups) and ( new_solution.fit_std< best_solution.fit_std):
                        best_solution = copy.copy(new_solution)
                        solution = copy.copy(new_solution)

                    #Nova solução com menos grupo que a solução atual encontrada e é valida  
                    elif new_solution.fit_quant_groups < solution.fit_quant_groups:
                            solution = copy.copy(new_solution)
                    
                    #Nova solução com a mesma quantidade de grupos que a atual encontrada mas com std menor
                    elif (new_solution.fit_quant_groups == solution.fit_quant_groups) and ( new_solution.fit_std< solution.fit_std):
                        solution = copy.copy(new_solution)

                    #solução valida, porém pior que a atual
                    else:
                        delta_fit = abs(solution.fit_std - new_solution.fit_std)
                        boltzmann_factor = math.e**(-delta_fit/self.temperature)
                        acceptance = random.random()
                        if boltzmann_factor > acceptance:
                            solution = copy.copy(new_solution)

                else:
                    #solução atual e nova são invalidas
                    if solution.isValid == False: 
                        #solução nova é tem mais grupos que a atual ou dvp maior      
                        if (solution.fit_std < new_solution.fit_std) or (solution.fit_quant_groups > new_solution.fit_quant_groups):
                            delta_fit = abs(solution.fit_std - new_solution.fit_std)
                            boltzmann_factor = math.e**(-delta_fit/self.temperature)
                            acceptance = random.random()
                            if boltzmann_factor > acceptance:
                                solution = copy.copy(new_solution)
                        #solução nova é melhor que a atual
                        else:
                            solution = copy.copy(new_solution)

            
            print("Actual solution: " + str(solution.fit_quant_groups) + " STD: " + str(solution.fit_std)+ " Is valid: " + str(solution.isValid)) 
            print("Max: " + str(max(solution.points_in_groups)) + " Min: " + str(min(solution.points_in_groups)))
            print("Best solucion groups: " + str(best_solution.fit_quant_groups) + " STD: " + str(best_solution.fit_std) + " Is valid: " + str(best_solution.isValid))
            print("Max: " + str(max(best_solution.points_in_groups)) + " Min: " + str(min(best_solution.points_in_groups)))
            print("Temperature: " + str(self.temperature))
            print("Min groups valid: " + str(self.min_groups))
            print(etapa)
            self.temperature = self.temperature*self.alfa

        arq = open("Resultados/centers"+str(etapa)+".txt", "w+")

        for center in best_solution.centers:
            arq.write(str(center['x']) + ", " + str(center['y']) +"\n")
            
        arq.close()

        arq = open("Resultados/labels"+str(etapa)+".txt", "w+")
    
        for label in best_solution.labels.tolist():
            arq.write(str(label)+"\n")
        arq.close

        
        return best_solution