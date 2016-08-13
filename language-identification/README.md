## Usage 

```
$ python english-identification-short-texts.py titles-accents.first200-msfag.txt
```

The texts must be in tsv format, the first column is the language id (i.e. en, fr, es) and the second is the text to be categorized.

## Resources 

First [200 titles in English](https://data.totum.one/resources/titles.first200-msfag.txt).

First [200 titles not only English](https://data.totum.one/resources/titles.others200-msfag.txt).

First [200 titles with accents](https://data.totum.one/resources/titles-accents.first200-msfag.txt), more than one language.

## Results 

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

Python lib: 	custom1
Precision:  	1.0000
Recall:     	0.9750
f1:         	0.9873

Python lib: 	custom2
Precision:  	1.0000
Recall:     	0.9750
f1:         	0.9873

```

```
$ python english-identification-short-texts.py titles.others200-msfag.txt 
Python lib: 	guess_language
Precision:  	0.8969
Recall:     	0.9667
f1:         	0.9305

Python lib: 	langdetect
Precision:  	0.8854
Recall:     	0.9444
f1:         	0.9140

Python lib: 	textcat
Precision:  	0.8060
Recall:     	0.6000
f1:         	0.6879

Python lib: 	langid
Precision:  	0.9231
Recall:     	0.9333
f1:         	0.9282

Python lib: 	custom1
Precision:  	0.9231
Recall:     	0.9333
f1:         	0.9282

Python lib: 	custom2
Precision:  	0.9231
Recall:     	0.9333
f1:         	0.9282

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

Python lib: 	custom1
Precision:  	0.9843
Recall:     	0.9615
f1:         	0.9728

Python lib: 	custom2
Precision:  	1.0000
Recall:     	0.9538
f1:         	0.9764

```
