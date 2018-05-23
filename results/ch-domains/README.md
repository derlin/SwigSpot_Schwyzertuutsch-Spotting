# Crawling the .ch domain: results

Those results were obtained by running the data-gathering pipeline (Spark Crawler) on a list of __1'150'975 URLs__ from the .ch domain (list from viewdns, 2017-11). The crawl was done during May, 2018. 

In total, we processed __1'150'975 URLs__. 227'684 of them were _unreachable_ and 321'046 triggered encoding or server errors, leaving __829'929 HTML pages__ with potential Swiss German.

We kept only sentences with a probability of Swiss German >= 85%. Note that due boilerpipe and classifier limitations, a lot of the results are false positive. Here are the numbers:

| ≥ 0.85 | ≥ 0.90 | ≥ 0.95 |
|--------|--------|--------|
| 30’452 | 7’969  | 1’517  |





## Files

- `all-sentences.csv`: all the sentences extracted in a CSV format. Headers:
     + url
     + proba-de
     + proba-fr
     + proba-en
     + proba-it
     + proba-sg
     + crawled-date
     + crawled-time
     + sentence-orig
     + sentence-sanitized
    
- `sentences-95-percent-plus.csv`: sentences with more than 95% probability of being Swiss German. Headers:
     + url
     + proba-sg
     + sentence-orig
     + sentence-sanitized

- `crawled-urls.csv`: the list of URLs crawled. exception is set to "OK" if the crawl succeeded.
    + url
    + sg-count
    + exception
- `as-collection.json`: the dump of all records in the mongo collection `as` (article sentences)