import numpy as np
from ConstructTrainingExamplesKenpomOnly import ConstructTrainingExamplesKenpomOnly
from ConstructTrainingExamples import ConstructTrainingExamples
from sklearn.preprocessing import StandardScaler
import keras
from keras.models import Sequential
from keras.layers import Dense





def neural_net(training_data, training_ouput,testing_data,testing_info,
               input_size, num_hidden_layers,num_hidden_nodes_in_each_layer,batch_size,epochs):

    #Scale Data
    sc = StandardScaler()
    X_train = sc.fit_transform(training_data)
    X_test = sc.transform(testing_data)

    #Initializing Neural Network
    classifier = Sequential()

    # Adding the input layer and the first hidden layer
    classifier.add(Dense(activation = "sigmoid", units = num_hidden_nodes_in_each_layer[0],
                         kernel_initializer = 'uniform', input_dim = input_size))
    for i in range(1,num_hidden_layers):
        # Adding the second hidden layer
        classifier.add(Dense(activation = "sigmoid", units = num_hidden_nodes_in_each_layer[i],
                             kernel_initializer = 'uniform'))

    # Adding the output layer
    classifier.add(Dense(activation = "sigmoid", units = 1, kernel_initializer = 'uniform'))

    # Compiling Neural Network
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

    # Fitting our model
    classifier.fit(X_train, training_ouput, batch_size = batch_size, epochs = epochs)

    y_pred = classifier.predict(testing_data)
    y_pred_binary = (y_pred > 0.5)

    for i in range(0,len(testing_data)):
        print(testing_info[i])
        print(y_pred[i])
        print(y_pred_binary[i])

c = ConstructTrainingExamples()
arr = c.construct_training_data()
info = arr[0]
training_data = arr[1]
training_ouput = arr[2]
testing_data = arr[3]
info_testing = arr[4]
testing_data = np.matrix(testing_data)
testing_info = np.array(info_testing)
training_data = np.matrix(training_data)
training_ouput =  np.array(training_ouput)
neural_net(training_data,training_ouput,testing_data,testing_info,33,3,[20,30,30],5,50)