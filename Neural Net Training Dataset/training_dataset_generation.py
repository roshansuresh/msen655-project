# -*- coding: utf-8 -*-
"""
Code to generate the training dataset for the neural network

@author: roshan94
"""
#from Post_P_Script import getResults
from math import pi, sin, radians
import csv
import numpy as np
from pyDOE2 import *
from subprocess import Popen, PIPE
import time

### Start timer
start_time = time.time()

### Initialize I/O parameter lists
input_fibre_radius = []
input_matrix_E = []
input_fibre_angle = []
output_buckling_load_e1 = [] # Buckling Load for first eigen mode
output_buckling_load_e2 = [] # Buckling Load for second eigen mode
output_buckling_load_e3 = [] # Buckling Load for third eigen mode

### Define the number of designs for Neural Network training
n_train = 2000

### Create the input designs
l_matrix = 3048
t_matrix = 254

Em_upper_limit = 8e5
Em_lower_limit = 1e4

rf_upper_limit = t_matrix/2
rf_lower_limit = 25

theta_f_upper_limit = 90
theta_f_lower_limit = 0

def project(x, Em_lower_limit, Em_upper_limit, rf_lower_limit, rf_upper_limit, theta_f_lower_limit, theta_f_upper_limit,):
    # x = [rf, theta_f, Em]
    rf_projected = x[:,0]*(rf_upper_limit-rf_lower_limit) + rf_lower_limit
    theta_f_projected = x[:,1]*(theta_f_upper_limit-theta_f_lower_limit) + theta_f_lower_limit
    Em_projected = x[:,2]*(Em_upper_limit-Em_lower_limit) + Em_lower_limit
    x_projected = np.vstack((rf_projected, theta_f_projected, Em_projected)).T
    return x_projected

x_train = lhs(3, samples=n_train, criterion='maximin')
x_train_proj = project(x_train, Em_lower_limit, Em_upper_limit, rf_lower_limit, rf_upper_limit, theta_f_lower_limit, theta_f_upper_limit)
#print(x_train_proj)

print('Design datapoints generated')

### Populate input parameter lists
input_fibre_radius = list(x_train_proj[:,0])
input_fibre_angle = list(x_train_proj[:,1])
input_matrix_E = list(x_train_proj[:,2])

### Use Abaqus FEA to determine maximum buckling load
for i in range(n_train):
    sys_command = ['abaqus','cae','noGUI=abaqus_fea_macro.py','--',str(input_fibre_radius[i]),str(input_fibre_angle[i]),str(input_matrix_E[i]),str(i)]
    process = Popen(sys_command, stdout=PIPE, stderr=PIPE, cwd=r'H:/Desktop/MSEN 655 - Material Design Studio/python code/final bayesian optimization run',shell=True)
    process.wait()
    stdout, stderr = process.communicate()
    #print(stdout)
    output_string = stdout.decode("utf-8")
    print(output_string)
    
    Eigen_1_pos_start = output_string.find('One') + 6
    Eigen_1_pos_end = output_string.find('Endone') - 1
    Eigen_2_pos_start = output_string.find('Two') + 6
    Eigen_2_pos_end= output_string.find('Endtwo') - 1
    Eigen_3_pos_start = output_string.find('Three') + 8
    Eigen_3_pos_end = output_string.find('Endthree') - 1
    
    buckling_load_e1 = output_string[Eigen_1_pos_start:Eigen_1_pos_end-1]
    buckling_load_e2 = output_string[Eigen_2_pos_start:Eigen_2_pos_end-1]
    buckling_load_e3 = output_string[Eigen_3_pos_start:Eigen_3_pos_end-1]
    
    output_buckling_load_e1.append(buckling_load_e1)
    output_buckling_load_e2.append(buckling_load_e2)
    output_buckling_load_e3.append(buckling_load_e3)
    
    process.kill()
    
    print('Datapoint ' + str(i+1) + ' evaluated')
         
    
### Writing training data to csv file
print('Wrinting data to csv file')
with open('NeuralNet_training_dataset.csv', mode='w') as train_file:
    traindata_writer = csv.writer(train_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    traindata_writer.writerow(['Fibre Radius in mm', 'Fibre Angle in Degrees', 'Fibre Youngs Modulus in N/mm^2', 'Buckling Load for first eigenmode in N', 'Buckling Load for second eigenmode in N', 'Buckling Load for third eigenmode in N'])
    for j in range(n_train):
        traindata_writer.writerow([str(input_fibre_radius[j]), str(input_fibre_angle[j]), str(input_matrix_E[j]), output_buckling_load_e1[j], output_buckling_load_e2[j], output_buckling_load_e3[j]])
    
print('Data Writing Completed....')

### End timer
print(['Run time to generate a dataset of ' + str(n_train) + ' datapoints is ' + str(time.time() - start_time) + ' seconds'])