import io
import os.path
import scipy
import numpy as np
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import random

from sklearn.pipeline import Pipeline
from sklearn import model_selection # cross_validation
from sklearn import metrics

from typing import List

# ==========================
#  set big fonts in plots
# ==========================
## NOT WORKING FROM HERE... => RUN IT INSIDE THE NOTEBOOK
# SMALL_SIZE = 20
# matplotlib.rc('font', size=SMALL_SIZE)
# matplotlib.rc('axes', titlesize=SMALL_SIZE)


# ==========================
#  data loading
# ==========================

_datadir = "../data"
langs = ['de', 'fr', 'en', 'it', 'sg']

def load_data():
    """
    Load the data from disk.
    :return (X, y)
    """
    X = []
    y = []
    
    for i in range(len(langs)):
        fpath = os.path.join(_datadir, '%s.txt' % langs[i])
        lines = [ line.strip() for line in io.open(fpath, encoding="utf-8") ]
        X += lines
        y += [i] * len(lines)

    return (np.array(X), np.array(y))


def load_split_data(test_size=0.2, random_state=0, **kwargs):
    """ 
    Load and split data into train and test set.
    Usage: 
       X_train, X_test, y_train, y_test = load_split_data()
    """
    (X,y) = load_data()
    return model_selection.train_test_split(X, y, test_size=test_size, random_state=random_state, **kwargs)


# ==========================
#  printing results
# ==========================

def print_results(y_real, y_predicted, labels=langs):
    print("accuracy: %.4f" % metrics.accuracy_score(y_real, y_predicted))
    print()
    print(metrics.classification_report(y_real, y_predicted, target_names=labels, digits=4))

def plot_confusion_matrix(y_real, y_predicted, normalised=False, figsize=(10,6), labels=langs, title='Confusion Matrix for Languages'):
    cm = metrics.confusion_matrix(y_real, y_predicted)
    fmt = ''
    if normalised: 
        cm = cm.astype('float')/cm.sum(axis=1)[:, np.newaxis]
        fmt = '.3f'
        
    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt=fmt, xticklabels=labels, yticklabels=labels)#"YlGnBu");
    plt.title(title)
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.show()


def print_errors_per_lang(y_real, y_predicted):
    errors_idx = np.argwhere(y_real != y_predicted)
    print("Errors per language:\n")
    for (y, count) in zip(*np.unique(y_real[errors_idx], return_counts=True)):
        print("  %s: %4d" % (langs[y], count))


def print_sample_errors(X, y_real, y_predicted, limit=None):
    errors_idx = np.argwhere(y_real != y_predicted).flatten()
    # print sample errors
    print("\nSample errors:\n")
    if limit is not None and len(errors_idx) > limit: 
        random.shuffle(errors_idx)
        errors_idx = errors_idx[:limit]

    print("real|predicted  <sentence>")
    print('--------------------------')
    for idx in errors_idx:
        print("  {}|{}   {}".format(langs[y_real[idx]], langs[y_predicted[idx]], X[idx]))


# ==========================
#  SMS recall (validation)
# ==========================

sms_sg = [ line.strip() for line in io.open(os.path.join(_datadir, 'sms-sg.txt'), encoding="utf-8") ]

def test_recall_with_sms(pipe: Pipeline):
    sms_predicted = pipe.predict(sms_sg)
    
    error_idx = np.argwhere(sms_predicted != 4).flatten()   
    stats = metrics.confusion_matrix([4] * len(sms_predicted), sms_predicted)[-1]

    print("total samples %8d" % len(sms_predicted))
    print("total errors  %8d (%.2f%%)" % (len(error_idx), len(error_idx) / len(sms_predicted) * 100))
    print("---------------------------------")
    print("languages detected")
    for t in zip(langs, stats):
        print("    %s %8d" % t)


def eval_recall_sms(sms_predicted): 
    error_idx = np.argwhere(sms_predicted != 4).flatten()   
    stats = metrics.confusion_matrix([4] * len(sms_predicted), sms_predicted)[-1]

    print("total samples %8d" % len(sms_predicted))
    print("total errors  %8d (%.2f%%)" % (len(error_idx), len(error_idx) / len(sms_predicted) * 100))
    print("---------------------------------")
    print("languages detected")
    for t in zip(langs, stats):
        print("    %s %8d" % t)


# ==========================
#  SMS any (validation)
# ==========================


def load_sms_any():
    sms_any_X = []
    sms_any_y = []
    for line in io.open(os.path.join(_datadir, 'sms-any.txt'), encoding="utf-8"):
        line = line.strip()
        y, x = line[:2], line[3:]
        sms_any_X.append(x)
        sms_any_y.append(langs.index(y))
    return np.array(sms_any_X), np.array(sms_any_y)


# ==========================
#  VALIDATION data (leipzig)
# ==========================

def load_validation_data():
    """
    Load the data prefixed with `valid_` from disk.
    :return (X, y)
    """
    X = []
    y = []
    
    for i in range(len(langs)):
        fpath = os.path.join(_datadir, 'valid_%s.txt' % langs[i])
        lines = [ line.strip() for line in io.open(fpath, encoding="utf-8") ]
        X += lines
        y += [i] * len(lines)

    return (np.array(X), np.array(y))