import csv
from typing import Dict, List


def prepare():
    """
    dictionary.pyなどをつくるために作ったメソッド
    """
    dictionary: Dict[str, List[str]] = {}
    inverted_dictionary: Dict[str, str] = {}

    with open('ngsl_words.csv') as f:
        reader = csv.reader(f)
        for row in reader:
            # 言葉の原形
            infinitiv = row[0]
            for word in row:
                if infinitiv not in dictionary:
                    dictionary[infinitiv] = []
                dictionary[infinitiv].append(word)
                inverted_dictionary[word] = infinitiv

    # print(dictionary)
    print(inverted_dictionary)
