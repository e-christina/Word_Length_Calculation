# Santa Barbara Corpus 

Reference: Du Bois, J. W., Chafe, W. L., Meyer, C., Thompson, S. A., Englebretson, R., & Martey, N. (2000–2005). Santa Barbara corpus of spoken American English, parts 1–4 [Dataset]. Linguistic Data Consortium. 

This script processes transcriptions from the publicly available Santa Barbara Corpus of Spoken American English. 

## Data Source
The original transcription (`.trn`) files for the Santa Barbara Corpus are publicly available. 
You can download them here: https://www.linguistics.ucsb.edu/research/santa-barbara-corpus-spoken-american-english

## Repository Contents (according to order of execution)

| File Name | Description |
| :---      | :---        |
|'01_Preprocess_Santa_Barbara_corpus_read_count_all_and_create_unique_lemmas.py'|Extracts, cleans, and lemmatizes the spoken words while stripping out conversational annotations.
|'02_Split_content_and_function_words_SBCorpus.py'| Uses NLTK's English stopword list for filtering, followed by spaCy's `en_core_web_lg` model for Part-of-Speech (POS) tagging. If a word's POS is ambiguous, the script falls back to NLTK's WordNet lexical database for verification.

## Data Preparation
Before running the script, you must set up your folders exactly as follows:
1. Download the corpus and extract the `.trn` files.
2. Create a folder named `SBCorpus_trn` in the exact same directory as this script.
3. Place all the extracted `.trn` files into the `SBCorpus_trn` folder.
4. Move the extracted files into your project folder 'Preprocess_Santa_Barbara_corpus".

## Requirements

The 2nd script, '02_Split_content_and_function_words_SBCorpus.py', requires Python and the following libraries:

```bash
pip install spacy nltk
python -m spacy download en_core_web_lg
```