
import tensorflow as ts
from tensorflow import keras
from tensorflow.keras import layers

class FurnitureCategoryAI:
    def __init__(self, path="", refpath="", size=64):
        self.ressPath = path
        self.refPath = refpath
        self.categories = ['none']
        self.size = size

    def generate_model(self):
        self.model = keras.Sequential([
            keras.Input(shape=(self.size, self.size, 1), name="input"),
            layers.Conv2D(4, 32, activation='relu', name='layer1'),
            layers.Conv2D(4, 16, activation='relu', name='layer2'),
            layers.Flatten(),
            layers.Dense(len(self.categories), activation='softmax', name='output')
        ])
        return self.model

    def compile_model(self):
        self.model.compile(
            optimizer=keras.optimizers.RMSprop(),
            loss=keras.losses.KLDiver
        )

    def training_set(self):
        train_x, train_y = 1, 2 # get inputs
        self.train_set = (train_x, train_y)

    def testing_set(self):
        test_x, test_y = 1, 2 # get inputs
        self.test_set = (test_x, test_y)

    def train(self, epochs=200):
        if not self.train_set:
            raise Exception("Missing training set")
        train_x, train_y = self.train_set
        self.model.fit(train_x, train_y, batch_size=64, epochs=epochs)

    def test(self):
        if not self.test_set:
            raise Exception("Missing testing set")
        test_x, test_y = self.test_set
        _, accuracy = self.model.evaluate(test_x, test_y, batch_size=20)
        print("%.2f%% accuracy" % (accuracy * 100))

def quick_test():
    pass

if __name__ == '__main__':
    quick_test()
