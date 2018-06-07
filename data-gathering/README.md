# Data Gathering tools

The components in this repository have been used for both approaches: (1) scraping of the _.ch domain_ and (2) the _search engine approach_.

## Folders

- `langid-microservice`: microservice for language prediction written in Python 3 and using gRPC;
- `linksearch`: command line tools to query search engines (either Google or StartPage);
- `protos`: gRPC prototype definitions;
- `spark-crawler`: a Spark application for scraping webpages and extracting Swiss German content.

## Architecture

The architecture is as follows:

<img src="https://docs.google.com/drawings/d/e/2PACX-1vSeY68mCFcGZmePVHpJ1-ubQHzE2szqU9vxLJ9jj_hacZNPqS7-2n3qXaPZqlily3nmUTxHD_kJntrv/pub?w=960&amp;h=720">

As you can see, we have three main components:

1. _langid-microservice_: a Python 3 microservice for language identification;
2. _database_: a [MongoDB](https://www.mongodb.com/) database to store the results; 
3. _crawler_: the main program, a Spark scala application.


## Scraping URLs: setup

If you already have a bunch of URLs you want to crawl (and no HADOOP cluster available), you can run everything locally. For that:

1. Launch the `langid-microservice` server, either using Docker or on your local machine (see the README);
2. Launch a MongoDB instance somewhere. Using docker:
    ```shell
    docker pull mongo:latest
    mkdir mongo-datadir
    docker run --rm --name langid-mongo -v $(pwd)/datadir:/data/db -p 27017:27017 -d mongo:latest
    ```
3. Launch `spark-crawler` from your favorite IDE or using `java -jar` (README).

## Getting URLs

You can use the scripts in `linksearch` in order to make search engine queries and get the resulting URLs into a text file. Once you have the file, use the scraper described above.
