import os
import numpy as np
import pandas as pd
from joblib import dump, load
from typing import List
from tqdm import trange
from sklearn.utils import shuffle

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Input, Flatten, Dense, Conv2D, MaxPool2D, BatchNormalization
from keras.layers.core import Dropout, Activation
from keras.layers.pooling import GlobalAveragePooling2D
from keras.models import Model
from keras import initializers, regularizers


from eeg_ai_layer.models.ssvep_utils import butter_bandpass_filter, buffer
from eeg_ai_layer.models.utils import make_confusion_matrix
from eeg_ai_layer.models.CNN.preprocess import Preprocess
from eeg_ai_layer.models.CNN.load_params import get_params

class CNNModel:
    """A generic CNN model."""

    def __init__(self, args):
        self.frequencies = args.frequencies # [0.0, 12.75, 14.75, 11.75, 10.25]
        self.CNN_params = get_params()

        if args.model_path:
            self.model = self.load_model(model_path=args.model_path)
        else:
            self.model = self.build_model()

        self.model.summary()
        self.freq2label = {freq: idx for idx, freq in enumerate(self.frequencies)}

    def build_model(self):
        '''
        Returns the Concolutional Neural Network model for SSVEP classification.
        Expecting shape of input training data 
            e.g. [num_training_examples, num_channels, n_fc] or [num_training_examples, num_channels, 2*n_fc].

        CNN_PARAMS (dict): dictionary of parameters used for feature extraction.        
        CNN_PARAMS['batch_size'] (int): training mini batch size.
        CNN_PARAMS['epochs'] (int): total number of training epochs/iterations.
        CNN_PARAMS['droprate'] (float): dropout ratio.
        CNN_PARAMS['learning_rate'] (float): model learning rate.
        CNN_PARAMS['lr_decay'] (float): learning rate decay ratio.
        CNN_PARAMS['l2_lambda'] (float): l2 regularization parameter.
        CNN_PARAMS['momentum'] (float): momentum term for stochastic gradient descent optimization.
        CNN_PARAMS['kernel_f'] (int): 1D kernel to operate on conv_1 layer for the SSVEP CNN. 
        CNN_PARAMS['n_ch'] (int): number of eeg channels
        CNN_PARAMS['num_classes'] (int): number of SSVEP targets/classes

        Returns:
            (keras.Sequential): CNN model.
        '''
        model = Sequential()
        model.add(Conv2D(2*self.CNN_PARAMS['n_ch'], kernel_size=(self.CNN_PARAMS['n_ch'], 1), 
                        padding="valid", kernel_regularizer=regularizers.l2(self.CNN_PARAMS['l2_lambda']), 
                        kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(self.CNN_PARAMS['droprate']))  
        model.add(Conv2D(2*self.CNN_PARAMS['n_ch'], kernel_size=(1, self.CNN_PARAMS['kernel_f']), 
                        kernel_regularizer=regularizers.l2(self.CNN_PARAMS['l2_lambda']), padding="valid", 
                        kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None)))
        model.add(BatchNormalization())
        model.add(Activation('relu'))
        model.add(Dropout(self.CNN_PARAMS['droprate']))  
        model.add(Flatten())
        model.add(Dense(self.CNN_PARAMS['num_classes'], activation='softmax', 
                        kernel_regularizer=regularizers.l2(self.CNN_PARAMS['l2_lambda']), 
                        kernel_initializer=initializers.RandomNormal(mean=0.0, stddev=0.01, seed=None)))
        return model

    def load_model(self, model_path: os.PathLike):
        model = tf.keras.models.load_model(model_path)
        return model

    def save_model(self, filepath):
        if not self.model: # if there is no model
            print('No model to save')
            return
        
        self.model.save(filepath)

    def predict(self, data: np.ndarray):
        """
        Make a prediction on some parsed and filtered EEG data.

        Args:
            data: Parsed and filtered EEG data

        Returns:
            Frequency predictions from the CNN model
        """
        predictions = self.model.predict(data)
        pred_freq = np.argmax(predictions, axis=1)
        return pred_freq.tolist()

    def convert_index_to_frequency(self, predictions: np.array):
        return [self.frequencies[pred] for pred in predictions]

    def split_train_test(self, data, labels):        
        """
        Splits data into training and validation set.
        
        Args:
            data: Data to be split into training and test
            labels: Labels to be split into training and test

        Returns:
            Split train and test data/labels
        """
        n_data, n_labels = shuffle(data,labels, random_state = 0)

        split_index = int(np.round(len(n_data)*0.8) )
        print(split_index)

        train_data = n_data[:split_index]
        test_data = n_data[split_index:]

        train_labels = n_labels[:split_index]
        test_labels = n_labels[split_index:]

        return (train_data, test_data, train_labels, test_labels)

    def train(self, train_data, train_labels):
        self.model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy'])
        self.model.fit(train_data, train_labels, epochs = 100)

    def test(self, test_data, test_labels):
        score = self.model.evaluate(test_data, test_labels, verbose=0) 
        preds = self.model.predict(test_data)
        pred_prob = np.array(tf.squeeze(tf.round(preds)))
        test_labels = np.array(test_labels)

        make_confusion_matrix(y_pred = pred_prob.argmax(axis=1), y_true = test_labels.argmax(axis=1))

        return score

