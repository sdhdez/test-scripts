## Usage 

```
$ python english-identification-short-texts.py titles-accents.first200-msfag.txt
```

The texts must be in tsv format, the first column is the language id (i.e. en, fr, es) and the second is the text to be categorized.

## Resources 

First [50 titles with accents](https://data.totum.one/resources/titles-accents.first50-msfag.txt) (all are in english).

First [100 titles with accents](https://data.totum.one/resources/titles-accents.first100-msfag.txt) (all are in english).

First [200 titles with accents](https://data.totum.one/resources/titles-accents.first200-msfag.txt).

First [200 titles](https://data.totum.one/resources/titles.first200-msfag.txt) (all are in english).

## Results 

```
$ python english-identification-short-texts.py titles-accents.first50-msfag.txt 
Python lib: guess_language
Precision:    1.0000
Recall:       1.0000
f1:           1.0000

Python lib: langdetect
Precision:    1.0000
Recall:       0.9600
f1:           0.9796

Python lib: textcat
Precision:    1.0000
Recall:       0.5800
f1:           0.7342

Python lib: langid
Precision:    1.0000
Recall:       0.7400
f1:           0.8506
```

```
$ python english-identification-short-texts.py titles-accents.first100-msfag.txt 
Python lib: guess_language
Precision:    1.0000
Recall:       0.9600
f1:           0.9796

Python lib: langdetect
Precision:    1.0000
Recall:       0.9600
f1:           0.9796

Python lib: textcat
Precision:    1.0000
Recall:       0.4500
f1:           0.6207

Python lib: langid
Precision:    1.0000
Recall:       0.7600
f1:           0.8636
```

```
$ python english-identification-short-texts.py titles-accents.first200-msfag.txt 
Python lib:  guess_language
Precision:    0.9843
Recall:       0.9615
f1:           0.9728

Python lib:  langdetect
Precision:    1.0000
Recall:       0.9538
f1:           0.9764

Python lib:  textcat
Precision:    1.0000
Recall:       0.5077
f1:           0.6735

Python lib:  langid
Precision:    1.0000
Recall:       0.7538
f1:           0.8596
```

```
$ python english-identification-short-texts.py titles.first200-msfag.txt 

Python lib:  guess_language
Precision:    1.0000
Recall:       0.9850
f1:           0.9924

Python lib:  langdetect
Precision:    1.0000
Recall:       0.9750
f1:           0.9873

Python lib:  textcat
Precision:    1.0000
Recall:       0.8550
f1:           0.9218

Python lib:  langid
Precision:    1.0000
Recall:       0.9750
f1:           0.9873
```
