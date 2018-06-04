# Abstract

> In the past years, Swiss German has become more and more pregnant in written contexts. How- ever, there are still few natural language processing (NLP) studies, corpora or tools available. As a result, support for Swiss German dialects is non-existent in our day-to-day interactions with tech- nology. To automate the treatment of Swiss German and foster its adoption in online services, the SwigSpot project aimed at creating a large corpus of Swiss German sentences available to re- searchers.
>
> Using Machine Learning techniques, we first created a model able to discriminate between French, English, Italian, German and Swiss German languages using training material from avail- able corpora. We then made the assumption that the Web was the most likely source of unseen sentences. In a first attempt, we crawled more than one million landing pages from the Swiss .ch domain. It yielded very poor results, less than 1’000 new Swiss German sentences, suggesting that Swiss German is mostly used in more informal contexts such as blogs or social media. In a second attempt, we used a search engine and manual “seeds” to gather URLs likely to have Swiss German content. Crawling those URLs yielded far better results: using only 5 seeds, 211 URLs and 3 minutes of processing time, we gathered about 8’000 unseen Swiss German sentences.
This project is a Master’s Deepening Project proposed by Swisscom’s new Artificial Intelligence group.

# About this repo

This repository contains all the work done for the __SwigSpot__ project (see abstract above).

The repository is structured as such:

* `dataset`: contains the scripts used to create a _quickstart dataset_ for LID (Language IDentification) using Machine Learning;
* `language-detection`: contains all the notebooks and scripts testing various Machine Learning techniques for Swiss German language identification.
* `language-detection-webapp`: a little Python 3 / Flask webapp for quickly scraping an URL and display the results after language identification;
* `data-gathering`: contains everything related to Web scraping, including a distributed Spark crawler and scripts to gather URLs using query search engines.


Each repository contains a README with further explanations.

