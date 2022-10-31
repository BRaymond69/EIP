#!/bin/python3

from sys import argv
from itertools import groupby
import os, sys
from PIL import Image
import numpy as np
from random import shuffle

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

from modelize import get_coords

def disable_logs():
    tf.get_logger().setLevel('WARNING')

def usage():
    print("""USAGE
    ./dimention_ai train_folder/ test_folder/ [-i=input_model] [-s=output_model] [-m=modes] [-e=epochs] [-t=test_only] [-a=always_save]

DESCRIPTION
    train_folder    folder containing the training dataset
    test_folder     folder containing the testing dataset
    input_model     the ai will import this model instead of generating another one
    output_model    the ai will save it's model in the designated output file ("ai_model" if not specified)
    modes           the type of ai that will be trained ('w' for width, 'h' for height, 'd' for depth)
    epochs          the number of epochs the AI will train in (more epochs means the AI will train more)
    test_only       set to 'yes' or 'y' to enable test only mode
    always_save     set to 'yes' or 'y' to enable always save mode (will save the data even if performing worse)
""")

def get_flags(flags):
    # adaptation of Benj's code
    if not all(e.startswith("-") and "=" in e for e in flags) or flags == []:
        return "", "", "whd", 200, False, False
    input_flag  = next((e for e in flags if e.startswith("-i=")), "-i=")
    output_flag = next((e for e in flags if e.startswith("-s=")), "-s=")
    modes       = next((e for e in flags if e.startswith("-m=")), "-m=whd")
    epochs      = next((e for e in flags if e.startswith("-e=")), "-e=200")
    test_only   = next((e for e in flags if e.startswith("-t=")), "-t=no")
    always_save = next((e for e in flags if e.startswith("-a=")), "-a=no")
    confirmations = ["yes", "y"]
    return input_flag.split("=")[1], output_flag.split("=")[1], modes.split("=")[1], int(epochs.split("=")[1]), test_only.split("=")[1] in confirmations, always_save.split("=")[1] in confirmations

def get_args():
    if "-h" in argv or len(argv) < 3:
        usage()
        exit(0)

    return argv[1:]

def get_dataset(folder):
    # code adaptation of Flo's code
    if not os.path.isdir(folder):
        raise Exception(f"{folder} is not a folder")

    files = filter(lambda x: x.endswith(".jpg") or x.endswith(".png"), os.listdir(folder))
    return list(map(lambda x: os.path.join(folder, x), files))

def get_image_input(path):
    img = Image.open(path)
    pixels = [[[r / 255] for r, g, b, *_ in list(y)] for y in np.array(img)]
    img.close()
    return pixels

def dimention_to_output(value, max_size=200, output_size=50, tolerance_range=5):
    # Im sad I had to comment everything here ;<
    # code adaptation of Benj's code
    output = [0] * output_size
    correct_pos = min(int((value - 1) * (output_size / max_size)), 49)
    output[correct_pos] = 1

    curr_precision = 1
    for x in range(tolerance_range):
        curr_precision /= 2
    
        left_i = max(0,  correct_pos - x)
        right_i = min(output_size - 1, correct_pos + x)
        output[left_i]  = max(output[left_i],  curr_precision)
        output[right_i] = max(output[right_i], curr_precision)

    return output

def get_image_output(path, target_dimentions="whd", output_size=50, tolerance_range=5):
    ai_outputs = []
    w, h, d = get_coords(path)
    dimention = {'w' : w, 'h' : h, 'd' : d}
    max_size = {'w' : 200, 'h' : 300, 'd' : 100}

    for c in target_dimentions:
        ai_outputs += [dimention_to_output(dimention[c], max_size[c], output_size, tolerance_range)]

    return ai_outputs

