#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# This script downloads all the Swiss German SMS from sms4sciences.
# To use it, you must have an account and be able to access the SMS Navigator.
#
# parameters: 
#   -u, --username TEXT  Your SMS Navigator username.
#   -p, --password TEXT  Your SMS Navigator password.
#   -o, --output TEXT    The output file.
# 
# example use: 
#   python sms4science.py -u 'MyUsername' -p 'PaSSWord' -o 'sms.txt'
#
# author: lucy.linder <lucy.derlin@gmail.com>
# date: April 2018

import requests 
from http.cookiejar import LWPCookieJar, Cookie
from bs4 import BeautifulSoup
import click 
import logging
import sys 
import string
import re

# URL showing results for a query with perpage=200, search="", language="Swiss German"
BASE_URL = 'https://sms.linguistik.uzh.ch/sms-navigator/cgi-bin/solve.pl?selected=simple&queryType=simple&pageNumber=1&freqMode=all&view=list&urlTest=yes&query=&dummy=SMS&tagger=NO+TAGS&corpus=sms_extended_all&case=No&pageSize=200&mainLang=deu&main_de_varieties=gsw&main_fr_varieties=fra-all&main_it_varieties=ita-all&main_rm_varieties=roh-all&nonce_de_varieties=deu-all'

cookies_file = 'sms.cookies'
session = requests.Session()
session.cookies = LWPCookieJar(cookies_file)
credentials = ('', '')

def strip_punctuation(s):
    """ Remove all punctuation from a sentence (unused) """
    exclude = set(string.punctuation)
    return ''.join(ch for ch in s if ch not in exclude)


def get_html(url, page):
    """ Get the BeautifulSoup object for the given URL, doing authentification if needed """
    resp = session.get(url.format(page), auth=requests.auth.HTTPBasicAuth(*credentials))
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup 


def get_nb_pages(soup):
    """ Find the 'Page X/Y' information in the table header and extract X """
    txt = soup.select("table p b")[-1].get_text()
    regex = re.compile(".* Page 1/(\d+)")
    matches = regex.match(txt)
    if matches:
        return int(matches.group(1))
    else:
        print("Could not find number of pages")
        sys.exit(1)

@click.command()
@click.option('--username', '-u', help="Your SMS Navigator username.")
@click.option('--password', '-p', prompt=True, hide_input=True, help="Your SMS Navigator password.")
@click.option('--output', '-o', help="The output file.")
def scrape(username, password, output):
    sentences = []

    # setup credentials
    global credentials
    credentials = (username, password)

    # Update the URL to replace the page number by a placeholder
    url = re.sub(r'pageNumber=\d+', 'pageNumber={}', BASE_URL)
    # get the total number of pages
    num_pages = get_nb_pages(get_html(url, 1)) 
    # open the file
    file = open(output, 'w')
    num_sentences = 0
    # fetch each page and extract the SMS 
    print("Beginning to scrape %d pages. This might take a while..." % num_pages)
    for i in range(1, num_pages+1):
        print("processing page %d" % i)
        soup = get_html(url, i)
        # get the table rows, skipping the first one (headers)
        trs = soup.select('table + table tr')[1:]
        for tr in trs:
            tds = tr.select('td')
            # get the languages in the sms
            langs = tds[-2].text.strip()
            if langs == 'gsw;;':
                # get the last table cell (containing the actual SMS)
                sentence = tds[-1].text.strip()
                # keep only SMS with at least one letter
                file.write("%s\n" % sentence)
                num_sentences += 1
        file.flush() # ensure the results from this page are written

    file.close()
    print("found %d sentences." % num_sentences)


if __name__ == "__main__":
    scrape()