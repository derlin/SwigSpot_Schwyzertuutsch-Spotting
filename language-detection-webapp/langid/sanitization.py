import re

reg_nonletters_v0 = re.compile("[^\w \.,]|\d|_")


def remove_nonletters_v0(text: str) -> str: return re.sub(reg_nonletters_v0, " ", text)


def remove_manyspaces_v0(text: str) -> str: return re.sub(r'\s+', ' ', text)


def sanitize_v0(text: str) -> str:
    text = text.lower()
    text = remove_nonletters_v0(text)
    text = remove_manyspaces_v0(text)
    return text.strip()


# ----------

reg_nonletters_v1 = re.compile("[^\w \.,']|\d") # TODO: '-' ?

def normalise_singlequotes_v1(text: str) -> str:
    return re.sub("’", "'", text)

def remove_nonletters_v1(text: str) -> str:
    return re.sub(reg_nonletters_v1, " ", text)

def remove_lost_v1(text: str) -> str:
    text = re.sub(r"([^\w]|[, \.])'([^\w]|[, \.])", r"\1\2", text)
    # text = re.sub("' +", "'", text)
    # text = re.sub("- +", "", text)
    return text

def remove_manyspaces_v1(text: str) -> str:
    return re.sub(r'\s+', ' ', text)

def remove_manynonletters_v1(text: str) -> str:
    text = re.sub(r"^([^\w]|[, \.])+", "", text)  # remove leading non letters
    text = re.sub(r"([^\w]|[_, ])+([\.,]+)", r"\2", text) # remove non letters before dots, comma, underscores
    text = re.sub(r"[,\.][,\.]+", ".", text) # replace multiple nonletters following each other. '...' => '.'
    return text

def sanitize_v1(text: str) -> str:
    #if not ad.is_latin(text): print("not latin:", text)
    text = normalise_singlequotes_v1(text)
    text = remove_nonletters_v1(text)
    text = remove_lost_v1(text)
    text = remove_manynonletters_v1(text)
    text = remove_manyspaces_v1(text)
    return text.strip()

# ----------

reg_nonletters_v2 =  re.compile("[^\w ]|\d|_")

def sanitize_v2(text: str) -> str:
    text = re.sub(reg_nonletters_v2, " ", text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

# from alphabet_detector import AlphabetDetector
# ad = AlphabetDetector()