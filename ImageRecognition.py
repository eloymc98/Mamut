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
        self.learn = load_learner('/Users/eloymarinciudad/Downloads')

    def predict_image(self):
        img = open_image('/Users/eloymarinciudad/Downloads/paper1.jpeg')
        pred_class, pred_idx, outputs = self.learn.predict(img)
        print(pred_class)
        return pred_class


if __name__ == '__main__':
    predict = CNN()
    predict.predict_image()
