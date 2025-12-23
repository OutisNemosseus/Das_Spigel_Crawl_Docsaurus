"""
German word parser for extracting and translating individual words.
"""
import re
from dataclasses import dataclass
from translator import get_translator


# Common German stopwords to optionally filter out
GERMAN_STOPWORDS = {
    "der", "die", "das", "den", "dem", "des",
    "ein", "eine", "einer", "einem", "einen", "eines",
    "und", "oder", "aber", "doch", "jedoch",
    "in", "im", "an", "am", "auf", "aus", "bei", "mit", "nach", "von", "zu", "zum", "zur",
    "ist", "sind", "war", "waren", "wird", "werden", "wurde", "wurden",
    "hat", "haben", "hatte", "hatten",
    "ich", "du", "er", "sie", "es", "wir", "ihr",
    "mein", "dein", "sein", "ihr", "unser", "euer",
    "nicht", "kein", "keine", "keiner", "keinem", "keinen",
    "als", "wenn", "weil", "dass", "ob",
    "auch", "noch", "schon", "nur", "sehr", "so", "wie",
    "für", "über", "unter", "vor", "hinter", "neben", "zwischen",
}


@dataclass
class WordEntry:
    """Represents a German word with its translation."""
    german: str
    english: str
    notes: str = ""

    def to_dict(self) -> dict:
        return {
            "german": self.german,
            "english": self.english,
            "notes": self.notes
        }


def tokenize_german_text(text: str) -> list[str]:
    """
    Tokenize German text into individual words.

    Args:
        text: German text to tokenize

    Returns:
        List of words
    """
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)

    # Remove hashtags but keep the word
    text = re.sub(r'#(\w+)', r'\1', text)

    # Remove mentions
    text = re.sub(r'@\w+', '', text)

    # Split on whitespace and punctuation, keeping words
    words = re.findall(r'\b[a-zA-ZäöüÄÖÜß]+\b', text)

    return words


def extract_unique_words(text: str, include_stopwords: bool = True) -> list[str]:
    """
    Extract unique words from German text.

    Args:
        text: German text
        include_stopwords: Whether to include common stopwords

    Returns:
        List of unique words (preserving first occurrence order)
    """
    words = tokenize_german_text(text)
    seen = set()
    unique_words = []

    for word in words:
        word_lower = word.lower()
        if word_lower not in seen:
            if include_stopwords or word_lower not in GERMAN_STOPWORDS:
                seen.add(word_lower)
                unique_words.append(word)

    return unique_words


def get_word_notes(word: str) -> str:
    """
    Get grammatical notes for a German word.

    Args:
        word: German word

    Returns:
        Notes about the word (article, part of speech hints)
    """
    word_lower = word.lower()

    # Articles
    if word_lower in {"der", "die", "das", "den", "dem", "des"}:
        return "definite article"
    if word_lower in {"ein", "eine", "einer", "einem", "einen", "eines"}:
        return "indefinite article"

    # Pronouns
    if word_lower in {"ich", "du", "er", "sie", "es", "wir", "ihr"}:
        return "personal pronoun"
    if word_lower in {"mein", "dein", "sein", "ihr", "unser", "euer"}:
        return "possessive pronoun"

    # Common verbs
    if word_lower in {"ist", "sind", "war", "waren"}:
        return "verb (sein - to be)"
    if word_lower in {"hat", "haben", "hatte", "hatten"}:
        return "verb (haben - to have)"
    if word_lower in {"wird", "werden", "wurde", "wurden"}:
        return "verb (werden - to become)"

    # Prepositions
    prepositions = {"in", "im", "an", "am", "auf", "aus", "bei", "mit", "nach", "von", "zu", "zum", "zur",
                    "für", "über", "unter", "vor", "hinter", "neben", "zwischen"}
    if word_lower in prepositions:
        return "preposition"

    # Conjunctions
    if word_lower in {"und", "oder", "aber", "doch", "jedoch", "weil", "dass", "ob", "wenn", "als"}:
        return "conjunction"

    # Negation
    if word_lower in {"nicht", "kein", "keine", "keiner", "keinem", "keinen"}:
        return "negation"

    # Check for common noun patterns
    if word[0].isupper() and len(word) > 1:
        return "noun"

    # Check for common verb endings
    if word_lower.endswith(("en", "st", "t", "te", "ten")):
        return "likely verb"

    # Check for adjective endings
    if word_lower.endswith(("ig", "lich", "isch", "bar", "sam", "haft")):
        return "likely adjective"

    return ""


def parse_text_to_vocabulary(text: str, include_stopwords: bool = True) -> list[WordEntry]:
    """
    Parse German text and create vocabulary entries with translations.

    Args:
        text: German text to parse
        include_stopwords: Whether to include common stopwords

    Returns:
        List of WordEntry objects
    """
    translator = get_translator()
    words = extract_unique_words(text, include_stopwords)

    vocabulary = []
    for word in words:
        english = translator.translate_word(word)
        notes = get_word_notes(word)
        vocabulary.append(WordEntry(german=word, english=english, notes=notes))

    return vocabulary


def vocabulary_to_markdown_table(vocabulary: list[WordEntry]) -> str:
    """
    Convert vocabulary list to a Markdown table.

    Args:
        vocabulary: List of WordEntry objects

    Returns:
        Markdown table string
    """
    if not vocabulary:
        return ""

    lines = [
        "| German | English | Notes |",
        "|--------|---------|-------|"
    ]

    for entry in vocabulary:
        german = entry.german.replace("|", "\\|")
        english = entry.english.replace("|", "\\|")
        notes = entry.notes.replace("|", "\\|")
        lines.append(f"| {german} | {english} | {notes} |")

    return "\n".join(lines)


if __name__ == "__main__":
    # Test the word parser
    test_text = "Die Bundesregierung hat neue Maßnahmen zur Bekämpfung des Klimawandels angekündigt."

    print("Original text:", test_text)
    print("\nTokenized words:", tokenize_german_text(test_text))
    print("\nUnique words (with stopwords):", extract_unique_words(test_text, True))
    print("\nUnique words (without stopwords):", extract_unique_words(test_text, False))

    print("\n--- Vocabulary Table ---")
    vocabulary = parse_text_to_vocabulary(test_text)
    print(vocabulary_to_markdown_table(vocabulary))
