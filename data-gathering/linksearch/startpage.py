#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup as Soup
import click
import re
from typing import List, Dict
import sys
import json as libjson
import logging
from time import sleep


# link to the search startpage
SEARCH_LINK = "https://www.startpage.com/do/asearch"
# parameters for the first search query
# the only missing parameter is: query=<thing to search>
#DEFAULT_PARAMS = dict(hmb=1, cat='web', cmd='process_search', engine0='v1all', abp=1, t='air', nj=0)
DEFAULT_PARAMS = dict(cat='web', cmd='process_search', dgf=1, hmb=1, pl="", ff="")

# regex excluding some URLs we know are not interested
excludes = [
    'www.youtube.com',
    '\.pdf$',
    '\.docx?$',
]

# use a session for HTTP requests
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
})

# add a trace level to the logger
TRACE = 5
logging.addLevelName(TRACE, "TRACE")
# create a logger outputting to stderr
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stderr))


def get_infos(soup: Soup) -> List[Dict]:
    """
    For each result in the page, extract:
     - the URL
     - the title
     - the description (if any)
     :param soup: a BeautifulSoup object with the HTML page
     :return: a list of object with the informations for each link
    """
    logger.debug("getting info...")
    results = []
    blocks = soup.select('li[id^=result]') # all result blocks
    for block in blocks:
        link = block.select('h3 > a')[0]['href']
        if is_link_ok(link):
            title = block.select('h3')[0].text
            span = block.select('.desc.clk')
            descr = span[0].text if len(span) > 0 else ""
            results.append(dict(title=title, link=link, description=descr))

    logger.debug("got %d results" % len(results))
    return results


def get_links(soup: Soup) -> List[str]:
    """
    For each result in the page, extract the link it is pointing to.
    :param soup: a BeautifulSoup object with the HTML page
    :return: a list of links
    """
    logger.debug("getting links...")
    results = [l['href'] for l in soup.select('li[id^=result] h3 > a') if is_link_ok(l['href'])]
    logger.debug("got %d links" % len(results))
    return results


def is_link_ok(link: str) -> bool:
    """
    Check if the link is ok, i.e. not part of the excluded ones (see the excludes variable).

    :param link: the link
    :return: False if the link should be excluded from the results
    """
    return not any([re.search(exc, link) for exc in excludes])


def do_query(query: str, n: int = 10, processing=get_links) -> List[str]:
    """
    Query the startpage website.

    :param query: the query string
    :param n: the number of results to return
    :param processing: the function to use to extract results. One of get_links, get_infos
    :return: n results.
    """
    results = []
    start = 0
    payload = dict(**DEFAULT_PARAMS, query=query)
    logger.debug('Options: %s' % payload)

    # on startpage, the navigation uses forms with a nonce. This means that
    # in order to access a page > 1 in the results, we need to extract the
    # form hidden values and submit it using a POST.
    form_url = None     # the action parameter in the navigation form
    form_data = None    # a dictionary of hidden fields in the navigation form

    while len(results) < n:

        if form_url is None:
            # first request, do a simple get to fetch page 1
            r = session.get(SEARCH_LINK, params=payload)
        else:
            # not the first request, use a POST with the navigation form
            form_data['startat'] = start # update the page
            r = session.post(form_url, data=form_data)
        logger.log(TRACE, "request url: %s" % r.request.url)

        # get data
        soup = Soup(r.text, 'html.parser')
        results += processing(soup)
        start += 10

        # get the navigation form for further queries
        forms = soup.select('#jumpsbar form')
        if len(forms) == 0:
            logger.error("query %s: no navigation form. No result left ?" % query)
            break

        form_url = forms[0]['action']
        form_data = [(hidden['name'], hidden['value']) for hidden in forms[0].select('input[type=hidden]')]
        form_data = dict(form_data)

        logger.log(TRACE, "POST url: %s" % form_url)
        logger.log(TRACE, "POST data: %s" % form_data)

        #sleep(.1) # just to be less a "robot" TODO really necessary ?

    logger.debug('Got %d results (pruned to %d)' % (len(results), n))
    return results[:n]


def print_results(results, out, json=False):
    """
    Output the results.

    :param results: the results to print
    :param out: the file to output to
    :param json: if true, use json.dump instead of print
    """
    logger.debug("printing results")
    if json:
        libjson.dump(results, out, indent=4, ensure_ascii=False)
    else:
        print("\n".join(results), file=out)

# --- Command line

@click.group()
@click.option('--query', '-q', multiple=True, prompt=True, help="The query|queries to make.")
@click.option('--num', '-n', default=10, type=int, help="The number of results to fetch.")
@click.option('--json', '-j', default=False, is_flag=True, 
    help="If set, output json instead of the default text.")
@click.option('--output', '-o', default=sys.stdout, type=click.File('wb'), 
    help="Output, default to stdout ('-').")
@click.option('--debug', '-d', default=False, is_flag=True, help="If set, log DEBUG info to stderr.")
@click.option('--trace', '-t', default=False, is_flag=True, help="If set, log TRACE info to stderr.")
@click.pass_context
def cli(ctx, query, num, json, output, debug, trace):
    """ CLI entrypoint. """
    if trace: logger.setLevel(level=TRACE)
    elif debug: logger.setLevel(level=logging.DEBUG)
    ctx.obj['query'] = query
    ctx.obj['n'] = num
    ctx.obj['json'] = json
    ctx.obj['output'] = output

@cli.command(help="Get result links only.")
@click.pass_context
def links(ctx):
    """ CLI for getting links only """
    results = []
    for q in ctx.obj['query']:
        results += do_query(q, ctx.obj['n'], get_links)
    print_results(results, ctx.obj['output'], ctx.obj['json'])


@cli.command(help="Get informations such as title, description and link from search results.")
@click.pass_context
def infos(ctx):
    """ CLI for getting full infos """
    results = []
    for q in ctx.obj['query']:
        results += do_query(ctx.obj['query'], ctx.obj['n'], get_infos)
    print_results(results, ctx.obj['output'], True) #ctx.obj['json'])

if __name__ == "__main__":
    cli(obj={})
