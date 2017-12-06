from __future__ import print_function
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
import numpy as np
import random
import sys
from keras.models import load_model
from keras.layers import Dropout
from keras.callbacks import EarlyStopping


class Lstm:
    chars = None
    char_indices = None
    indices_char = None
    x = None
    y = None
    maxlen = 40
    step = 3
    model = None
    text = None
    earlyStopping = None

    def __init__(self, path, mode):
        self.getData(path)
        self.setUp()
        self.generateModel(mode)

    def getData(self, path):
        with open(path, 'r') as myfile:
            text = myfile.read()
        print('corpus length:', len(text))
        self.text = text

    def setUp(self):
        self.chars = sorted(list(set(self.text)))
        print('total chars:', len(self.chars))
        self.char_indices = dict((c, i) for i, c in enumerate(self.chars))
        self.indices_char = dict((i, c) for i, c in enumerate(self.chars))

        # cut the text in semi-redundant sequences of maxlen characters
        sentences = []
        next_chars = []
        for i in range(0, len(self.text) - self.maxlen, self.step):
            sentences.append(self.text[i: i + self.maxlen])
            next_chars.append(self.text[i + self.maxlen])
        print('nb sequences:', len(sentences))

        print('Vectorization...')
        self.x = np.zeros((len(sentences), self.maxlen, len(self.chars)), dtype=np.bool)
        self.y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                self.x[i, t, self.char_indices[char]] = 1
            self.y[i, self.char_indices[next_chars[i]]] = 1


        # build the model: a single LSTM
    def generateModel(self, mode):
        print('Build model...')
        self.earlyStopping = EarlyStopping(monitor='loss', min_delta=0, patience=3, verbose=1, mode='auto')
        if(mode == "Load"):
            self.model = load_model('musicModel.h5')
        else:
            self.model = Sequential()
            self.model.add(LSTM(128, input_shape=(self.maxlen, len(self.chars))))
            self.model.add(Dense(len(self.chars)))
            self.model.add(Activation('softmax'))

            optimizer = RMSprop(lr=0.01)
            self.model.compile(loss='categorical_crossentropy', optimizer=optimizer)

    def sample(self, preds, temperature=1.0):
        # helper function to sample an index from a probability array
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def write(self, diversity):
        text_file = open("Output.txt", "w")
        while True:

            start_index = random.randint(0, len(self.text) - self.maxlen - 1)

            print()
            print()
            print('----- diversity:', diversity)

            generated = ''
            sentence = self.text[start_index: start_index + self.maxlen]
            generated += sentence
            print()
            print()
            print('----- Generating with seed: "' + sentence + '"')
            print()
            print()
            text_file.write(generated)

            while True:
                x_pred = np.zeros((1, self.maxlen, len(self.chars)))
                for t, char in enumerate(sentence):
                    x_pred[0, t, self.char_indices[char]] = 1.

                preds = self.model.predict(x_pred, verbose=0)[0]
                next_index = self.sample(preds, diversity)
                next_char = self.indices_char[next_index]

                generated += next_char
                sentence = sentence[1:] + next_char

                text_file.write(next_char)
            print()

    def train(self):
        iteration = 0
        while True:
            iteration = iteration + 1
            self.model.save('musicModel.h5')

            print()
            print('-' * 50)
            print('Iteration', iteration)
            history = self.model.fit(self.x, self.y,
                                     batch_size=128,
                                     epochs=1,
                                     callbacks=[self.earlyStopping])

            start_index = random.randint(0, len(self.text) - self.maxlen - 1)

            print()
            print()
            print("TRAIN LOSS : ", history.history["loss"])

            for diversity in [0.2, 0.5, 1.0, 1.2]:
                print()
                print('----- diversity:', diversity)

                generated = ''
                sentence = self.text[start_index: start_index + self.maxlen]
                generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                sys.stdout.write(generated)

                for i in range(400):
                    x_pred = np.zeros((1, self.maxlen, len(self.chars)))
                    for t, char in enumerate(sentence):
                        x_pred[0, t, self.char_indices[char]] = 1.

                    preds = self.model.predict(x_pred, verbose=0)[0]
                    next_index = self.sample(preds, diversity)
                    next_char = self.indices_char[next_index]

                    generated += next_char
                    sentence = sentence[1:] + next_char

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                print()

if __name__ == '__main__':
    lstm = Lstm("data.txt", "Load")
    lstm.write(1.2)
