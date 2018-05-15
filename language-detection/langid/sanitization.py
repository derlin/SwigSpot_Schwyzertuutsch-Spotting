import re
import numpy as np

reg_nonletters = re.compile("[^\w ]|\d|_") # re.compile("[^\w \.,]|\d|_")


def remove_nonletters(text: str) -> str:
    return re.sub(reg_nonletters, " ", text)


def remove_manyspaces(text: str) -> str:
    return re.sub(r'\s+', ' ', text)


def sanitize(text: str) -> str:
    text = remove_nonletters(text)
    text = remove_manyspaces(text)
    return text.strip()


np_sanitize = np.vectorize(sanitize)
