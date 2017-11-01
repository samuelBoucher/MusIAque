from __future__ import print_function

import numpy as np
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.layers.wrappers import TimeDistributed
from keras.models import Sequential

DATA_DIR = 'Data\chasser_des_separatistes.txt'
SEQ_LENGTH = 1000
HIDDEN_DIM = 700
LAYER_NUM = 2
BATCH_SIZE = 15
GENERATE_LENGTH = 500


def generate_text(model, length, VOCAB_SIZE, ix_to_char):
    ix = [np.random.randint(VOCAB_SIZE)]
    y_char = [ix_to_char[ix[-1]]]
    X = np.zeros((1, length, VOCAB_SIZE))
    for i in range(length):
        X[0, i, :][ix[-1]] = 1
        print(ix_to_char[ix[-1]], end="")
        ix = np.argmax(model.predict(X[:, :i + 1, :])[0], 1)
        y_char.append(ix_to_char[ix[-1]])
    return ('').join(y_char)


def main():
    data = open(DATA_DIR).read()  # 'r'
    chars = list(set(data))
    VOCAB_SIZE = len(chars)

    ix_to_char = {ix: char for ix, char in enumerate(chars)}
    char_to_ix = {char: ix for ix, char in enumerate(chars)}

    X = np.zeros((int(len(data) / SEQ_LENGTH), SEQ_LENGTH, VOCAB_SIZE))
    y = np.zeros((int(len(data) / SEQ_LENGTH), SEQ_LENGTH, VOCAB_SIZE))
    # print(X)
    # print(y)
    for i in range(0, int(len(data) / SEQ_LENGTH)):
        X_sequence = data[i * SEQ_LENGTH:(i + 1) * SEQ_LENGTH]
        print(X_sequence)
        X_sequence_ix = [char_to_ix[value] for value in X_sequence]
        # print(y_sequence)
        input_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
        # print(input_sequence)
        for j in range(SEQ_LENGTH):
            input_sequence[j][X_sequence_ix[j]] = 1.
        X[i] = input_sequence

        y_sequence = data[i * SEQ_LENGTH + 1:(i + 1) * SEQ_LENGTH + 1]
        y_sequence_ix = [char_to_ix[value] for value in y_sequence]
        target_sequence = np.zeros((SEQ_LENGTH, VOCAB_SIZE))
        for j in range(SEQ_LENGTH):
            target_sequence[j][y_sequence_ix[j]] = 1.
        y[i] = target_sequence

    model = Sequential()
    model.add(LSTM(HIDDEN_DIM, input_shape=(None, VOCAB_SIZE), return_sequences=True))
    for i in range(LAYER_NUM - 1):
        model.add(LSTM(HIDDEN_DIM, return_sequences=True))
    model.add(TimeDistributed(Dense(VOCAB_SIZE)))
    model.add(Activation('softmax'))
    model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

    nb_epoch = 0
    while True:
        print('\n\n')
        model.fit(X, y, batch_size=BATCH_SIZE, verbose=1, nb_epoch=1)
        nb_epoch += 1
        generate_text(model, GENERATE_LENGTH, VOCAB_SIZE, ix_to_char)
        # if nb_epoch % 10 == 0:
        model.save_weights('checkpoint_{}_epoch_{}.hdf5'.format(HIDDEN_DIM, nb_epoch))


if __name__ == '__main__':
    main()
