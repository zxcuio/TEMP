import argparse
import csv
from pathlib import Path


def titlecase_token(token: str) -> str:
    """Uppercase only the first alphabetic character in a token."""
    if not token:
        return token
    for idx, ch in enumerate(token):
        if ch.isalpha():
            return token[:idx] + ch.upper() + token[idx + 1 :]
    return token


def load_capitalized_words(path: Path) -> dict[str, str]:
    """Load mapping from lowercase word to preferred capitalized form."""
    mapping: dict[str, str] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue
            if not word[0].isupper():
                continue
            mapping[word.lower()] = word
    return mapping


def transform_csv(input_csv: Path, output_csv: Path, word_map: dict[str, str]) -> int:
    with input_csv.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        if not fieldnames:
            raise ValueError("CSV header is missing.")
        rows = list(reader)

    updated = 0
    for row in rows:
        for col in ("Word", "Headword"):
            current = row.get(col, "")
            if not current:
                continue
            preferred = word_map.get(current.lower())
            if preferred:
                if current != preferred:
                    row[col] = preferred
                    updated += 1
            elif current[0].islower() and current.lower() in word_map:
                # Fallback safeguard (normally covered above)
                row[col] = titlecase_token(current)
                updated += 1

    with output_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return updated


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Capitalize Word/Headword entries in basewords_all_pos.csv based on "
            "capitalized_words.txt"
        )
    )
    parser.add_argument(
        "--capitalized-list",
        type=Path,
        default=Path("capitalized_words.txt"),
        help="Path to capitalized_words.txt",
    )
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=Path("basewords_all_pos.csv"),
        help="Input CSV path",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("basewords_all_pos.capitalized.csv"),
        help="Output CSV path",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Overwrite --input-csv instead of writing --output-csv",
    )

    args = parser.parse_args()

    output_csv = args.input_csv if args.in_place else args.output_csv
    word_map = load_capitalized_words(args.capitalized_list)
    updates = transform_csv(args.input_csv, output_csv, word_map)

    print(f"Loaded {len(word_map)} capitalized words from {args.capitalized_list}")
    print(f"Updated {updates} cells in {output_csv}")


if __name__ == "__main__":
    main()
