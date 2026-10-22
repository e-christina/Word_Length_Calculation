import spacy
from nltk.corpus import wordnet as wn
import nltk
from nltk.corpus import stopwords

# Download nltk resources
nltk.download('stopwords')
nltk.download('wordnet')

# Load stopwords
stop_words = set(stopwords.words('english'))

# Load spaCy large model
nlp = spacy.load("en_core_web_lg", disable=["parser", "textcat"])

# POS tag categories
CONTENT_POS = {"NOUN", "VERB", "ADJ", "ADV", "PROPN"}
FUNCTION_POS = {
    "DET", "ADP", "AUX", "CCONJ", "SCONJ", "PART", "INTJ",
    "X", "PRON"
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

def classify_lemmas(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lemmas = [
            l.strip().capitalize()
            for l in f
            if l.strip()
        ]

    content_lemmas, function_lemmas = [], []
    unknown_pos = {}
    total_valid_lemmas = 0

    for lemma in lemmas:
        if not is_clean_lemma(lemma):
            print(f"Skipping invalid lemma: {lemma}")
            continue

        total_valid_lemmas += 1

        if lemma.lower() in stop_words:
            function_lemmas.append(lemma)
            continue

        doc = nlp(lemma)
        token = doc[0]
        pos = token.pos_

        if not pos or pos == "X":
            wordnet_pos = get_wordnet_pos(lemma.lower())
            if wordnet_pos:
                pos = wordnet_pos
            else:
                pos = ""

        if lemma.lower() in {"ye", "thee"}:
            pos = "PRON"

        if pos in {"SYM", "NUM"}:
            continue

        if pos == "PROPN" or (
            lemma[0].isupper() and
            lemma.lower() not in stop_words and
            pos not in FUNCTION_POS and
            pos != "PRON"
        ):
            content_lemmas.append(lemma)
        elif pos in FUNCTION_POS:
            function_lemmas.append(lemma)
        elif pos in CONTENT_POS:
            content_lemmas.append(lemma)
        else:
            content_lemmas.append(lemma)
            unknown_pos[pos] = unknown_pos.get(pos, 0) + 1

    with open(output_file, "w", encoding="utf-8") as f:
        for lemma in content_lemmas:
            f.write(lemma + "\n")

    print(f"\nProcessed: {input_file}")
    print(f"Total valid lemmas: {total_valid_lemmas}")
    print(f"Total content lemmas: {len(content_lemmas)}")
    print(f"Total function lemmas: {len(function_lemmas)}")
    if unknown_pos:
        print(f"Unknown POS encountered: {dict(unknown_pos)}")


def process_lemmas_spacy_style():
    # Added "Preprocessing_Brown_corpus/"
    files = [
        ("Preprocessing_Brown_corpus/Brown_Fiction_unique_lemmas_all_words.txt",
         "Preprocessing_Brown_corpus/Content_Lemmas_Brown_Fiction.txt"),
        ("Preprocessing_Brown_corpus/Brown_Magazine_unique_lemmas_all_words.txt",
         "Preprocessing_Brown_corpus/Content_Lemmas_Brown_Magazine.txt"),
        ("Preprocessing_Brown_corpus/Brown_News_unique_lemmas_all_words.txt",
         "Preprocessing_Brown_corpus/Content_Lemmas_Brown_News.txt"),
    ]

    for input_file, output_file in files:
        classify_lemmas(input_file, output_file)


# Run it
process_lemmas_spacy_style()