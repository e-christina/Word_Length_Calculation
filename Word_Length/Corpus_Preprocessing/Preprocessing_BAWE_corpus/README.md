# BAWE Corpus Lemmatization and Preprocessing

This repository contains Python scripts used to process and lemmatize data from the British Academic Written English (BAWE) corpus. 
The scripts handle both tabular (.csv) and raw text (.txt) corpus formats to extract, clean, and deduplicate lemmas for linguistic analysis.

Reference: Nesi, H., Gardner, S., Thompson, P., & Wickens, P. (2004). The British Academic Written English (BAWE) corpus [Dataset]. Oxford, UK: University of Oxford / Oxford Text Archive. Retrieved from https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2539
Reference: Durrant, P. (n.d.). Parsed BAWE corpus [Dataset]. https://phildurrant.net/parsed-bawe-corpus/ 

## Repository Contents (according to order of execution)

| File Name | Description |
| :---      | :---        |
|`01_All_csv_BAWE_files_to_one_txt_file.py` | Uses the Polars library to read BAWE CSV files, extracting data from the 'lemma' column. 
|`02_Keep_English_words_only_BAWE.py` | Uses spaCy to parse raw BAWE text files (`.txt`). It filters valid tokens, processes hyphenated words, tallies total tokens and lemmas, and exports a list of unique lemmas.

## Data Preparation
Before running the script, you must set up your folders exactly as follows:
1. Download the corpus and extract the `.csv` files.
2. Place the extracted `BAWE_csv` folder into the `Preprocessing_BAWE_corpus` folder.

## Requirements
The 1st script, `01_All_csv_BAWE_files_to_one_txt_file.py`, requires the Polars library:

```bash
pip install polars
```

The 2nd script, `02_Keep_English_words_only_BAWE.py`, requires the following libraries:

```bash
pip install aiohttp pyenchant nltk
```