"""
Brown Corpus Lemma Extraction by Genre

This script processes the publicly available Brown Corpus (TEI XML format) to
extract, clean, and categorize lemmas into news, magazine, and fiction genres.

Data Source:
The Brown Corpus data used in this project was downloaded via NLTK (Natural
Language Toolkit) in TEI XML format.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_lg")

# Brown Corpus genre prefixes mapped to categories, per manual (Brown Corpus in TEI XML format)
genres = {
    # News-related genres
    'a': 'news',  # News (Press: Reportage)
    'b': 'news',  # Editorial (Press: Editorial)
    'c': 'news',  # Reviews (Press: Reviews)

    # Magazine-like genres
    'e': 'magazine',      # Hobbies (Skills and Hobbies)
    'f': 'magazine',      # Popular Lore
    'g': 'magazine',      # Belles Lettres

    # Fiction genres
    'k': 'fiction',       # Fiction (General Fiction)
    'l': 'fiction',       # Mystery (Mystery and Detective Fiction)
    'm': 'fiction',       # Science Fiction
    'n': 'fiction',       # Adventure (Adventure and Western Fiction)
    'p': 'fiction',       # Romance (Romance and Love Story)
    'r': 'fiction',       # Humor

    # Excluded genres (not mapped / ignored)
    # 'd': Religion
    # 'h': Government (Miscellaneous)
    # 'j': Learned (Academic)
}

# Valid pattern: alphabetic and hyphenated alphabetic (e.g., well-known)
valid_lemma_pattern = re.compile(r"^[A-Za-z]+(-[A-Za-z]+)*$")

# Token filter: alphabetic and hyphenated only
def is_valid_token(token):
    return (
        not token.is_space
        and not token.is_punct
        and not token.like_num
        and valid_lemma_pattern.match(token.text)
    )

# Lemma filter: only alphabetic or hyphenated; allow "a", "i" as single letters
def is_clean_lemma(lemma):
    return all(part.isalpha() for part in lemma.split("-")) and \
           (len(lemma) > 1 or lemma.lower() in {"a", "i"})

# Extract words from TEI <text> element
def get_clean_text(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    ns = {'tei': 'http://www.tei-c.org/ns/1.0'}
    words = [elem.text for elem in root.findall(".//tei:text//tei:w", ns) if elem.text]
    return ' '.join(words)

# Main corpus processing function
def process_corpus(input_folder, output_folder):
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)

    genre_stats = {
        genre: {'tokens': 0, 'lemmas': 0, 'unique_lemmas': set()}
        for genre in set(genres.values())
    }

    for file_path in Path(input_folder).glob("*.xml"):
        prefix = file_path.name[0].lower()
        if prefix in genres:
            genre = genres[prefix]
            clean_text = get_clean_text(file_path)
            if clean_text:
                doc = nlp(clean_text)

                tokens = [token.text for token in doc if is_valid_token(token)]
                lemmas = [
                    token.lemma_.lower()
                    for token in doc
                    if is_valid_token(token) and is_clean_lemma(token.lemma_)
                ]

                genre_stats[genre]['tokens'] += len(tokens)
                genre_stats[genre]['lemmas'] += len(lemmas)
                genre_stats[genre]['unique_lemmas'].update(lemmas)

    for genre, stats in genre_stats.items():
        filename = f"Brown_{genre.capitalize()}_unique_lemmas_all_words.txt"
        file_path = output_path / filename
        with open(file_path, "w", encoding="utf-8") as f:
            for lemma in sorted(stats['unique_lemmas']):
                f.write(lemma.capitalize() + "\n")

        print(f"\n{genre.upper()} STATS:")
        print(f"Total tokens: {stats['tokens']}")
        print(f"Total valid lemmas: {stats['lemmas']}")
        print(f"Unique valid lemmas: {len(stats['unique_lemmas'])}")
        print(f"Lemmas saved to: {file_path.name}")

# Set input/output folders
input_folder = r"brown_tei"
output_folder = r"Preprocessing_Brown_corpus"

# Run the script
process_corpus(input_folder, output_folder)
