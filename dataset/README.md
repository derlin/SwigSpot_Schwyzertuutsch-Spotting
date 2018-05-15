# Dataset

This directory contains the scripts used to download and assemble the _quickstart datasets_ used for training language identifiers (see directory language-detection). The data sources are:

* [leipzig corpora collection](http://wortschatz.uni-leipzig.de/en/download/)
* [NOAH corpus](http://kitt.cl.uzh.ch/kitt/noah/corpus)
* [Swiss SMS corpus](http://www.sms4science.ch/bin/view/Main/WebHome)

## Setup

The scripts are written in python 3. Required libraries are listed in `requirements.txt`. 
To get started quickly, I advise you to use `virtualenv`. 

On __MAC and Linux__:

```bash
virtualenv -p python3 venv
source ./venv/bin/activate
pip install -r requirements.txt
```

On __Windows__:

If in PowerShell, relax the policy with `Set-ExecutionPolicy RemoteSigned` [as explained here](https://virtualenv.pypa.io/en/stable/userguide/).

```cmd
virtualenv -p python3 venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

All the scripts come with a help option:

```bash
python get_quickstart_dataset.py --help
python get_sms4science.py --help
```