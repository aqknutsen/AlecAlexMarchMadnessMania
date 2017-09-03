import numpy as np
#from scipy.special import expit
import sys

# ONE INPUT, ONE HIDDEN, AND ONE OUTPUT LAYER
class neuralNets:

    def __init__(self, n_training_examples, n_output, n_features, n_hidden_layers, n_units_per_hidden, l1, l2, epochs, eta, alpha, decrease_const, shuffle, minibatches, random_state):

        self.n_training_examples = n_training_examples
        self.n_output = n_output
        self.n_features = n_features
        self.n_units_per_hidden = n_units_per_hidden
        self.n_hidden_layers = n_hidden_layers
        # Parameter matrix between layers
        self.weights = self._initialize_weights()
        self.l1 = l1
        self.l2 = l2
        # Number of passes over training data
        self.epochs = epochs
        # Learning rate
        self.eta = eta
        # Used for momentum learning
        self.alpha = alpha
        # Used for adpative learning rate
        self.decrease_count = decrease_const
        # Shuffling training set prior to every epoch to prevent algorithm from getting stuck in cycles
        self.shuffle = shuffle
        # Splitting training data into k mini-batches in each epoch. The gradient is computed for each mini-batch
        # separately for faster learning
        self.miniBatches = self.minibatches

    def _initialize_weights(self):

        weights_list = []
        w1 = np.random.uniform((-1.0), 1.0, size=self.n_units_per_hidden * (self.n_features + 1))
        w1 = w1.reshape(self.n_units_per_hidden, self.n_features + 1)
        weights_list.append(w1)
        for i in range(0,self.n_hidden_layers-1 ):
            w1 = np.random.uniform((-1.0), 1.0, size=self.n_units_per_hidden * (self.n_units_per_hidden + 1))
            w1 = w1.reshape(self.n_units_per_hidden, self.n_units_per_hidden + 1)
            weights_list.append(w1)

        w1 = np.random.uniform((-1.0), 1.0, size=self.n_output * (self.n_units_per_hidden + 1))
        w1 = w1.reshape(self.n_output, self.n_units_per_hidden + 1)
        weights_list.append(w1)
        return weights_list

    def _sigmoid(self, z):
        return 1.0/(1.0 + np.exp(-z))

    def _sigmoid_gradient(self, z):
        sg = self._sigmoid(z)
        return sg * (1- sg)

    def _add_bis_unit(selfself, X, how='column'):
        if how == 'column':
            X_new = np.ones((X.shape[0],X.shape[1]+1))
            X_new[:, 1:] = X
        elif how == 'row':
            X_new = np.ones((X.shape[0] + 1, X.shape[1]))
            X_new[1:,] = X
        else:
            raise AttributeError('how must be a column or row')
        return X_new

    def _feedforward(self, X, weights_list):
        a = []
        z = []
        a.append(self._add_bias_unit(X, how='column'))
        for i in range(0,self.n_hidden_layers):
            z.append(weights_list[0].dot(a.T))
            a = self.sigmoid(z)
            a.append(self._add_bis_unit(X, how = 'column'))

        z.append(weights_list[0].dot(a.T))
        a.append(self.sigmoid(z))

        return a,z

    def get_cost(self, lambda_, weights, training_example_outputs, alg_outputs):
        sum = 0
        for i in range(0, len(self.weights)):
            for j in range(0, len(self.weights[i].shape[0])):
                for k in range(0, len(self.weights[i].shape[1])):
                    sum = sum + self.weights[i][j][k]


        term2 = (sum * lambda_)/(2*self.n_training_examples)

        term1 = 0

        for i in range(0, self.n_training_examples):
            t1 = -training_example_outputs[i] * (np.log(alg_outputs[i]))
            t2 = (1-training_example_outputs[i]) * np.log(1-alg_outputs[i])
            term1 = term1 + np.sum(t1 - t2)

        term1 = term1 * (-1/self.n_training_examples )

        return term1 + term2



















