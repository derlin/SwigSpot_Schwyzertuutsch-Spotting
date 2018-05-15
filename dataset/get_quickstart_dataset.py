#!/usr/bin/env python3

# -*- coding: utf-8 -*-

# This script downloads a quickstart corpus for language identification.
#
# Languages: Swiss German, English, French, German, Italian
# Sources: NOAH corpus (http://kitt.cl.uzh.ch/kitt/noah), 
#          Leipzig corpora (http://wortschatz.uni-leipzig.de/en/download/)
# 
# Notes: this script guarantees that the number of samples is the same for each language.
# To do so, it first downloads and recreate sentences from the NOAH corpus (XMl), then
# limits the number of sentences extracted from the leipzig corpora to match the ones from NOAH.
# The leipzig sentences being ordered alphabetically, a random sample is taken fro each language.
#
# author: lucy.linder <lucy.derlin@gmail.com>
# date: April 2018

import io
import urllib.request
import tarfile
import zipfile
import xml.etree.ElementTree as etree  
import logging
import re
import random
import click
import os.path
import sys


def download_into_memory(archive_url):
    # see https://stackoverflow.com/a/18624269/2667536
    stream = urllib.request.urlopen(archive_url)
    # BytesIO creates an in-memory temporary file.
    tmpfile = io.BytesIO()
    while True:
        s = stream.read(16384)
        # Once the entire file has been downloaded, tarfile returns b''
        # (the empty bytes) which is a falsey value
        if not s: break
        tmpfile.write(s)
    stream.close()
    # Reset the pointer to the beginning of the file
    tmpfile.seek(0)
    return tmpfile

def sentences_from_noah_archive(archive_url):
    logging.info("getting noah corpus from %s" % archive_url)
    tmpfile = download_into_memory(archive_url)
    zfile = zipfile.ZipFile(tmpfile)
    # keep only xml files from the archive
    files_list = [ filename 
                    for filename in zfile.namelist()
                    if re.match(r"\w+\.xml", filename.split("/")[-1]) ]
    
    sentences = []
    for filename in files_list:
        logging.debug("  extracting sentences from %s" % filename)
        # read the file from the archive and parse it as xml
        content = zfile.read(filename).decode("utf-8")
        root = etree.fromstring(content)  
        # iterate over the articles (<article>)
        for article in root:
            # reconstruct each sentence (<s>)
            for s in article: 
                try:
                    # add space between words except if the pos tag begins with $
                    # in this case, the word is actually a punctuation mark.
                    sentence = "".join([[" ", ""][w.attrib['pos'].startswith('$')] + w.text 
                        for w in s if w.text is not None])
                    # keep only sentences with at least one letter
                    if not re.match(r'[^\w0-9]+$', sentence): 
                        sentences.append(sentence.strip())
                except:
                    logging.warning("error extracting information from article n=%s", s.attrib['n'])

    logging.info("got %d sentences" % len(sentences))
    return sentences 

def sentences_from_leipzig_archives(archive_url, num_sentences=-1):
    logging.info("getting leipzig corpus from %s" % archive_url)
    tmpfile = download_into_memory(archive_url)

    # Tell the tarfile module that you're using a file object
    # that supports seeking backward.
    # r|gz forbids seeking backward; r:gz allows seeking backward
    tfile = tarfile.open(fileobj=tmpfile, mode="r:gz")

    # We only want the sentences file
    sentences_file = [filename
                    for filename in tfile.getnames()
                    if 'sentences' in filename]

    # Extract the sentences file and decode its content as an UTF-8 string
    sentences_bytes = tfile.extractfile(sentences_file[0]).read()
    sentences = sentences_bytes.decode('utf8').split("\n")

    # Clean up
    tfile.close()
    tmpfile.close()

    # get a sample
    if 0 < num_sentences < len(sentences):
        sentences = random.sample(sentences, num_sentences)
    
    # remove the number at the beginning of the sentence
    sentences = [re.sub('^[\d\s]+', '', s) for s in sentences]
    logging.info("got %d sentences" % len(sentences))
    return sentences


@click.command()
@click.option('--verbose', '-v', default=False, is_flag=True, help="Be verbose.")
@click.option('--all', '-a', default=False, is_flag=True, help="Download all instead of the same number of sentence per lang.")
@click.option('--directory', '-d', default=".", required=False, help="Output directory, default to current directory.")
def main(verbose, all, directory):

    if verbose:
        # Only enable logging if requested
        logging.basicConfig(level=logging.INFO, format="%(message)s")

    if not os.path.isdir(directory):
        print("Eror: directory %s does not exist", file=sys.stderr)
        exit(1)

    # URLs to the 5 datasets
    leipzig_datasets = [
        ("en", "http://pcai056.informatik.uni-leipzig.de/downloads/corpora/eng_wikipedia_2016_10K.tar.gz"),
        ("de", "http://pcai056.informatik.uni-leipzig.de/downloads/corpora/deu_wikipedia_2016_10K.tar.gz"),
        ("fr", "http://pcai056.informatik.uni-leipzig.de/downloads/corpora/fra_wikipedia_2010_10K.tar.gz"),
        ("it", "http://pcai056.informatik.uni-leipzig.de/downloads/corpora/ita_wikipedia_2016_10K.tar.gz"),
    ]

    noah_dataset = "http://kitt.cl.uzh.ch/kitt/noah/NOAHsCorpusOfSwissGermanDialects_Release2.0.zip"

    # get NOAH corpus first
    sentences = sentences_from_noah_archive(noah_dataset)
    num_sentences = -1 if all else len(sentences)  
    filename = os.path.join(directory, 'sg.txt')
    logging.info("writing to file %s\n" % filename)
    with io.open(filename, 'w', encoding="utf-8") as f: f.write("\n".join(sentences))

    # get LEIPZIG corpora, getting the same number of sentences as NOAH for each language 
    for (lang, url) in leipzig_datasets:
        sentences = sentences_from_leipzig_archives(url, num_sentences=num_sentences)
        filename = os.path.join(directory, '%s.txt' % lang)
        logging.info("writing to file %s\n" % filename)
        with io.open(filename, 'w', encoding="utf-8") as f: f.write("\n".join(sentences))

if __name__ == "__main__":
    main()