def get_input_output_set(folder, target_dimentions="whd"):
    # ouput format [input1, input2 ...] , [output1, output2 ...]
    # inputX = [[0..1] * 64] * 64
    # outputX = [[0..1] * 50] * 3

    files = get_dataset(folder)
    inputs = list(map(get_image_input, files))

    # zip * will unzip the output lists:
    # [[w_out1, h_out1, d_out1], [w_out2, h_out2, d_out2], [w_out3, h_out3, d_out3] ...]
    # becomes
    # [[w_out1, w_out2, w_out3, ...], [h_out1, h_out2, h_out3, ...], [d_out1, d_out2, d_out3, ...]]
    outputs = list(map(list, zip(*map(get_image_output, files))))

    mode_index = {"w" : 0, "h" : 1, "d" : 2}
    return inputs, outputs[mode_index[target_dimentions]]

class DimentionAI:

    def __init__(self, size=64, mode="w", n_output_nodes=50, debug=False):
        self.size = size
        self.n_output_nodes = n_output_nodes
        self.debug = debug
        allowed_modes = "whd"
        if mode not in allowed_modes:
            raise Exception(f"{mode} is not a valid mode (should be one of 'w' 'h' 'd')")
        self.mode = mode
        # self.accuracy = 0

    def generate_model(self):
        self.model = keras.Sequential([
            keras.Input(shape=(self.size, self.size, 1), name="input"),
            layers.Conv2D(4, 32, activation='relu', name="layer1"),
            layers.Conv2D(4, 16, activation='relu', name="layer2"),
            layers.Flatten(),
            layers.Dense(self.n_output_nodes, activation='softmax', name="output")
        ])
        if self.debug:
            self.model.summary()
        return self.model

    def compile_model(self):
        self.model.compile(
            optimizer=keras.optimizers.RMSprop(),
            loss=keras.losses.KLDivergence(),
            metrics=[keras.metrics.Precision()]
        )

    def training_set(self, folder):
        train_x, train_y = get_input_output_set(folder, target_dimentions=self.mode)
        self.train_set = (train_x, train_y)

    def testing_set(self, folder):
        test_x, test_y = get_input_output_set(folder, target_dimentions=self.mode)
        self.test_set = (test_x, test_y)

    def training_testing_set(self, folder):
        x, y = get_input_output_set(folder, target_dimentions=self.mode)
        if len(x) < 3:
            raise Exception("Too few samples to work with (must be at least 3)")

        # Shuffle the samples randomly
        sets = list(zip(x, y))
        shuffle(sets)
        x, y = list(map(list, zip(*sets)))

        # Seperate the sets (I gave 2/3 of the sets to the training to componsate the lack of training data)
        sep = round(len(x) / 3) * 2
        self.train_set = (x[:sep], y[:sep])
        self.test_set = (x[sep:], y[sep:])

    def train(self, epochs=200):
        if not self.train_set:
            raise Exception("You need to specify your training set with .training_set(folder)")
        train_x, train_y = self.train_set
        self.model.fit(train_x, train_y, batch_size=64, epochs=epochs)

    def test(self):
        if not self.test_set:
            raise Exception("You need to specify your testing set with .testing_set(folder)")
        test_x, test_y = self.test_set
        _, accuracy = self.model.evaluate(test_x, test_y, batch_size=20)
        print("%.2f%% accuracy" % (accuracy * 100))

        print("Manual tests:")
        manual_accuracy = 0
        r = {"w" : 4, "h" : 6, "d" : 2}[self.mode] # dimention range
        # print(np.array(test_x).shape, self.model.input)
        results = self.model.predict(test_x)
        for i, y_true in enumerate(test_y):
            y_pred = list(results[i])
            got = y_pred.index(max(y_pred))
            exp = y_true.index(max(y_true))
            print("in range {}-{} while expecting {}-{} - {}".format(got * r, got * r + r,
                                                                     exp * r, exp * r + r,
                                                                     "OK" if exp == got else "FAIL"))
            manual_accuracy += 1 if exp == got else 0
        print("Manual accuracy is %.2f%%" % (100 * manual_accuracy / len(test_x)))

        # was going to be used in save name but too bothersome to implement now
        # self.accuracy = round(manual_accuracy * 100, 2)

        return accuracy, manual_accuracy

    def save(self, output_file="ai_model"):
        flavor_text = {"w" : "width", "h" : "height", "d" : "depth"}[self.mode]
        self.model.save(flavor_text + "_" + output_file)

    def load(self, input_file="ai_model"):
        flavor_text = {"w" : "width", "h" : "height", "d" : "depth"}[self.mode]
        self.model = keras.models.load_model(flavor_text + "_" + input_file)

