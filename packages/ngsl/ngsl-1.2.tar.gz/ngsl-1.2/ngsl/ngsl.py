from typing import Optional, List, Set
from ngsl.inverted_dictionary import INVERTED_DICTIONARY, DICTIONARY


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


def get_infinitiv_list(words: List[str]) -> Set[str]:
    result: List[str] = []
    for word in words:
        infinitiv: Optional[str] = get_infinitiv(word=word)
        if infinitiv is None:
            continue
        result.append(infinitiv)
    return set(result)


def all_infinitiv() -> List[str]:
    """
    Return all word that belongs to NGSL.
    """
    return DICTIONARY.keys()
