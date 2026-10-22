SUBTLEX-US
The SUBTLEX-US word-frequency list (Brysbaert & New, 2009) was used as the source dataset.

The original word-form list was lemmatized. The processing procedure is documented in the script in this repository.
The original dataset is not redistributed here. Please consult the original source and its applicable terms of use to obtain the data.

Reference:
Brysbaert, M., & New, B. (2009). Moving beyond Kučera and Francis: A critical evaluation of current word frequency norms and the introduction of a new and improved word frequency measure for American English. Behavior Research Methods, 41, 977–990.The SUBTLEXus frequency list can be obtained here: https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus

## Repository Contents (according to order of execution)

Step 01: First download and extract the SUBTLEX-US corpus (in .txt form) from (Original source) https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexus
Step 02: Run the scripts.

| File Name | Description |
| :---      | :---        |
|`01_Lemmatize_SUBTLEX_74286_types.py` | Lemmatize and deduplicate types.
|`02_Split_content_and_function_words_SUBTLEX_us.py` | Splits the output file from previous code to all words and content word files.

## Data Preparation
Before running the script, you must set up your folders exactly as follows:
1. Download the corpus and extract the `.txt` file.
2. Place the extracted `SUBTLEXus74286wordstextversion.txt` file into the `Preprocessing_SUBTLEX_us_corpus` folder.
3. Name the `SUBTLEXus74286wordstextversion.txt` file as 'SUBTLEX_us_74286_word_TYPES.txt'.

## Requirements

The 1st script, `01_Lemmatize_SUBTLEX_74286_types.py`, requires the spaCy library, along with its small English language model:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

The 2nd script, `02_Split_content_and_function_words_SUBTLEX_us.py`, requires the spaCy library and NLTK.

```bash
pip install spacy nltk
python -m spacy download en_core_web_lg
```
