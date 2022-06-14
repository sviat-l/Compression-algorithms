"""
Module to create text cases and files with test results
"""
import generate_texts as gt
import random
import lz77
import lzw
import huffman
import deflate
import time


def write_tests(text_type:str, length:int, number=1,repo_name='Test_cases',  alph_len=26,
                repeat_part=.3, words=(100, 10), cyclic_len=10):
    """
    function to write text test case, with stated parameters in the related file
    :param repo_name: name of the repository to save files
    :param text_type: type for the test cases of (full_random, typical, real, cyclic, repeatetive)
    :param length: length of the text to write
    :param number: number of lines to write
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    .: paramaters: repeat_part, words, cyclic_len - related to functions in generate texst
    :param repeatetiv_part: show part of the text that contains stated repeated words
    :param word: number of words that will repeat in text, default = 100
    :param word_len: length of the repeatetiv words, default=10
    :param cyclic_len: length of the repeatetive part
    """
    func_args = {'full_random': (gt.full_random_text, (length, alph_len)),
                 'typical':     (gt.typical_text, (length, alph_len)),
                 'repeatetive': (gt.repeatetive_text, (length, repeat_part, *words, alph_len)),
                 'cyclic':      (gt.cyclic_text, (length, cyclic_len, alph_len))}

    with open(f'{repo_name}/{text_type}.txt', 'a', encoding='utf-8') as file:
        for _ in range(number):
            function, args = func_args[text_type]
            line = function(*args) + '\n'
            file.write(line)


def write_4_files():
    """
    create files with text cases for cyclic, full_random, typical, repeatetive tests
    """
    for type_test in ['cyclic', 'full_random', 'typical', 'repeatetive']:
        for length in [1,3,5,7,9, 10,30,50,70,90, 100,200,300,400,500,600,700,800,900,
                       1000,1500,2000,2500,3000,3500,4000,4500,5000,5500,6000,6500,7000,
                       7500,8000,8500,9000,9250,9500,9750,10000]:
            for j in range(5):
                cyl_len = random.choice([2,10,100, length//100, length//10]) if length>1000 else 10
                repeat_part = j/5 + 0.1
                alph_len = random.choice([3,10,20,26])
                write_tests(type_test, length=10*length, number=1, repo_name='Test_cases',
                           alph_len=alph_len, repeat_part=repeat_part, cyclic_len=cyl_len)


def write_real_text():
    """
    write string texts from real text
    note that lines length distribution is not changable
    """
    with open('Test_cases/test_string.txt', 'r', encoding='utf-8') as file:
        text = ''.join(line.strip() for line in file)

    with open('Test_cases/real.txt', 'w', encoding='utf-8') as file:
        curr_len = 0
        for length in [10,30,50,70,90, 100,300,500,700,900, 1000,2000,3000,4000,5000,6000,7000,
                  8000,9000,   10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,
                  60000,65000,70000, 75000,80000,85000,90000,92500,95000,97500,100000]:
            for _ in range(5):
                file.write(text[curr_len : curr_len + length])
                file.write('\n')
                curr_len += length


# -------------------------------------------------------------------------------------------------
# for algo in [lz77, lzw, huffman, deflate]:
#     print(f'-------CURRENT ALGO = {algo.__name__} -------')
#     for TEST_TEXT in basic_tests:
#         compressed = algo.compress(TEST_TEXT)
#         if algo == lz77:
#             compressed = [compressed]
#         DECOMPRESSED = algo.decompress(*compressed)
#         # print('--- Inital  text ---', TEST_TEXT, sep='\n')
#         print('___compressed___', compressed, sep='\n')
#         # print('--- Decompressed text ---', DECOMPRESSED, sep='\n')
#         # print(
#         #     f'\nInitial text == decompressed text\n {TEST_TEXT == DECOMPRESSED}')
#         assert(TEST_TEXT == DECOMPRESSED)

# result(algo) = (length, text type, time to compress, compression level)

def write_result():
    with open('Test_cases/test_string.txt', 'r') as f:
        text = []
        for line in f:
            text.append(line.strip())
        text = ''.join(text)
        print(len(text))
