# Link Search

This directory contains Python and bash scripts to get URLs from search engines.

## Google 

The script `goolesearch.py` uses [Google Custom Search](https://developers.google.com/custom-search/) through the [Google Custom Search JSON API](https://developers.google.com/custom-search/json-api/v1/overview).

To use it, you need to setup a Google project and to get an API key as described [here](https://developers.google.com/custom-search/json-api/v1/overview#prerequisites). 

Usage: use the `--help` option to get started.

```bash
python googlesearch.py --help
```

Notes: 

- A default search context is already setup. 
- You have limited quota. To monitor it, go to your Google Cloud console and navigate to the [_API Quota_ page](https://console.developers.google.com/apis/api/customsearch.googleapis.com/quotas).

## StartPage

[StartPage](https://www.startpage.com/) is a free search engine. Slower than Google, it is however easier to scrape :). 

Usage: use the `--help` option to get started.

```bash
python startpage.py --help
```




