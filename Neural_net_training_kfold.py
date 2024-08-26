# -*- coding: utf-8 -*-
"""
Python code to create and train the Neural Network for Buckling Eigenvalue prediction

@author: roshan94
"""

import csv
import numpy as np
from keras.models import Sequential 
from keras.layers import Dense, Dropout, Activation
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

### Read data from NeuralNet_training_dataset
print('Reading data from csv file')
with open('H:\\Desktop\\MSEN 655 - Material Design Studio\\python code\\final bayesian optimization run\\NeuralNet_training_dataset.csv',newline='')as csvfile:
    data = [row for row in csv.reader(csvfile)]
    fibre_radius_str = ["" for x in range(len(data))]
    fibre_angle_str = ["" for x in range(len(data))]
    matrix_modulus_str = ["" for x in range(len(data))]
    buckling_eigen_1_str = ["" for x in range(len(data))]
    buckling_eigen_2_str = ["" for x in range(len(data))]
    buckling_eigen_3_str = ["" for x in range(len(data))]
    for x in range(len(data)-1):
        if (not data[x+1]):
            continue
        else:
            fibre_radius_str[x] = data[x+1][0]
            fibre_angle_str[x] = data[x+1][1]
            matrix_modulus_str[x] = data[x+1][2]
            buckling_eigen_1_str[x] = data[x+1][3]
            buckling_eigen_2_str[x] = data[x+1][4]
            buckling_eigen_3_str[x] = data[x+1][5]
        
buckling_eigen_1 = []
buckling_eigen_2 = []
buckling_eigen_3 = []
fibre_radius = []
fibre_angle = []
matrix_modulus = []
n_designs = int(len(buckling_eigen_1_str)/2 - 1)
print('In total, evaluation of ' + str(n_designs) + ' designs was attempted.')

### Store the float values of the successful abaqus evaluations
## NOTE: Erroneous storage of the outputs from the abaqus python script 
## resulted in unwanted ' and space pre-appended to the values, hence
## the string sequence from the 2nd position onwards are stored as floats. 
## Similarly an additional ' was found at the end of the third eigen value 
## strings and is thus omitted. Additionally, some of the 2nd and 3rd eigen 
## values are stored in scientific form, so if-else statements are used to 
## to splice the string appropriately
print('Storing successful evaluations as floats')
for i in range(len(buckling_eigen_1_str)):
    try:
        current_buckling_eigen1 = float(buckling_eigen_1_str[i][2:])
    except:
        continue
    else:
        fibre_radius.append(float(fibre_radius_str[i]))
        fibre_angle.append(float(fibre_angle_str[i]))
        matrix_modulus.append(float(matrix_modulus_str[i]))
        buckling_eigen_1.append(current_buckling_eigen1)
        if (buckling_eigen_2_str[i].find('E+') != -1):
            buckling_eigen_2.append(float(buckling_eigen_2_str[i][1:]))
        else:
            buckling_eigen_2.append(float(buckling_eigen_2_str[i][2:]))
            
        if (buckling_eigen_3_str[i].find('E+') != -1):
            buckling_eigen_3.append(float(buckling_eigen_3_str[i][1:-1]))
        else:
            buckling_eigen_3.append(float(buckling_eigen_3_str[i][2:-2]))
        
n_des_success = len(fibre_radius)
#print(n_des_success)
print('However, only ' + str(n_des_success) + ' designs were evaluated successfully.')

### Create dataset array from the stored floats
x = np.zeros([n_des_success, 3])
y = np.zeros([n_des_success, 3])
for i in range(n_des_success):
    x[i,:] = [fibre_radius[i], fibre_angle[i], matrix_modulus[i]]
    y[i,:] = [buckling_eigen_1[i], buckling_eigen_2[i], buckling_eigen_3[i]]
    
