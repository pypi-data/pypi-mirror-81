from typing import Optional
from ngsl.inverted_dictionary import INVERTED_DICTIONARY


def include(word: str) -> bool:
    """
    Return if word is in NGSL
    """
    return word in INVERTED_DICTIONARY


def get_infinitiv(word: str) -> Optional[str]:
    """
    Return the infinitiv of the word
    """
    return INVERTED_DICTIONARY[word] if include(word) else None
