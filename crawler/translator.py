"""
Translation module using deep-translator for German to English translation.
"""
from deep_translator import GoogleTranslator
import time


class GermanTranslator:
    """Translator for German to English using Google Translate (free)."""

    def __init__(self):
        self.translator = GoogleTranslator(source='de', target='en')
        self._cache = {}  # Cache translations to avoid repeated API calls

    def translate_text(self, text: str) -> str:
        """
        Translate German text to English.

        Args:
            text: German text to translate

        Returns:
            English translation
        """
        if not text or not text.strip():
            return ""

        # Check cache first
        if text in self._cache:
            return self._cache[text]

        try:
            translation = self.translator.translate(text)
            self._cache[text] = translation
            return translation
        except Exception as e:
            print(f"Translation error: {e}")
            return f"[Translation failed: {text}]"

    def translate_word(self, word: str) -> str:
        """
        Translate a single German word to English.

        Args:
            word: German word to translate

        Returns:
            English translation of the word
        """
        if not word or not word.strip():
            return ""

        # Clean the word
        clean_word = word.strip().lower()

        # Check cache
        if clean_word in self._cache:
            return self._cache[clean_word]

        try:
            # Add small delay to avoid rate limiting
            time.sleep(0.1)
            translation = self.translator.translate(clean_word)
            self._cache[clean_word] = translation
            return translation
        except Exception as e:
            print(f"Word translation error for '{word}': {e}")
            return word  # Return original word if translation fails

    def translate_words_batch(self, words: list[str]) -> dict[str, str]:
        """
        Translate multiple words and return a dictionary.

        Args:
            words: List of German words

        Returns:
            Dictionary mapping German words to English translations
        """
        translations = {}
        for word in words:
            if word and word.strip():
                translations[word] = self.translate_word(word)
        return translations


# Global translator instance
_translator = None


def get_translator() -> GermanTranslator:
    """Get or create the global translator instance."""
    global _translator
    if _translator is None:
        _translator = GermanTranslator()
    return _translator


def translate_german_to_english(text: str) -> str:
    """
    Convenience function to translate German text to English.

    Args:
        text: German text

    Returns:
        English translation
    """
    return get_translator().translate_text(text)


if __name__ == "__main__":
    # Test translations
    translator = GermanTranslator()

    test_texts = [
        "Die Bundesregierung hat neue Maßnahmen angekündigt.",
        "Guten Tag, wie geht es Ihnen?",
        "Das Wetter ist heute sehr schön."
    ]

    print("Testing German to English translation:\n")
    for text in test_texts:
        translation = translator.translate_text(text)
        print(f"German: {text}")
        print(f"English: {translation}")
        print()
