""" categorisation_v2.py """
""" Main file for the categorisation AI """

from utils import *
from save import *

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from random import shuffle

class Categorisation_v2_AI:
    def __init__(self, name="AI_Categorization", size=128, output_shape=2, dt_path="IA_Categorisation/dt.data", debug=False):
        self.name = name
        self.size = size
        self.output_shape = output_shape
        self.dt_path = dt_path
        self.debug = debug
        self.dataset_config = get_config(module="Dataset") # To be changed
        self.paths = {
            "save": "./IA_Categorisation/IA_Save/",
            "templates": "./Modelisation/Templates/ids.json"
        }
        self.templates = {
            id: (path, img2pxl(path))
            for id, path in fetch_templates(self.paths["templates"]).items()
        }
        self.model = None

    def generate_model(self):
        """ Model of the tensorflow AI """
        """
        Input: 1=Target Image 2=Image we are comparing it to

        111111111111
        111111111111
        111111111111
        111111111111
        111111111111
        222222222222
        222222222222
        222222222222
        222222222222
        222222222222
        h = size*2, w = size

        Output:
        [a, b]
        a = images are similar
        b = same category
        """
        # https://www.tensorflow.org/api_docs/python/tf/keras/Sequential
        self.model = keras.Sequential([
            layers.InputLayer(input_shape=(self.size * 2, self.size, 1), name="input"),
            layers.Conv2D(4, 3, input_shape=(self.size * 2, self.size, 1), activation='relu', name="layer1"),
            layers.Conv2D(4, 3, input_shape=(self.size // 2, self.size // 4, 1), activation='relu', name="layer2"),
            layers.Conv2D(4, 3, input_shape=(self.size // 16, self.size // 16, 1), activation='relu', name="layer3"),
            layers.Flatten(),
            layers.Dense(self.output_shape, activation='softmax', name="output")
        ])
        if self.debug:
            print(f"{self.name}: Model initialized")
            print(f"Input: {self.model.input_shape}")
            print(f"Output: {self.model.output_shape}")
            print(" ------------- ", flush=True)

    def compile_model(self):
        """ Compilation of the beforementionned model """
        self.model.compile(
            # https://towardsdatascience.com/optimizers-for-training-neural-network-59450d71caf6
            optimizer=keras.optimizers.SGD(),
            # https://towardsdatascience.com/common-loss-functions-in-machine-learning-46af0ffc4d23
            loss=keras.losses.BinaryCrossentropy(),
            # https://towardsdatascience.com/metrics-to-evaluate-your-machine-learning-algorithm-f10ba6e38234
            metrics=[keras.metrics.CategoricalAccuracy()]
        )
        if self.debug:
            print(f"{self.name}: Model compiled", flush=True)

    def prepare_dataset(self, redo=False):
        """ Training and testing dataset are assigned/fetched from here """
        if not redo and os.path.exists(self.dt_path):
            """ TODO: Implement save of dataset to avoid problems in future """
            pass
        print("Fetching dataset", flush=True)
        dt = fetch_dataset(self.dataset_config["Save_path"][0])
        self.refs = fetch_templates()
        print("Done", flush=True)
        if self.debug:
            print(f'{self.name}: loaded {len(dt.keys())} categories')
            for d, imgs in dt.items():
                print(f"{d}: {len(imgs)} samples")
            print(" ------------- ", flush=True)

        print("Processing model template images", flush=True)
        refs = {}
        for r, p in self.refs.items():
            refs[r] = img2pxl(p, debug=True)
        print(f"Done: loaded {len(self.refs)} templates", flush=True)

        print("Processing sample images + Coupling", flush=True)
        samples = {}
        for k, v in dt.items():
            l = len(v)
            samples[k] = []
            no_match = []
            shuffle(v) # The shuffling is to reduce the load for the next part
            for i, s in enumerate(v):
                path = f'{self.dataset_config["Save_path"][0]}{k}/{s[0]}'
                pxl = img2pxl(path, debug=False)
                """ Coupling: Every samples will have a coupling with each templates """
                for r_id, r_pxl in refs.items():
                    is_similar  = 1 if s[1] == r_id else 0
                    is_same_cat = 1 if self.refs[r_id].split("/")[-2] == self.refs[s[1]].split("/")[-2] else 0
                    if is_similar:
                        samples[k] += [(pxl + r_pxl, [is_similar, is_same_cat])]
                    else:
                        no_match += [(pxl + r_pxl, [is_similar, is_same_cat])]
                shuffle(no_match) # take 5 unmatching samples to reduce the load
                samples[k] += no_match[5:]
                print(f"{k} progress: {i + 1}/{l}", end="\r", flush=True)
            print()
        print(f"Done: loaded {sum(map(len, samples.values()))} samples", flush=True)

        print("Splitting the sets", flush=True)
        """ Plan: Shuffle each category (done earlier) and split in the middle, half for training and half for testing """
        self.train_set = []
        self.test_set = []
        for v in samples.values():
            middle = len(v) // 2
            self.train_set += v[:middle]
            self.test_set  += v[middle:]
        # self.train_set = self.train_set[:1000]
        self.train_set = [self.train_set[i:i+len(self.train_set)//5] for i in range(0, len(self.train_set), len(self.train_set)//5)]
        # self.test_set = self.test_set[:1000]
        self.test_set  = [self.test_set[i:i+len(self.test_set)//5]   for i in range(0, len(self.test_set),  len(self.test_set)//5)]
        self.generator_sets = False
        print(f"Done: loaded {len(self.train_set)} train samples and {len(self.test_set)} test samples", flush=True)

    def prepare_dataset_generator(self):
        """ Training and testing dataset are assigned/fetched from here """
        print("Fetching dataset", flush=True)
        dt = fetch_dataset(self.dataset_config["Save_path"][0])
        self.refs = fetch_templates()
        print("Done", flush=True)
        if self.debug:
            print(f'{self.name}: loaded {len(dt.keys())} categories')
            for d, imgs in dt.items():
                print(f"{d}: {len(imgs)} samples")
            print(" ------------- ", flush=True)

        total_set = [[samples] for samples in dt.values()]
        [shuffle(samples) for samples in total_set]
        self.train_paths = total_set[:len(total_set) // 2]
        self.test_paths = total_set[len(total_set) // 2:]
        print("Setting up the generators")
        def dataset_generator(dt_paths):
            for category, samples in dt_paths:
                for sample in samples:
                    path = f'{self.dataset_config["Save_path"][0]}{category}/{sample[0]}'
                    pxl = img2pxl(path)
                    no_match = []
                    for model, model_pxl in self.templates.items():
                        is_similar  = 1 if sample.split("_")[1] == model else 0
                        is_same_cat = 1 if self.refs[model].split("/")[-2] == self.refs[sample[1]].split("/")[-2] else 0
                        if is_similar:
                            yield pxl + model_pxl, [is_similar, is_same_cat]
                        else:
                            no_match += [(pxl + model_pxl, [is_similar, is_same_cat])]
                    shuffle(no_match)
                    for non_matching in no_match[:4]:
                        yield non_matching
        
        self.train_set = dataset_generator(zip(dt.keys(), self.train_paths))
        self.test_set = dataset_generator(zip(dt.keys(), self.test_paths))
        self.generator_sets = True
        print("Done, ready to go")

    def train(self, epochs=100):
        """ Launch a training session """
        if not self.train_set:
            raise Exception("No training set has been defined")
        if not self.generator_sets:
            for sets in self.train_set:
                print("Unzipping train dataset", flush=True)
                train_x, train_y = list(zip(*sets))
                print("Training", flush=True)
                self.model.fit(train_x, train_y, batch_size=64, epochs=epochs)
                break
        else:
            self.model.fit_generator(self.train_set, epochs=epochs)

    def test(self):
        """ Check the accuracy of the AI on the given dataset """
        if not self.test_set:
            raise Exception("No testing set has been defined")
        if not self.generator_sets:
            for sets in self.test_set:
                print("Unzipping test dataset", flush=True)
                test_x, test_y = list(zip(*sets))
                print("Testing", flush=True)
                _, accuracy = self.model.evaluate(test_x, test_y, batch_size=64)
                print("%.2f%% accuracy" % (accuracy * 100))
        else:
            self.model.evaluate_generator(self.test_set, batch_size=64)

    def save(self, name=None):
        """ The AI saves its parameters """
        if name == None:
            name = self.name
        SaveSys.save_now(self.model, self.dataset_config["Save_path"][0] + "/" + name)

    def load(self, load_type="r"):
        """ The AI loads its saved parameters """
        load_method = {
            "r": SaveSys.load_recent,
            "b": SaveSys.load_best
        }
        self.model = load_method[load_type](self.dataset_config["Save_path"])

    def run(self, input):
        """ Ask the AI its interpretation of the one input """
        if self.model == None:
            raise Exception("Cannot run no AI, either build one or load an existing one")
        pixels = img2pxl(input)
        pixels += pixels # to be changed
        res = self.model(pixels)
        return 1



def interface():
    """ Main interface that can be used to run some quick tests with the AI """
    print("INITIALISATION")
    ai = Categorisation_v2_AI(debug=True)

    print("FETCH DATASET")
    ai.prepare_dataset()

    print("GENERATE_MODEL")
    ai.generate_model()

    print("COMPILE_MODEL")
    ai.compile_model()

    print("TRAIN")
    ai.train(epochs=1)

    print("TEST")
    ai.test()

    print("SAVE")
    ai.save()

if __name__ == "__main__":
    interface()
