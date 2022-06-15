"""
Module to create text cases and files with test results
"""
import random
import time
import generate_texts as gt
import lz77
import lzw
import huffman
import deflate


def write_tests(text_type:str, length:int, number=1,repo_name='Test_cases',  alph_len=26,
                repeat_part=.3, words=(100, 10), cyclic_len=10):
    """
    function to write text test case, with stated parameters in the related file
    :param repo_name: name of the repository to save files
    :param text_type: type for the test cases of (full_random, typical, real, cyclic, repeatetive)
    :param length: length of the text to write
    :param number: number of lines to write
    :param alphabet_len: number of letters in our alphabet, <27, default=26
    ..: paramaters: repeat_part, words, cyclic_len - related to functions in generate texst
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

def get_test_result_data(text:str, algo):
    """
    get test results parameters
    :param text: string to compress
    :param algo: algorithm to use for compression
    """
    # calculating time to compress data
    st_time = time.time()
    compressed = algo.compress(text)
    compress_time = time.time() - st_time
    # find aproximately compressed data ratio
    if algo==deflate:
        compressed_text_size =sum(pair[0].bit_length() for pair in compressed[0])
    elif algo==huffman:
        compressed_text_size = len(compressed[0])
    elif algo==lzw:
        compressed_text_size = sum(int(x).bit_length() for x in compressed[0].split()) +\
                               len(''.join(compressed[1].values()))
    elif algo==lz77:
        compressed_text_size = sum(sum( x.bit_length() for x in pair[:2]) for pair in compressed)+\
                                    len(compressed)*8
        compressed = [compressed]
    compression_level = 1- compressed_text_size/(8*len(text))

    # calculating time to decompress data
    st_time = time.time()
    decompressed = algo.decompress(*compressed)
    decompress_time = time.time() - st_time

    if decompressed != text:
        return "!!!WRONG ANSVER!!!"
    return len(text), compress_time, decompress_time, compression_level

def write_results(algorithms:list,test_types:list, save_path:str, test_path:str):
    """
    write test results for all file types and allalgorithms
    safa data in csv in format: length, compress_time,decompress_time, compression_level
    :param algorithms: list with algorithms to comapare
    :param test_types: list with data type charasteristics
    :param save_path: directory path to safe results
    :param test_path: directory path to get test cases
    """
    for tpt in test_types:
        with open(f'{test_path}{tpt}.txt', 'r', encoding='utf-8') as read_file:
            text = [line.strip() for line in read_file]
            for algo in algorithms:
                with open(f'{save_path}{algo.__name__}.csv', 'a', encoding='utf-8') as write_file:
                    write_file.write(f'---{tpt}---test cases---\n')
                    for line in text:
                        test_result = get_test_result_data(line, algo)
                        write_file.write('  ,  '.join(str(x) for x in test_result))
                        write_file.write('\n')


ALGORITHMS = [lz77, lzw, huffman, deflate]
TEST_TYPES = ['cyclic', 'full_random', 'typical', 'repeatetive', 'real']
SAVE_PATH = 'Tests_results/'
TEST_PATH = 'Test_cases/'
