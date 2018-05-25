# The _search Google approach_: POC results

Those results are a proof of concept of the _Search Google Approach_. The idea is the following:

- use human seeds to search google for common Swiss German sentences;
- retrieve the first X distinct URLs listed in the results;
- use the crawler to extract sentences from those URLs.

This method seems to work great: using __211 URLs__ and __~3 minutes__ of processing, we gathered more than 10'000 sentences.

## Stats 

Number of sentences:

```
Proba >= 80%: 10122  (uniques:  8557)
Proba >= 85%:  8816  (uniques:  7479)
Proba >= 90%:  6470  (uniques:  5528)
Proba >= 95%:  2189  (uniques:  1903)
```

Sentences per URL:
```
count:     152.00
mean :      66.59
std  :     153.87
min  :       1.00
25%  :       3.75
50%  :      12.00
75%  :      51.00
max  :    1487.00
```

Characters in sentences:

```
                   raw        san
                   ---        ---
count:        10122.00   10122.00
mean :          150.16     154.04
std  :         5501.09    5578.15
min  :           15.00      16.00
25%  :           33.00      34.00
50%  :           47.00      50.00
75%  :           79.00      83.00
max  :       553307.00  561059.00
```

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

- `crawled-urls.txt`: the list of URLs crawled, obtained through the _Google Custom Search API_ (see the scripts in the `data-gathering/linksearch` directory) using 5 seeds: 

     + _das isch sone seich_:that's bullshit;
     + _das isch super_: that's great;
     + _weiss öpper_: do somebody know...
     + _het super_: do somebodyhave...
     + _wär chamer_:who can help/give me..

- `as-collection.json`: the dump of all records in the mongo collection `as` (article sentences)

- `sentences-only.txt`: all original sentences, one per line. Contains duplicates !

- `sentences-only-san.txt`: all sanitized sentences, one per line. Contains duplicates !
