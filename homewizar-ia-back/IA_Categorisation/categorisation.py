""" categorisation.py """
""" Main file for the categorisation AI """

from utils import *

from datetime import datetime

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from random import shuffle

class Categorisation_AI:
    def __init__(self):
        self.size = size
        self.dataset_config = get_config(module="Dataset")
        self.config = get_config(module="IA_Dimensions")
        self.name = name
        self.categories = None

    def generate_model(self):
        """ Model of the tensorflow AI """
        self.model = keras.Sequential([
            keras.Input(shape=(self.size, self.size, 1), name="input"),
            layers.Conv2D(4, 64, activation='relu', name="layer1"),
            layers.Conv2D(4, 32, activation='relu', name="layer2"),
            layers.Flatten(),
            layers.Dense(self.nb_cat, activation='softmax', name="output")
        ])

    def compile_model(self):
        """ Compilation of the beforementionned model """
        self.model.compile(
            optimizer=keras.optimizers.RMSprop(),
            loss=keras.losses.KLDivergence(),
            metrics=[keras.metrics.Precision()]
        )

    def prepare_dataset(self):
        """ Training and testing dataset are assigned/fetched from here """
        print("Fetching dataset")
        dt = fetch_dataset(self.dataset_config["Save_path"], "info.txt")
        print("Done")
        for d, imgs in dt.items():
            print(d)
            for i in imgs:
                print(i)

        """ TODO: Make this more clever """
        self.dataset = [[], []]
        for _, curr_dataset in dt.items():
            sep = len(curr_dataset) // 2
            self.dataset[0] += curr_dataset[sep:]
            self.dataset[1] += curr_dataset[:sep]
        self.train_set = list(zip(*self.dataset[0]))
        self.test_set = list(zip(*self.dataset[1]))
        print(len(self.train_set[0]), len(self.train_set[1]))
        print(len(self.test_set[0]), len(self.test_set[1]))

    def train(self, epochs=200):
        """ Launch a training session """
        if not self.train_set:
            raise Exception("No training set has been defined")
        train_x, train_y = self.train_set
        self.model.fit(train_x, train_y, batch_size=64, epochs=epochs)

    def test(self):
        """ Check the accuracy of the AI on the given dataset """
        if not self.test_set:
            raise Exception("No testing set has been defined")
        test_x, test_y = self.test_set
        _, accuracy = self.model.evaluate(test_x, test_y, batch_size=20)
        print("%.2f%% accuracy" % (accuracy * 100))


    def save(self):
        """ The AI saves its parameters """
        if name == None:
            name = self.name
        time = datetime.now().strftime("%d/%m/%Y_%H-%M-%S")
        self.model.save(self.config["Save_path"] + "/[" + name + "]" + time)

    def load(self):
        """ The AI loads its saved parameters """
        """ TODO: Load most recent model matching the name """
        self.model = keras.models.load_model(self.config["Save_path"] + "/" + path)

    def run(self, input):
        """ Ask the AI its interpretation of the one input """
        """ (Main function call when it's running in prod) """
        pass

def interface():
    """ Main interface that can be used to run some quick tests with the AI """

    print("INITIALISATION")
    ai = Categorisation_AI()

    print("GENERATE_MODEL")
    ai.generate_model()

    print("COMPILE_MODEL")
    ai.compile_model()

    print("FETCH DATASET")
    ai.prepare_dataset()

    print("TRAIN")
    ai.train()

    print("TEST")
    ai.test()

    print("SAVE")
    ai.save()

if __name__ == "__main__":
    interface()
