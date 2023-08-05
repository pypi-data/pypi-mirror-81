import re

from abc import ABC, abstractmethod


class BasePhoneticsAlgorithm(ABC):
    _vowels = ''
    __reduce_regex = re.compile(r'(\w)(\1)+', re.I)
    __latin2cyrillic_table = str.maketrans('AOao', 'АОао')

    def _reduce_seq(self, seq):
        return self.__reduce_regex.sub(r'\1', seq)

    def _latin2cyrillic(self, seq):
        return seq.translate(self.__latin2cyrillic_table)

    @abstractmethod
    def transform(self, word):
        """
        Converts a given word to phonetic code
        :param word: string
        :return: string code
        """
        return None
