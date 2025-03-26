# Permutation Lookup Service

A toy web service that accepts an input string, and returns all known permutations of that string from an internal word list file.

## Implementation

See [app.py](app.py).

Summary: at startup, the application loads a word list file into a dictionary (hash table) as follows:
- each key is a character-sorted string.
- each value is the list of permutations of that string from the word list file.

Subsequently, this dictionary supports constant-time lookup of known permutations.

## Pre-Requisites

Install Python 3. This application was developed and tested with Python 3.13.1.

## Startup

```
python3 app.py -f mywordlist.txt
```

or,

```
./app.py -f mywordlist.txt
```

## Usage

While the service is running, open a browser window to `http://localhost:8000/permutations?word=abc`, or use curl:

```
curl "localhost:8000/permutations?word=abc"
```
