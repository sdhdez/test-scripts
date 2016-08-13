## Usage 

```
$ python english-identification-short-texts.py titles-accents.first200-msfag.txt
```

The texts must be in tsv format, the first column is the language id (i.e. en, fr, es) and the second is the text to be categorized.

## Resources 

First [50 titles with accents](https://data.totum.one/resources/titles-accents.first50-msfag.txt)

First [100 titles with accents](https://data.totum.one/resources/titles-accents.first100-msfag.txt)

First [200 titles with accents](https://data.totum.one/resources/titles-accents.first200-msfag.txt)

First [200 titles](https://data.totum.one/resources/titles.first200-msfag.txt)

## Results 

```
$ python english-identification-short-texts.py titles-accents.first200-msfag.txt 
Method name:  guess_language
Accuracy:     0.9650
Precision:    0.9843
Recall:       0.9615
f1:           0.9728

Method name:  langdetect
Accuracy:     0.9700
Precision:    1.0000
Recall:       0.9538
f1:           0.9764

Method name:  textcat
Accuracy:     0.6800
Precision:    1.0000
Recall:       0.5077
f1:           0.6735

Method name:  langid
Accuracy:     0.8400
Precision:    1.0000
Recall:       0.7538
f1:           0.8596
```

```
$ python english-identification-short-texts.py titles.first200-msfag.txt 

Method name:  guess_language
Accuracy:     0.9850
Precision:    1.0000
Recall:       0.9850
f1:           0.9924

Method name:  langdetect
Accuracy:     0.9750
Precision:    1.0000
Recall:       0.9750
f1:           0.9873

Method name:  textcat
Accuracy:     0.8550
Precision:    1.0000
Recall:       0.8550
f1:           0.9218

Method name:  langid
Accuracy:     0.9750
Precision:    1.0000
Recall:       0.9750
f1:           0.9873

```
