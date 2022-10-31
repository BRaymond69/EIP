
from datetime import datetime
import time
import os

from tensorflow import keras

class SaveSys:

    @staticmethod
    def save_now(model, path):
        # We may need to save and load the test and training set in the future
        date = datetime.now().strftime("_%d-%m-%Y_%H-%M-%S#")
        stamp = f"{time.time():.0f}"
        model.save(path + date + stamp)

    @staticmethod
    def list_saves(folder, mode="recent"):
        saves = list(map(lambda x: x.split("#"), os.listdir(folder)))
        info_id = {
            "recent": -1,
            "best": -2
        }
        sorted_saves = saves.sort(key=lambda x: int(x[info_id[mode]]), reverse=True)
        return list(map(lambda x: x[0], sorted_saves))

    @staticmethod
    def load_recent(folder):
        return keras.models.load_model(SaveSys.list_saves(folder)[0])

    @staticmethod
    def load_best(folder):
        # We still need to write the score of the tests in the saves to find reliability
        pass