def new_ai_training(training_f, testing_f, output_file="", modes="whd", epochs=200, force_save=False):
    descriptions = {"w" : "Generating width detection AI",
                    "h" : "Generating height detection AI",
                    "d" : "Generating depth detection AI"}
    for mode in modes:
        if mode not in "whd":
            raise Exception(f"{mode} is not a valid mode (should be one of 'w' 'h' 'd')")
        print(descriptions[mode])
        ai = DimentionAI(mode=mode)

        # Model creation / Compilation
        ai.generate_model()
        ai.compile_model()

        # Setting up the training and testing sets
        if training_f == testing_f:
            ai.training_testing_set(training_f)
        else:
            ai.training_set(training_f)
            ai.testing_set(testing_f)

        # Train / Test the AI
        ai.train(epochs=epochs)
        a, m_a = ai.test()

        # Saving the model
        if a == 0 or m_a == 0 and not force_save:
            print("Not saving an AI with 0% accuracy!")
        else:
            print("Saving ai...")
            if output_file:
                ai.save(output_file=output_file)
            else:
                ai.save()


def retrain_ai(training_f, testing_f, input_file="", output_file="", modes="whd", epochs=200, force_save=False):
    descriptions = {"w" : "Retraining the width AI",
                    "h" : "Retraining the height AI",
                    "d" : "Retraining the depth AI"}
    for mode in modes:
        if mode not in "whd":
            raise Exception(f"{mode} is not a valid mode (should be one of 'w' 'h' 'd')")
        print(descriptions[mode])
        ai = DimentionAI(mode=mode)

        # Load the trained AI
        ai.load(input_file=input_file)

        # Setting up the training and testing sets
        if training_f == testing_f:
            ai.training_testing_set(training_f)
        else:
            ai.training_set(training_f)
            ai.testing_set(testing_f)

        # Train / Test the AI
        o_a, o_m_a = ai.test()
        ai.train(epochs=epochs)
        a, m_a = ai.test()

        # Saving the model
        # probably could refactor this part to look a little better
        if a >= o_a and m_a >= o_m_a or force_save:
            if a >= o_a and m_a >= o_m_a:
                print("BETTER PRECISION = saving progress")
            else:
                print("WORSE PRECISION... But saving anyways")

            if output_file:
                ai.save(output_file=output_file)
            else:
                ai.save()
        else:
            print("WORSE PRECISION = discarding changes")

def test_ai(testing_f, input_file="", modes="whd"):
    descriptions = {"w" : "Testing the width AI",
                    "h" : "Testing the height AI",
                    "d" : "Testing the depth AI"}
    for mode in modes:
        if mode not in "whd":
            raise Exception(f"{mode} is not a valid mode (should be one of 'w' 'h' 'd')")
        print(descriptions[mode])
        ai = DimentionAI(mode=mode)

        # Load the trained AI
        ai.load(input_file=input_file)

        # Setting up the testing set
        ai.testing_set(testing_f)

        # Test the AI
        a, m_a = ai.test()

if __name__ == '__main__':
    disable_logs()
    training_folder, testing_folder, *flags = get_args()
    ai_import_file, ai_export_file, modes, epochs, test_only, always_save = get_flags(flags)

    if test_only:
        print("Testing an existing AI")
        test_ai(testing_folder, input_file=ai_import_file, modes=modes)
    elif ai_import_file == "":
        print("Generating and training a new AI")
        new_ai_training(training_folder, testing_folder, output_file=ai_export_file,
                        modes=modes, epochs=epochs, force_save=always_save)
    else:
        print("Retraining an existing AI")
        retrain_ai(training_folder, testing_folder,
                   input_file=ai_import_file, output_file=ai_export_file,
                   modes=modes, epochs=epochs, force_save=always_save)