### Data Preprocessing 
print('Preproceessing the training dataset')
scaler = StandardScaler()
scaler.fit(y)
y_scaled = scaler.transform(y)
y_mean = scaler.mean_
y_var = scaler.var_
## The training dataset mean and variance will be used to rescale the output
## of the Neural Network
with open('normalization_constants.csv', mode='w') as norm_file:
    norm_writer = csv.writer(norm_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    norm_writer.writerow(['Training Dataset Mean[0]','Training Dataset Mean[1]','Training Dataset Mean[2]','Training Dataset Variance[0]','Training Dataset Variance[1]','Training Dataset Variance[2]'])
    norm_writer.writerow([str(y_mean[0]), str(y_mean[1]), str(y_mean[2]), str(y_var[0]), str(y_var[1]), str(y_var[2])])

### Split the dataset into training and testing datasets
x_train, x_test, y_train, y_test = train_test_split(x, y_scaled, test_size=0.2, random_state=21)

### Defining Neural Net training parameters
batch_size = 128
num_epochs = 100

def create_model():
    NeuralNet = Sequential()
    NeuralNet.add(Dense(30, input_dim=3))
    NeuralNet.add(Activation('relu'))
    NeuralNet.add(Dropout(0.3))
    NeuralNet.add(Dense(50))
    NeuralNet.add(Activation('relu'))
    NeuralNet.add(Dropout(0.3))
    NeuralNet.add(Dense(25))
    NeuralNet.add(Activation('relu'))
    NeuralNet.add(Dropout(0.3))
    NeuralNet.add(Dense(3))
    
    NeuralNet.compile(loss='mean_squared_error', optimizer='adam', metrics=['mse'])
    return NeuralNet

### K-fold cross validation
n_folds = 10
best_model = None
best_model_history = None
best_modelfold = 0
best_trainscore = 1

Score = np.empty([n_folds,2])
TrainScore = np.empty([n_folds,2])
TestScore = np.empty([n_folds,2])
skf_sc = KFold(n_folds, shuffle=True)
count = 0
for (train_ind, test_ind) in skf_sc.split(x_train, y_train):
    print("Running Fold ",str(count+1),"/",str(n_folds))
    x_train_fold = x_train[train_ind,:]
    y_train_fold = y_train[train_ind,:]
    x_val_fold = x_train[test_ind]
    y_val_fold = y_train[test_ind]
    fold_model = None
    fold_model = create_model()
    fold_History = fold_model.fit(x_train_fold, y_train_fold, batch_size=batch_size, epochs=num_epochs)
    Score[count,:] = fold_model.evaluate(x_val_fold, y_val_fold, batch_size=batch_size)
    TrainScore[count,:] = fold_model.evaluate(x_train_fold, y_train_fold, batch_size=batch_size)
    TestScore[count,:] = fold_model.evaluate(x_test, y_test, batch_size=batch_size)
    if (all(i < best_trainscore for i in list(TrainScore[count,:]))):
        best_trainscore = np.amin(TrainScore[count,:])
        best_model = fold_model
        best_model_history = fold_History
        best_modelfold = count
    count += 1
    
print('The fold corresponding to the best model is ', str(best_modelfold))

### Plotting the MSE values for training, validation and test datasets for all folds
fig1 = plt.figure()
plt.plot(Score[:,1], label='val')
plt.plot(TrainScore[:,1], label='train')
plt.plot(TestScore[:,1], label='test')
plt.xlabel('Fold Number')
plt.ylabel('Mean Squared Error in N/mm^2')
plt.title('K-Fold cross validation')
plt.legend(loc='upper right')
plt.show()
fig1.savefig('kfold_mse.png')

### PLotting the Training MSE vs Epoch for the best Neural Network
fig2 = plt.figure()
plt.plot(best_model_history.history['loss'])
plt.title('Training loss for the best Neural Network')
plt.ylabel('Mean Squared Error in N/mm^2')
plt.xlabel('Epoch')
plt.show()
fig2.savefig('mse_bestNN.png')

### Saving the best Neural Network
print('Saving the best Neural Network')
best_model.save('Buckling_Neural_Net.h5')