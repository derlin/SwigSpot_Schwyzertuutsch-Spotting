#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# This script downloads all the Swiss German SMS from sms4sciences.
# To use it, you must have an account and be able to access the SMS Navigator.
#
# Invoke the program with --help for a list of available options.
# 
# Example use: 
#   python sms4science.py -u 'MyUsername' -p 'PaSSWord' -o 'sms.txt'
#
# To construct a dataset with X samples for each language, you can do:
#
#   for l in de fr en it sg; do
#     python ~/git/SwigSpot/dataset/get_sms4science_any.py -u 'user' -p 'pass' -o sms.txt -l $l -y -n X
#   done
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
import io


# URL showing results for a query
BASE_URL = 'https://sms.linguistik.uzh.ch/sms-navigator/cgi-bin/solve.pl?selected=simple&queryType=simple&pageNumber={{page}}&freqMode=all&view=list&urlTest=yes&query=&dummy=SMS&tagger=NO+TAGS&corpus=sms_extended_all&case=No&pageSize=200&mainLang={mainLang}&main_de_varieties={de_variety}&main_fr_varieties=fra-all&main_it_varieties=ita-all&main_rm_varieties=roh-all&nonce_de_varieties=deu-all'

lang_parameters = {
    'de': dict(code="deu", mainLang="deu", de_variety="deu"),
    'fr': dict(code="fra", mainLang="fra", de_variety="deu-all"),
    'en': dict(code="eng", mainLang="eng", de_variety="deu-all"),
    'it': dict(code="ita", mainLang="ita", de_variety="deu-all"),
    'sg': dict(code="gsw", mainLang="deu", de_variety="gsw"),
    'any': dict(code="", mainLang="", de_variety="deu-all"),
}

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
    resp = session.get(url.format(page=page), auth=requests.auth.HTTPBasicAuth(*credentials))
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

@click.command(help="Download SMS from the sms4science's SMS Navigator into a text file.")
@click.option('--username', '-u', help="Your SMS Navigator username.")
@click.option('--password', '-p', prompt=True, hide_input=True, help="Your SMS Navigator password.")
@click.option('--lang', '-l', type=click.Choice(lang_parameters.keys()), default='sg', help="The language to download.")
@click.option('--num', '-n', type=int, default=-1, help="Maximum number of results. Use -1 for no limit.")
@click.option('--labels', '-y', is_flag=True, default=False, help="Print language labels at the beginning of each sentence.")
@click.option('--multi', '-m', is_flag=True, default=False, help="Take any SMS, not only monolingual ones.")
@click.option('--words', '-w', type=int, default=3, help="Min number of words for an SMS to be retained.")
@click.option('--output', '-o', help="The output file.")
def scrape(username, password, lang, num, labels, multi, words, output):
    sentences = set()
 
    # setup credentials
    global credentials
    credentials = (username, password)

    # Update the URL to replace the page number by a placeholder
    url = BASE_URL.format(**lang_parameters[lang])
    if lang == 'any': url.replace('mainLang=', '') # remove lang param alltogether

    # set a filter to get only monolingual SMS in the specified language
    if lang == 'any':
        lang_filter = '^(deu|gsw|ita|fra|eng);;$'
    else:
        lang_filter = '^%s;;$' % lang_parameters[lang]['code']

    # open the file (in append mode)
    if output is None:
        output = "%s.txt" % lang
    file = io.open(output, 'a+', encoding="utf-8")

    # setup counter
    num_sentences = 0
    pages = 1 # number of pages 
    page  = 1 # current page

    # fetch each page and extract the SMS 
    print("Beginning to scrape pages (max=%d, lang=%s). This might take a while..." % (num, lang_filter))
    while page <= pages and (num <= 0 or num_sentences < num):
        print("processing page %d" % page)
        soup = get_html(url, page)
        if page == 1:
            # get the total number of pages
            pages = get_nb_pages(soup) 

        # get the table rows, skipping the first one (headers)
        trs = soup.select('table + table tr')[1:]
        for tr in trs:
            tds = tr.select('td')
            # get the languages in the sms
            langs = tds[-2].text.strip()
            if multi or re.match(lang_filter, langs):
                # get the last table cell (containing the actual SMS)
                sentence = tds[-1].text.strip()
                if len(sentence.split()) >= words and sentence not in sentences:
                    sentences.add(sentence)
                    # more than 'words' words and not a duplicate. Save the sentence.
                    if labels: 
                        # print labels, i.e. language of the SMS at the beginning
                        if langs.startswith('gs'): file.write('sg;')
                        else:  file.write('%s;' % langs[:2])
                    file.write("%s\n" % sentence)
                    num_sentences += 1
                    print("+1", num_sentences)
                    if num > 0 and num <= num_sentences:
                        print("break", num, num_sentences)
                        break
        file.flush() # ensure the results from this page are written
        page += 1

    file.close()
    print("found %d sentences." % num_sentences)


if __name__ == "__main__":
    scrape()