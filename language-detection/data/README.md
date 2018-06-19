# Dataset

The dataset has been created using the scripts under `/dataset`.

<img src="https://docs.google.com/drawings/d/e/2PACX-1vQuArDEmAfaOInDV6Y3FVUymfmN4h015PqJ114Bs3bpnXcsU9L8OnoiOJezDEKYM5oC8Jn2z4cODx2R/pub?w=960&amp;h=720">

### Train / test set

Created using `get_quickstart_dataset`, which will create 5 files (one per language), each containing 7387 sentences.

From leipzig: 

* `de.txt`
* `fr.txt`
* `it.txt`
* `en.txt`

From noah: 

* `sg.txt`


### SMS validation set

The validation set is taken from the Swiss SMS corpus. Two files are used, one for the recall, the other as a regular validation set.

__sms-sg.txt__: contains only Swiss German sentences. You can recreate it using:

```bash
python get_sms4science_any.py -u 'username' -p 'pwd' -o sms-sg.txt -l sg -n 200
```

__NOTE__: since there are some duplicates (14 to be exact), we also ran the following snippet to have only unique sentences:
```bash
mv sms-sg.txt sms-sg-old.txt
cat sms-sg-old.txt | sort | uniq | sort -R > sms-sg.txt
```

__sms-any.txt__: contains SMS in each of the 5 languages. Each line begins with the language code followed by a `;`. You can recreate it using:

```bash
for l in de fr en it sg; do
 python get_sms4science_any.py -u 'username' -p 'pwd' -o sms-any.txt -l $l -y -n 200
done
```

### Validation set

The files prefixed with `valid_` have been added afterwards. They each contain 2613 unseen sentences (a check has been performed to ensure there are no duplicates).

For _de_, _fr_, _it_, _en_, the content is the remaining sentences from leipzig not used for the train/test set. For _sg_, the content is a sample of sentences from the [leipzig gsw dataset from Web, 2016](http://pcai056.informatik.uni-leipzig.de/downloads/corpora/gsw-ch_web_2016_100K.tar.gz).
