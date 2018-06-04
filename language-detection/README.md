# Language detection

This folder contains various tests and models for the detection of English, German, Italian French and Swiss German, with of course a special interest in Swiss German.

To only peek at the best models, have a look at the notebooks prefixed with `09-FinalModel-`.

## Folders

* `data` contains the datasets used for training, testing and validation. Files have been created using the scripts in the `dataset` folder at the root of the project.
* `langid`: a python package for our custom classes and tools that are not dependent on the Jupyter Notebook (and create not visualisation);
* `notebooks`: contains the notebooks as well as scripts intended to run inside a Jupyter Notebook.

## Technologies

All the experiments are done in Jupyter Notebooks.

| Tool       | Version |
|------------|---------|
| Python     | 3.6.5   |
| Anaconda   | 5.1.0   |
| Keras      | 2.1.5   |
| TensorFlow | 1.7.0   |


## Setup

Within anaconda, you need at least a python 3 environment. I personnally used the default environment for all notebooks except the one using Keras. For this one, a new virtual environment within anaconda was created, called `keras-tf` (see [this gist](https://gist.github.com/jeffgreenca/28e0fe58644b8af48f97a3e18fe08302) for more information on how to install Keras+Tensorflow in Anaconda). 

To get started, simply launch anaconda _from this folder_ (and not inside the `notebooks` folder). This is important for the imports to work.

