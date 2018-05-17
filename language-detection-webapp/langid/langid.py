from boilerpipe.extract import Extractor

from .models import models

MODELS = list(models.keys())

EXTRACTORS = [
    'DefaultExtractor',
    'ArticleExtractor',
    'ArticleSentencesExtractor',
    # 'KeepEverythingWithMinKWordsExtractor', if used, don't forget to pass the kMin argument to its constructor
    'KeepEverythingExtractor',
    'LargestContentExtractor',
    'NumWordsRulesExtractor',
    'CanolaExtractor'
]


def lang_of_text(text: str, model=MODELS[0], min_words=0, with_proba=False, return_raw=False):
    model = models[model]
    sentences = text.split('\n')
    if len(sentences) == 0: return []
    func = model.predict_proba if with_proba else model.predict
    return func(sentences, min_words=min_words, return_raw=return_raw)


def sentences_from_urls(url: str, extractor_name=EXTRACTORS[0], model=MODELS[0],
                        min_words=0, with_proba=False, return_raw=False):
    extractor = Extractor(extractor=extractor_name)
    model = models[model]
    extracted_text = extractor.getTextBlocks(url=url)
    if len(extracted_text) > 0:
        func = model.predict_proba if with_proba else model.predict
        return func(extracted_text, min_words=min_words, return_raw=return_raw)


def mixed_sentences_from_urls(url: str, extractor_name=EXTRACTORS[0], model=MODELS[0],
                              min_words=0, with_proba=False, return_raw=False):
    extractor = Extractor(extractor=extractor_name)
    model = models[model]
    extracted_text = extractor.getTextBlocks(url=url)
    if len(extracted_text) > 0:
        func = model.predict_proba if with_proba else model.predict
        # ensure we don't return empty results
        return [preds for preds in
                (func(ss.split("\n"), min_words=min_words, return_raw=return_raw) for ss in extracted_text) if preds]
    return []
