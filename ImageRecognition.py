import pickle
from fastai.vision import *
from fastai.metrics import error_rate
from pathlib import Path
from glob2 import glob
from sklearn.metrics import confusion_matrix

import pandas as pd
import numpy as np
import os
import zipfile as zf
import shutil
import re
import seaborn as sns


class CNN:

    def __init__(self):
        self.prediction_recycle = {"plastic": "yellow", "paper": "blue", "metal": "yellow", "green_point": "green_point",
                                   "glass": "green", "cardboard": "blue", "brown": "brown"}
        self.learn = load_learner(r'C:\Users\Mephistopheles\Documents\Mamut\model2')

    def predict_image(self, img_path):
        img = open_image(img_path)
        pred_class, pred_idx, outputs = self.learn.predict(img)
        print(pred_class)
        return self.predict_to_recycle(str(pred_class))

    def predict_to_recycle(self, prediction):
        recycle_string = f'This is {prediction}, you ought to throw into the {self.prediction_recycle[prediction]} dumper'
        return recycle_string


if __name__ == '__main__':
    predict = CNN()
    predict.predict_image()
