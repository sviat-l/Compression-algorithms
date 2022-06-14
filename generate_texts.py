"""
Module to generate texts with different conditions
"""

from functools import lru_cache
import random

POSSIB_DISTRIBUTION = [('e', 11.16), ('a', 8.492), ('r', 7.576), ('i', 7.544), ('o', 7.163),
                ('t', 6.950), ('n', 6.654), ('s', 5.735), ('l', 5.489), ('c', 4.538),
                ('u', 3.630), ('d', 3.384), ('p', 3.167), ('m', 3.012), ('h', 3.003),
                ('g', 2.470), ('b', 2.072), ('f', 1.812), ('y', 1.777), ('w', 1.289),
                ('k', 1.101), ('v', 1.007), ('x', 0.290), ('z', 0.272), ('j', 0.196), ('q', 0.196)]

def users_letters_possibilities():
    """
    get letters occurrance chance for an alphabeth from user
    """
    inpt = input('Print letters and their occurance related numbers.\
                  \nTo end press Enter. Use format below {letter}|{number}\
                  \nExamples:\na|2\nb|0.7\n\n>>> ')
    letter_possibility = []
    while inpt:
        try:
            letter, number = inpt.split('|')
            number = float(number)
        except ValueError:
            print('OOps wrong input')

        letter_possibility.append((letter, number))
        inpt = input('>>> ')
    return sorted(letter_possibility, key=lambda x:-x[1])

@lru_cache()
def letters_distribution(length):
    """
    return distibution with stated possibilies for letters
    with stated alpabet length
    """
    sum_poss = sum(x[1] for x in POSSIB_DISTRIBUTION[:length])
    distibution, current_poss =[], 0
    for j in range(length):
        current_poss += POSSIB_DISTRIBUTION[j][1]/sum_poss
        distibution.append((POSSIB_DISTRIBUTION[j][0], current_poss))
    return distibution

def typical_text(length: int, alphabet_len=26):
    """
    random text with stated letter occurancy relation
    :param length: length of the text to return
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    """
    def get_letter(possibility, distribution):
        for letter, poss in distribution: #change to binary search
            if possibility < poss:
                return letter
    distr = letters_distribution(alphabet_len)
    return ''.join( get_letter(random.random(), distr) for _ in range(length))

def full_random_text(length:int, alphabet_len=26):
    """
    text with each letter the same possibile occurance
    :param length: length of the text to return
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'[:alphabet_len]
    return ''.join(random.choice(alphabet) for _ in range(length))

# ------------------------------------------------------------------------------------------------


def repeatetive_text(length:int, repeatetive_part = .3, words=100, word_len=10, alphabet_len=26):
    """
    return string that contains generated repeated words in some proportion
    :param length: length of the text to return
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    :param repeatetiv_part: show part of the text that contains stated repeated words
    :param word: number of words that will repeat in text, default = 100
    :param word_len: length of the repeatetiv words, default=10
    :return: string with text some part of which consists of repeted words
    """
    alp = 'abcdefghijklmnopqrstuvwxyz'[:alphabet_len]
    # generate words that will repeat in text
    repeatetive_words = [[random.choice(alp) for _ in range(word_len)] for _ in range(words)]
    result = []
    while length > len(result):
        if random.random() < repeatetive_part/word_len:
            result += random.choice(repeatetive_words)
        else:
            result.append(random.choice(alp))
    return ''.join(result[:length])


def cyclic_text(length:int, cyclic_len=10, alphabet_len=26):
    """
    return string that consists in full of repeated words
    :param length: length of the text to return
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    :param cyclic_len: length of the repeatetive part
    :return: string with repeated text
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz'[:alphabet_len]
    word = ''.join(random.choice(alphabet) for _ in range(cyclic_len))
    return word*(length//cyclic_len) + word[:length%cyclic_len]
