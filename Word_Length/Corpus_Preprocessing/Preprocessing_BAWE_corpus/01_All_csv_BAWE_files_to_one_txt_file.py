#Create a list of lemmas only (duplicates are included for a start,\
# but they are excluded later in the script)
import polars as pl
from pathlib import Path

# Directory containing the CSV files
data_dir = Path("BAWE_csv")

# Directory to save the output TXT file
output_dir = Path(".")

# Set of inflected lemmas to exclude
inflected_to_exclude = {"am", "is", "are"}

# Function to check if lemma is clean
def is_clean_lemma(lemma):
    return all(part.isalpha() for part in lemma.split("-")) and \
           (len(lemma) > 1 or lemma.lower() in {"a", "i"})

all_lemmas = []
file_count = 0
total_lemmas = 0
skipped_lemmas = 0

# Process each CSV file
for csv_file in data_dir.glob("*.csv"):
    try:
        # Read only the 'lemma' column, treat '_' as null
        df = pl.read_csv(csv_file, columns=["lemma"], null_values=["_"])
        file_count += 1

        # Normalize column names
        df = df.rename({col: col.strip().lower() for col in df.columns})

        lemmas = df["lemma"].drop_nulls().to_list()
        total_lemmas += len(lemmas)

        # Clean and validate lemmas
        for l in lemmas:
            if not l:
                continue
            l = l.lower()
            if l.replace("-", "").isalpha() and is_clean_lemma(l):
                all_lemmas.append(l)
            else:
                skipped_lemmas += 1

    except Exception as e:
        print(f"Error reading {csv_file.name}: {e}")

# Deduplicate and sort
unique_lemmas = sorted(set(all_lemmas))

# Remove inflected forms
final_lemmas = [lemma for lemma in unique_lemmas if lemma not in inflected_to_exclude]

# Save unique cleaned lemmas to TXT file
txt_output_path = output_dir / "unique_lemmas_BAWE_all_words_non-English_included.txt"
with txt_output_path.open("w", encoding="utf-8") as f:
    for lemma in final_lemmas:
        if lemma:
            f.write(lemma + "\n")

# Summary
print(f"Total files processed: {file_count}")
print(f"Total lemmas found (raw): {total_lemmas}")
print(f"Unique cleaned lemmas saved: {len(final_lemmas)}")
print(f"Lemmas skipped due to invalid form: {skipped_lemmas}")
print(f"TXT file written to: {txt_output_path}")
