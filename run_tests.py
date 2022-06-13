import lz77
import lzw
import huffman
import deflate

basic_tests = ['', 'a', 'a'*10, 'ab'*100, 'abcbbabcbbabc',
               'abcabbbedbebbbabcbbabcb', 'ababcbababaa',
               'ababcbababa']

for algo in [lz77, lzw, huffman, deflate]:
    print(f'-------CURRENT ALGO = {algo.__name__} -------')
    for TEST_TEXT in basic_tests:
        compressed = algo.compress(TEST_TEXT)
        if algo == lz77:
            compressed = [compressed]
        DECOMPRESSED = algo.decompress(*compressed)
        # print('--- Inital  text ---', TEST_TEXT, sep='\n')
        print('___compressed___', compressed, sep='\n')
        # print('--- Decompressed text ---', DECOMPRESSED, sep='\n')
        # print(
        #     f'\nInitial text == decompressed text\n {TEST_TEXT == DECOMPRESSED}')
        assert(TEST_TEXT == DECOMPRESSED)
