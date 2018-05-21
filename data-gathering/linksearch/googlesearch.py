#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests 
import json as jsonlib
import logging
import sys
import click
from typing import List, Dict

# google api URL
# see https://developers.google.com/custom-search/json-api/v1/reference/cse/list#request
# for the json API reference
BASE_URL = 'https://www.googleapis.com/customsearch/v1'

# add a trace level to the logger
TRACE = 5
logging.addLevelName(TRACE, "TRACE")
# create a logger outputting to stderr
logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
logger.addHandler(handler)

full_fields = "items(title,snippet,link),queries(nextPage)"
links_fields = "items(link),queries(nextPage)"

def _extract_results(json_response: str, full=False) -> List:
    """
    :param json_response: the json response from Google API
    :param full: wether to extract all items or only the link
    :return: an array of links if full=False, an array of object otherwise.
    """
    return json_response['items'] if full else [o['link'] for o in json_response['items']]

def do_query(query: str, key: str, cx: str, n: int = 10, full=False):
    """
    Query the Google API.
    Note that the API returns only 10 results at a time and has a limit of 100 queries a day.

    :param query: the actual query.
    :param key: the API key.
    :param cx: the Custom Search context 
            (see https://developers.google.com/custom-search/json-api/v1/overview)
    :param n: the number of results to return.
    :param full: True to return title, snippet and link for each result, False for only an 
            array of links.
    :return: an array of results.
    """
    results = []
    json_response = None
    params = dict(key=key, cx=cx, q=query, fields=full_fields if full else links_fields)
    
    start=1          # begin at result 1
    count=min(n, 10) # the API returns at most ten results

    logger.debug("Searching %s" % query)

    while len(results) < n:
        if json_response is None:
            # first query
            logger.log(TRACE, "First query. Params=%s, count=%d" % (params, count))
        elif 'queries' not in json_response or 'nextPage' not in json_response['queries']:
            # no next query available
            logger.error('No next page for query %s' % query)
            break
        else:
            # set the offset 
            logger.log(TRACE, 'Next query. Offset=%d, count=%d' % (start, count))
            params['start'] = start

        params['num'] = count  # always set the number of results to return 
        r = requests.get(BASE_URL, params=params)
        json_response = r.json()

        with open('/tmp/google.json', 'w') as f: jsonlib.dump(json_response, f, indent=4) # TODO

        if r.status_code != 200:
            logger.error('Oops, an error occured (status=%d, response=%s. No more quota ?' % 
                (r.status_code, r.text))
        elif not 'items' in json_response:
            logger.warn('No items found. Stopping.')
            break
        else:
            results += _extract_results(json_response, full)
            start += count 
            count = min(n - len(results), 10)

    logger.debug("Got %d results." % len(results))
    return results

# -- CLI


@click.command()
@click.option('--key', '-k', required=True, help="The google api key.")
@click.option('--query', '-q', prompt=True, help="The query to make.")
@click.option('--num', '-n', default=10, type=int, help="The number of results to fetch.")
@click.option('--context', '-cx', default="015058622601103575455:cpfpm27mio8", help="The context to use.")

@click.option('--full', '-f', default=False, is_flag=True, 
    help="If set, output all information instead of just links.")
@click.option('--json', '-j', default=False, is_flag=True, 
    help="If set, output json instead of the default text.")

@click.option('--debug', '-d', default=False, is_flag=True, help="If set, log DEBUG info to stderr.")
@click.option('--trace', '-t', default=False, is_flag=True, help="If set, log TRACE info to stderr.")
def cli(key, query, num, context, full, json, debug, trace):
    """ CLI entrypoint. """
    if trace: logger.setLevel(level=TRACE)
    elif debug: logger.setLevel(level=logging.DEBUG)
    
    results = do_query(query, key, context, num, full)

    if full or json: 
        print(jsonlib.dumps(results, ensure_ascii=False, indent=4))
    else:
        print("\n".join(results))


if __name__ == "__main__":
    cli()