import random
import numpy as np


class LayerDense:
    def __init__(self, n_inputs, n_neurons):
        # Cria a matriz de pesos utilizando as dimensoes de inputs e neuronios
        # Multiplicamos por 0.10 para manter os numeros mais proximos do zero (-1 ao +1)
        self.weights = 0.10 * np.random.randn(n_inputs, n_neurons)

        # Iniciamos o vetor de biases com 1 coluna e a quantidade de linhas necessarias
        self.biases = np.zeros((1, n_neurons))

    def random_weights(self):
        for i in range(0, len(self.weights)):
            rand = random.randint(0, 3)
            if rand == 0:
                # Soma Aleatoria
                self.weights[i] += random.uniform(-0.1, 0.1)
            elif rand == 1:
                # Multiplicacao Aleatoria
                self.weights[i] *= random.uniform(0.9, 1.1)

    def forward(self, inputs):
        self.output = np.dot(inputs, self.weights) + self.biases


class ActivationReLu:
    @staticmethod
    def forward(inputs):
        # Caso o numero seja menor que 0, ele será 0.
        # Caso ele seja maior que 0, será ele mesmo.
        # return np.tanh(inputs)
        return np.maximum(0, inputs)
