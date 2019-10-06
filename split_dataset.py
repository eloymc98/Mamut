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

path = Path('/Users/eloymarinciudad/Downloads/dataset_resized/')


## helper functions ##


## splits indices for a folder into train, validation, and test indices with random sampling
## input: folder path
## output: train, valid, and test indices
def split_indices(folder, seed1, seed2):
    n = len(os.listdir(folder))
    n -= 1
    full_set = list(range(1, n + 1))

    ## train indices
    random.seed(seed1)
    train = random.sample(list(range(1, n + 1)), int(.5 * n))

    ## temp
    remain = list(set(full_set) - set(train))

    ## separate remaining into validation and test
    random.seed(seed2)
    valid = random.sample(remain, int(.5 * len(remain)))
    test = list(set(remain) - set(valid))

    return (train, valid, test)


## gets file names for a particular type of trash, given indices
## input: waste category and indices
## output: file names
def get_names(waste_type, indices):
    file_names = [waste_type + str(i) + ".jpg" for i in indices]
    return (file_names)


## moves group of source files to another folder
## input: list of source files and destination folder
## no output
def move_files(source_files, destination_folder):
    for file in source_files:
        shutil.move(file, destination_folder)


if __name__ == '__main__':
    ## paths will be train/cardboard, train/glass, etc...
    subsets = ['train', 'valid']
    waste_types = ['brown', 'cardboard', 'glass', 'green_point', 'metal', 'paper', 'plastic']

    ## create destination folders for data subset and waste type
    for subset in subsets:
        for waste_type in waste_types:
            folder = os.path.join('/Users/eloymarinciudad/Downloads/data', subset, waste_type)
            if not os.path.exists(folder):
                os.makedirs(folder)

    if not os.path.exists(os.path.join('/Users/eloymarinciudad/Downloads/data', 'test')):
        os.makedirs(os.path.join('/Users/eloymarinciudad/Downloads/data', 'test'))
    ## move files to destination folders for each waste type
    for waste_type in waste_types:
        source_folder = os.path.join('/Users/eloymarinciudad/Downloads/dataset_resized', waste_type)
        train_ind, valid_ind, test_ind = split_indices(source_folder, 1, 1)

        ## move source files to train
        train_names = get_names(waste_type, train_ind)
        train_source_files = [os.path.join(source_folder, name) for name in train_names]
        train_dest = "/Users/eloymarinciudad/Downloads/data/train/" + waste_type
        move_files(train_source_files, train_dest)

        ## move source files to valid
        valid_names = get_names(waste_type, valid_ind)
        valid_source_files = [os.path.join(source_folder, name) for name in valid_names]
        valid_dest = "/Users/eloymarinciudad/Downloads/data/valid/" + waste_type
        move_files(valid_source_files, valid_dest)

        ## move source files to test
        test_names = get_names(waste_type, test_ind)
        test_source_files = [os.path.join(source_folder, name) for name in test_names]
        ## I use data/test here because the images can be mixed up
        move_files(test_source_files, "/Users/eloymarinciudad/Downloads/data/test")
