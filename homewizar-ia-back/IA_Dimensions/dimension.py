""" dimension.py """
""" Main file for the dimension AI """

from utils import *

from datetime import datetime

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from random import shuffle
from random import randrange

class Dimension_AI:
    def __init__(self, size=128, name="dim"):
        self.size = size
        self.dataset_config = get_config(module="Dataset")
        self.config = get_config(module="IA_Dimensions")
        self.name = name
        self.output_range = 50

        self.focus = "w"
        self.max = 200

    def generate_model(self):
        """ Model of the tensorflow AI """
        self.model = keras.Sequential([
            keras.Input(shape=(self.size, self.size, 1), name="input"),
            layers.Conv2D(4, 64, activation='relu', name="layer1"),
            layers.Conv2D(4, 32, activation='relu', name="layer2"),
            layers.Flatten(),
            layers.Dense(self.output_range, activation='softmax', name="output")
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
        focus = {
            "w": 0,
            "h": 1,
            "d": 2
        }
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
            dims = zip(*curr_dataset)[1]
            avg = sum(data[focus[self.focus]] for data in dims)
            lhs = [dim[focus[self.focus]] for dim in dims if dim[focus[self.focus]] <= avg]
            rhs = [dim[focus[self.focus]] for dim in dims if dim[focus[self.focus]] > avg]
            
            sep = len(curr_dataset) // 2
            self.dataset[0] += curr_dataset[sep:]
            self.dataset[1] += curr_dataset[:sep]

        def img_to_input(path):
            return [randrange(0, 1) for i in range(self.size * self.size)]

        def dim_to_output(dim):
            out = [0] * self.output_range
            pos = dim[focus[self.focus]] // 6 # 300
            print(pos)
            out[pos] = 1
            return out

        self.train_set = list(zip(*self.dataset[0]))
        self.train_set[0] = list(map(img_to_input, self.train_set[0]))
        self.train_set[1] = list(map(dim_to_output, self.train_set[1]))

        self.test_set = list(zip(*self.dataset[1]))
        self.test_set[0] = list(map(img_to_input, self.test_set[0]))
        self.test_set[1] = list(map(dim_to_output, self.test_set[1]))

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

    def save(self, name=None):
        """ The AI saves its parameters """
        if name == None:
            name = self.name
        time = datetime.now().strftime("%d/%m/%Y_%H-%M-%S")
        self.model.save(self.config["Save_path"] + "/[" + name + "]" + time)

    def load(self, path):
        """ The AI loads its saved parameters """
        """ TODO: Load most recent model matching the name """
        self.model = keras.models.load_model(self.config["Save_path"] + "/" + path)

    def run(self, inp):
        """ Ask the AI its interpretation of the one input """
        """ (Main function call when it's running in prod) """
        return self.model(inp)

def interface():
    """ Main interface that can be used to run some quick tests with the AI """

    print("INITIALISATION")
    ai = Dimension_AI()

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
