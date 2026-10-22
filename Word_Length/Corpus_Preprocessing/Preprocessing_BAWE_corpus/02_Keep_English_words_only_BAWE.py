import asyncio
import aiohttp
import json
import os
import re
from enchant.checker import SpellChecker
from nltk.corpus import wordnet as wn

# Initialize spellcheckers
us_checker = SpellChecker("en_US")
uk_checker = SpellChecker("en_GB")

# Load lemmas
with open("unique_lemmas_BAWE_all_words_non-English_included.txt", "r", encoding="utf-8") as f:
    lemmas = [line.strip() for line in f]  # keep original casing for output

# Load or initialize Wiktionary cache
cache_file = 'wiktionary_cache.json'
if os.path.exists(cache_file):
    with open(cache_file, 'r', encoding='utf-8') as cf:
        wiktionary_cache = json.load(cf)
else:
    wiktionary_cache = {}

english_words = set()
wiktionary_words = set()
to_lookup = []

# Regex to detect allowed characters:
# Only basic Latin letters (a-z, A-Z), digits, hyphen and apostrophe allowed
allowed_chars_re = re.compile(r"^[a-zA-Z0-9\-\']+$")

def is_english_word(word):
    """Check if word contains ONLY allowed English chars"""
    return bool(allowed_chars_re.match(word))

def is_english_component(part):
    """Check if a single word part is English via spellchecker, WordNet, or cache"""
    lower_part = part.lower()
    if us_checker.check(lower_part) or uk_checker.check(lower_part):
        return True
    if wn.synsets(lower_part):
        return True
    if lower_part in wiktionary_cache and wiktionary_cache[lower_part]:
        return True
    return False

# Classify lemmas
for word in lemmas:
    word = word.strip()

    # Skip words with disallowed characters (accents, Greek, etc.)
    if not is_english_word(word):
        continue

    lower_word = word.lower()
    is_english = False

    # Quick checks for non-hyphenated or simple words
    if "-" not in lower_word:
        if us_checker.check(lower_word) or uk_checker.check(lower_word):
            is_english = True
            english_words.add(word)
            continue

        if wn.synsets(lower_word):
            is_english = True
            english_words.add(word)
            continue

        if lower_word in wiktionary_cache and wiktionary_cache[lower_word]:
            is_english = True
            english_words.add(word)
            wiktionary_words.add(lower_word)
            continue

    else:
        # For hyphenated words, check how many components are English
        parts = lower_word.split("-")
        english_parts_count = sum(is_english_component(part) for part in parts)

        # New logic:
        # - 2 parts: accept if at least 1 part English
        # - 3 or more parts: accept if at least 2 parts English
        if (len(parts) == 2 and english_parts_count >= 1) or (len(parts) >= 3 and english_parts_count >= 2):
            is_english = True
            english_words.add(word)

    # If still not English, queue for Wiktionary lookup
    if not is_english:
        to_lookup.append(lower_word)

# Stats report
print(f"{len(lemmas)} total lemmas")
print(f"{len(english_words)} identified by spellchecker, WordNet, hyphen-parts heuristic, or cached Wiktionary")
print(f"{len(to_lookup)} will be checked via Wiktionary")

# Async Wiktionary fetch function
async def fetch_wiktionary(session, word):
    url = f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}"
    try:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                is_english = bool(data)
            else:
                is_english = False
    except Exception:
        is_english = False
    return word, is_english

async def main():
    added_now = 0
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_wiktionary(session, word) for word in to_lookup]

        for i, task in enumerate(asyncio.as_completed(tasks), 1):
            word, is_english = await task
            wiktionary_cache[word] = is_english
            if is_english:
                english_words.add(word)
                wiktionary_words.add(word)
                added_now += 1

            # Progress
            if i % 100 == 0 or i == len(to_lookup):
                print(f"Checked {i}/{len(to_lookup)} words")

            # Periodic cache write
            if i % 100 == 0 or i == len(to_lookup):
                with open(cache_file, 'w', encoding='utf-8') as cf:
                    json.dump(wiktionary_cache, cf)

    return added_now

# Run Wiktionary checks
new_wiki_additions = asyncio.run(main())

# Final cache save
with open(cache_file, 'w', encoding='utf-8') as cf:
    json.dump(wiktionary_cache, cf)

# Save final English lemmas (capitalize first letter)
with open("unique_lemmas_BAWE_English_words_only.txt", "w", encoding="utf-8") as f:
    for w in sorted(english_words, key=lambda x: x.lower()):
        f.write(w.capitalize() + "\n")

# Final stats
print(f"Total English words saved: {len(english_words)}")
print(f"Total words added from Wiktionary this run: {new_wiki_additions}")
print(f"Words already cached from Wiktionary: {len(wiktionary_words) - new_wiki_additions}")






