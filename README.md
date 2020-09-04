# Triplette-markov
Based on [markovify](https://github.com/jsvine/markovify/).

Markov chain experiment in python.
Lunch break fun project.

## Generate base *.json
- Place txt files in input
- Run
```
python generate.py -l <language code for spacy, it_core_news_lg> -d <depth, [2 - 3]>
```
- Wait for the process to finish

## Create text:
```
python index.py -d <depth [2 - 3]> -l <lenght of rows> -t <total texts> -o <output-filename>
```
- Example:
```
python index.py -d 3 -l 10 -t 10 -o test
```

## Upload:
- Create an `.env` file like `.env-sample` and add your dropbox token, then run:
```
python upload.py
```
