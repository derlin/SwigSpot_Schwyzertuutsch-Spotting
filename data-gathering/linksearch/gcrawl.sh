#!/bin/bash

script=googlesearch.py
key='YOUR_API_KEY'
num=100
file=results.txt

queries=(
    "das isch sone seich"
    "das isch super"
    "weiss öpper"
    "het öpper"
    "wär chamer"
)

for q in "${queries[@]}"; do 
    echo "searching for \"$q\""
    python $script -k $key -n $num -q "$q" >> $file
done
