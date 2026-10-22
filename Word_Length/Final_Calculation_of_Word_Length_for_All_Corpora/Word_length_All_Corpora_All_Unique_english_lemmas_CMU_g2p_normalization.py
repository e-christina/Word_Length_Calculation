import csv
import os
import datetime
import nltk
import nltk
nltk.download("averaged_perceptron_tagger_eng")
from nltk.corpus import cmudict
from g2p_en import G2p

# -----------------------------
# INIT RESOURCES
# -----------------------------
cmu_dict = cmudict.dict()
g2p = G2p()

# -----------------------------
# UNIFIED PHONOLOGICAL MODEL
# -----------------------------

VOWELS = {
    "AA","AE","AH","AO","AW","AY",
    "EH","ER","EY","IH","IY",
    "OW","OY","UH","UW"
}

def normalize_phonemes(phoneme_list):
    """
    Strip stress markers so CMU and G2P are comparable
    AH0 -> AH, EH1 -> EH
    """
    return [p.strip("012") for p in phoneme_list]


def count_syllables_from_phonemes(phonemes):
    """
    Single unified syllable definition:
    = vowel nucleus counting
    """
    phonemes = normalize_phonemes(phonemes)

    count = 0
    for p in phonemes:
        if p in VOWELS:
            count += 1

    return max(count, 1)


# -----------------------------
# CMU PATH (gold standard)
# -----------------------------
def cmu_syllables(word):
    word = word.lower()

    if word in cmu_dict:
        return max(
            count_syllables_from_phonemes(pron)
            for pron in cmu_dict[word]
        )

    return None


# -----------------------------
# G2P PATH (fallback)
# -----------------------------
def g2p_syllables(word):
    phonemes = g2p(word)
    return count_syllables_from_phonemes(phonemes)


# -----------------------------
# MAIN SYLLABLE FUNCTION
# -----------------------------
def count_syllables(word):
    """
    Unified pipeline:
    1. CMUdict (human gold standard)
    2. G2P fallback (ML prediction)
    """

    word = word.lower()

    syllables = cmu_syllables(word)
    if syllables is not None:
        return syllables, "CMUdict"

    return g2p_syllables(word), "g2p_en"


# -----------------------------
# CORPUS PROCESSING
# -----------------------------
def process_file(corpus_name, filepath):
    data = []

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            lemma = line.strip()

            if lemma:
                # orthographic length (your chosen definition)
                length_letters = sum(c.isalpha() or c == '-' for c in lemma)

                syllables, method = count_syllables(lemma)

                data.append([
                    corpus_name,
                    lemma,
                    length_letters,
                    syllables,
                    method
                ])

    return data


# -----------------------------
# FILE LIST
# -----------------------------
corpus_files = {
    "Brown_Fiction": "Brown_Fiction_unique_lemmas_all_words.txt",
    "Brown_Magazine": "Brown_Magazine_unique_lemmas_all_words.txt",
    "Brown_News": "Brown_News_unique_lemmas_all_words.txt",
    "SUBTLEX_us": "unique_lemmas_SUBTLEX_all_words_duplicates_excluded.txt",
    "Santa_Barbara": "unique_lemmas_Santa_Barbara_corpus_all_words.txt",
    "BAWE": "unique_lemmas_BAWE_English_words_only.txt",
}

# -----------------------------
# RUN PIPELINE
# -----------------------------
all_results = []

for corpus, path in corpus_files.items():
    if os.path.exists(path):
        print(f"Processing {corpus}...")
        all_results.extend(process_file(corpus, path))
    else:
        print(f"Missing file: {path}")


# -----------------------------
# OUTPUT
# -----------------------------
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
output_file = f"All_Corpora_All_unique_english_Lemmas_CMU_G2P_With_Normalization{timestamp}.csv"

with open(output_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "Corpus",
        "Lemma",
        "Length_Letters",
        "Syllables",
        "Method"
    ])
    writer.writerows(all_results)

print(f"Saved to: {os.path.abspath(output_file)}")