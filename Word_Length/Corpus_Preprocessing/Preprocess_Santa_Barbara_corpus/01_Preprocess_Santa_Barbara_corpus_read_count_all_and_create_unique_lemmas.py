import os
import re
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_lg", disable=["parser", "textcat"])

# Folder containing .trn files
folder_path = "SBCorpus_trn"
output_path = "Preprocess_Santa_Barbara_corpus"

# Counters and sets
total_tokens = 0
total_lemmas = 0
unique_lemmas = set()

# Regex to match valid lemmas (letters, internal hyphens only)
valid_lemma_pattern = re.compile(r"[A-Za-z]+(-[A-Za-z]+)*")

# Annotation pattern: [yeah], (Hx), <YWN>, etc.
annotation_pattern = re.compile(r'\[[^\]]*\]|\([^\)]*\)|<[^>]*>')

# Function to validate clean lemmas
def is_clean_lemma(lemma):
    return all(part.isalpha() for part in lemma.split("-")) and \
           (len(lemma) > 1 or lemma.lower() in {"a", "i"})

# Process each .trn file
for filename in os.listdir(folder_path):
    if filename.endswith(".trn"):
        filepath = os.path.join(folder_path, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="windows-1252") as f:
                lines = f.readlines()

        # Collect cleaned utterances
        utterances = []
        for line in lines:
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                utterance = annotation_pattern.sub('', parts[2])  # Remove annotations
                utterances.append(utterance)

        # Process utterances with spaCy
        for doc in nlp.pipe(utterances, batch_size=1000):
            for token in doc:
                if token.is_space or token.is_punct:
                    continue
                total_tokens += 1
                lemma = token.lemma_.strip()
                if valid_lemma_pattern.fullmatch(lemma) and is_clean_lemma(lemma):
                    total_lemmas += 1
                    unique_lemmas.add(lemma.lower())
                else:
                    print(f"Skipping invalid lemma: {lemma}")

# Capitalize first letter of each unique lemma
capitalized_lemmas = sorted({lemma.capitalize() for lemma in unique_lemmas})

# Output to file
output_file = os.path.join(output_path, "unique_lemmas_Santa_Barbara_corpus_all_words.txt")
with open(output_file, "w", encoding="utf-8") as out_file:
    for lemma in capitalized_lemmas:
        out_file.write(lemma + "\n")

# Summary
print(f"Total tokens: {total_tokens}")
print(f"Total lemmas: {total_lemmas}")
print(f"Unique lemmas: {len(unique_lemmas)}")
print(f"Output saved to: {output_file}")
print(f"Number of .trn files found: {len([f for f in os.listdir(folder_path) if f.endswith('.trn')])}")
