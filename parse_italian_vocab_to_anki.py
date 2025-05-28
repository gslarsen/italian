import pdfplumber
import re

# === CONFIGURABLE PARAMETERS ===
PDF_PATH = "2222-words.pdf"  # Change this to your PDF file path
OUTPUT_PATH = "2222-words-anki-output.txt"
START_PAGE = 7  # Zero-based (so 9 = 10th page in most readers)
END_PAGE = 348  # Inclusive, so 349 = last page to extract

# === SCRIPT STARTS HERE ===


def extract_entries(text):
    # Matches lines like: 1- Grande – Big
    entry_pattern = re.compile(r"^\d+\s*[-–]\s*(\w+)\s*[-–]\s*(\w+)", re.MULTILINE)
    # To store tuples: (English, Italian, Italian example, English example)
    cards = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # Match entry lines
        m = re.match(r"^\d+\s*[-–]\s*(.+?)\s*[-–]\s*(.+)", line)
        if re.match(r"^\d+", line) and not m:
            print("Missed possible entry:", line)
        if m:
            italian = m.group(1).strip()
            english = m.group(2).strip()
            # Next two lines are usually the example sentences
            italian_sentence = ""
            english_sentence = ""
            if i + 1 < len(lines):
                italian_sentence = lines[i + 1].strip()
            if i + 2 < len(lines):
                english_sentence = lines[i + 2].strip()
            # Build the card: (Front, Back)
            front = english
            back = f"{italian}<br>{italian_sentence}<br>{english_sentence}"
            cards.append((front, back))
            i += 3  # Skip past the example lines
        else:
            i += 1
    return cards


with pdfplumber.open(PDF_PATH) as pdf:
    # Pages are 0-indexed
    full_text = ""
    for pageno in range(START_PAGE, END_PAGE + 1):
        page = pdf.pages[pageno]
        full_text += page.extract_text() + "\n"

cards = extract_entries(full_text)

# Write to Anki format file
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for front, back in cards:
        f.write(f"{front}\t{back}\n")

print(f"Done! Extracted {len(cards)} cards. File ready for Anki: {OUTPUT_PATH}")
