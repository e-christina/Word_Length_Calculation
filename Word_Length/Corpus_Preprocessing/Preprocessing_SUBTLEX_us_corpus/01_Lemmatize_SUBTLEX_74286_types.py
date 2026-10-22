import spacy

# Load English spaCy model
nlp = spacy.load("en_core_web_sm", disable=["parser", "ner", "textcat"])

# Input and output file paths
input_file = "SUBTLEX_us_74286_word_TYPES.txt"
output_file = "lemmatized_SUBTLEX_us_raw_all_words_duplicates_included.txt"

# Read input words
with open(input_file, "r", encoding="utf-8") as f:
    words = [line.strip() for line in f if line.strip()]

# Lemmatize and collect unique lemmas
lemmas = set()
for word, doc in zip(words, nlp.pipe(words, batch_size=1000)):
    for token in doc:
        lemma = token.lemma_
        if word.isupper():
            lemma = lemma[0].upper() + lemma[1:]
        elif word[0].isupper():
            lemma = lemma[0].upper() + lemma[1:]
        lemmas.add(lemma)

# Write unique lemmas to output file
with open(output_file, "w", encoding="utf-8") as f:
    for lemma in sorted(lemmas):
        f.write(lemma + "\n")

print(f"Lemmas written to {output_file}")
