import spacy
from nltk.corpus import wordnet as wn
import nltk
from nltk.corpus import stopwords

# Download nltk stopword list
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Download WordNet if not already installed
nltk.download('wordnet')

# Load spaCy large model
nlp = spacy.load("en_core_web_lg", disable=["parser", "textcat"])

# POS tag categories
CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}
FUNCTION_POS = {
    "DET", "ADP", "AUX", "CCONJ", "SCONJ", "PART", "INTJ", "X", "PRON"
}

# WordNet to spaCy POS map
WORDNET_POS_MAP = {
    wn.NOUN: "NOUN",
    wn.VERB: "VERB",
    wn.ADJ: "ADJ",
    wn.ADV: "ADV"
}

def get_wordnet_pos(lemma):
    synsets = wn.synsets(lemma)
    if not synsets:
        return None
    return WORDNET_POS_MAP.get(synsets[0].pos(), None)

def is_clean_lemma(lemma):
    return all(part.isalpha() for part in lemma.split("-")) and \
           (len(lemma) > 1 or lemma.lower() in {"a", "i"})

def process_lemmas_spacy_style(
    input_file="unique_lemmas_SUBTLEX_all_words_duplicates_excluded.txt",
    output_file_content="Content_Lemmas_Subtlex_us_unique_english.txt",
):
    with open(input_file, "r", encoding="utf-8") as f:
        lemmas = [
            l.strip()
            for l in f
            if l.strip()
        ]

    content_lemmas, function_lemmas = [], []
    unknown_pos = {}
    total_valid_lemmas = 0

    for lemma in lemmas:
        if not is_clean_lemma(lemma):
            print(f"Skipping invalid lemma: {lemma}")  # Show skipped lemmas
            continue

        total_valid_lemmas += 1

        # Function words (stopwords) override
        if lemma in stop_words:
            function_lemmas.append(lemma)
            continue

        # Capitalize lemma temporarily for POS tagging to catch proper nouns better
        lemma_cap = lemma[0].upper() + lemma[1:] if lemma else lemma

        # POS tagging using spaCy
        doc = nlp(lemma)  # For both POS and NER results
        token = doc[0]
        pos = token.pos_

        # Fallback to WordNet if spaCy returns unknown
        if not pos or pos == "X":
            wordnet_pos = get_wordnet_pos(lemma)
            if wordnet_pos:
                pos = wordnet_pos
            else:
                pos = ""

        # Special case
        if lemma in {"ye", "thee"}:
            pos = "PRON"

        # Classification
        if pos == "PROPN" or (
            (lemma_cap[0].isupper() and
             lemma not in stop_words and
             pos not in FUNCTION_POS
             and pos != "PRON")
        ):
            content_lemmas.append(lemma)
        elif pos in FUNCTION_POS:
            function_lemmas.append(lemma)
        elif pos in CONTENT_POS:
            content_lemmas.append(lemma)
        else:
            # Default assumption: treat as content word
            content_lemmas.append(lemma)
            unknown_pos[pos] = unknown_pos.get(pos, 0) + 1

    # Write outputs in lowercase as original
    with open(output_file_content, "w", encoding="utf-8") as f:
        for lemma in content_lemmas:
            f.write(lemma.lower() + "\n")

    # Summary
    print(f"Total valid lemmas processed: {total_valid_lemmas}")
    print(f"Total content lemmas: {len(content_lemmas)}")
    print(f"Total function lemmas: {len(function_lemmas)}")
    if unknown_pos:
        print(f"Total unknown POS categories encountered: {dict(unknown_pos)}")

process_lemmas_spacy_style()
