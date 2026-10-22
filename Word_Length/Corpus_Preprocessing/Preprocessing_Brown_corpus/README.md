# Brown Corpus Preprocessing and Lemmatization

This repository contains Python scripts used to process and lemmatize data from the Brown corpus(TEI XML Version), which was downloaded from https://www.nltk.org/nltk_data/ 
The scripts handle both xml and raw text (.txt) corpus formats to extract, clean, and deduplicate lemmas for linguistic analysis.

Reference: Kucera, H., & Francis, W. (1967). Computational analysis of present-day American English. Brown University Press. 

## Repository Contents (according to order of execution)

Step 01: First download and extract the Brown corpus from https://www.nltk.org/nltk_data/
Step 02: Run the scripts.

| File Name | Description |
| :---      | :---        |
|`01_Preprocess_Brown_corpus_count_tokens_lemmas_create_unique_lemma_output.py` | Extract, clean, and categorize lemmas into news, magazine, and fiction genres
|`02_Split_content_and_function_words_Brown_genres.py` | Splits the output files from previous code to all words and content word files.

## Data Preparation
Before running the script, you must set up your folders exactly as follows:
1. Download the corpus and extract the `.xml` files.
2. Place the extracted `brown_tei` folder into the `Preprocessing_Brown_corpus` folder.

## Requirements

The 1st script, `01_Preprocess_Brown_corpus_count_tokens_lemmas_create_unique_lemma_output.py`, requires Python and the spaCy library, along with its English language model:

```bash
pip install spacy
python -m spacy download en_core_web_lg
```

The 2nd script, `02_Split_content_and_function_words_Brown_genres.py`, requires the spaCy
```bash
pip install spacy nltk
```
