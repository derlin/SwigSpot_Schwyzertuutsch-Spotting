#!/bin/bash

script=startpage.py
num=100
command=links
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
    python $script -n $num -q "\"$q\"" $command >> $file
done
