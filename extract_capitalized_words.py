import csv
from pathlib import Path

INPUT = Path('basewords_all_pos.csv')
OUTPUT = Path('capitalized_words.txt')

# Lowercase words that are generally capitalized even when POS is not marked as proper noun.
ALWAYS_CAPITALIZED = {
    'i': 'I',
    # Months
    'january': 'January', 'february': 'February', 'march': 'March', 'april': 'April',
    'may': 'May', 'june': 'June', 'july': 'July', 'august': 'August',
    'september': 'September', 'october': 'October', 'november': 'November', 'december': 'December',
    # Weekdays
    'monday': 'Monday', 'tuesday': 'Tuesday', 'wednesday': 'Wednesday',
    'thursday': 'Thursday', 'friday': 'Friday', 'saturday': 'Saturday', 'sunday': 'Sunday',
}


def titlecase_token(token: str) -> str:
    """Title-case a token while preserving leading apostrophes."""
    if not token:
        return token
    if token[0].isalpha():
        return token[0].upper() + token[1:]
    if len(token) > 1 and token[1].isalpha():
        return token[0] + token[1].upper() + token[2:]
    return token


def capitalize_word(word: str) -> str:
    """Capitalize multi-part words (hyphen/space/slash separated)."""
    separators = ['-', ' ', '/']
    parts = [word]
    sep_used = None
    for sep in separators:
        if sep in word:
            sep_used = sep
            parts = word.split(sep)
            break

    if sep_used is None:
        return titlecase_token(word)

    return sep_used.join(titlecase_token(part) for part in parts)


capitalized = set()
with INPUT.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        word = row['Word'].strip().lower()
        pos = row['POS'].strip().lower()

        if word in ALWAYS_CAPITALIZED:
            capitalized.add(ALWAYS_CAPITALIZED[word])

        # Exhaustive extraction: include every word tagged as proper noun.
        if 'proper noun' in pos:
            capitalized.add(capitalize_word(word))

with OUTPUT.open('w', encoding='utf-8') as f:
    for word in sorted(capitalized):
        f.write(word + '\n')

print(f'Wrote {len(capitalized)} words to {OUTPUT}')
