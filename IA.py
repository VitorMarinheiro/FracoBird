import random
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class Layer_Dense:
    def __init__(self, n_inputs, n_neurons):
        # Cria a matriz de pesos utilizando as dimensoes de inputs e neuronios
        # Multiplicamos por 0.10 para manter os numeros mais proximos do zero (-1 ao +1)
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)  # size of the input on this layer

        # Iniciamos o vetor de biases com 1 coluna e a quantidade de linhas necessarias para os neuronios
        self.biases = np.zeros((1, n_neurons))

    def randomWeights(self):
        for i in range(0, len(self.weights)):
            rand = random.randint(0, 3)
            if rand == 0:      # Valor Aleatorio
                self.weights[i] = random.uniform(-1, 1)
            elif rand == 1:    # Multiplicacao Aleatoria
                self.weights[i] *= random.uniform(0.2, 1.2)
            elif rand == 2:    # Soma Aleatoria
                self.weights[i] += random.uniform(-0.5, 0.5)


    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class Activation_ReLU:
    @staticmethod
    def forward(inputs):
        # Caso o numero seja menor que 0, ele será 0.
        # Caso ele seja maior que 0, será ele mesmo.
        # return np.tanh(inputs)
        return np.maximum(0, inputs)