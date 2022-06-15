# _Compression algorithms_
_Implemented most popular compression algorithms and presented results\
Each algorithm is implemented in eponymous files_

</br>

## LZ77
The main idea is that you look backward in data to find repeating of next symbols in buffer. Save compressed data in sequence of tuples (offset, length, next symbol).
1. offset - shows on how many symbols back you should go back
2. length - shows how many symbols you must copy from offset marker, if it is more than offset, than it goes in cycle
3. next symbol - letter that you should add after copping

 Example:
```bash
Initial: 'a a b b b c a b a b c b c'

Encoded: (0, 0, 'a'), (1, 1, 'b'), (1, 2, 'c'), (5, 2, 'a'), (5, 2, 'b'), (0, 0, 'c')
```

</br>

## LZW
The feature for this algorithm is that we create dictionary to encode / decode text.\
We are looking from current symbol to the following and find if string that they form is in dictionary, if yes we add its key to result, if not we add substring to the dictionary.

Example:
```bash
Initial: 'a b c a b a c b c b a b c'

Encoded: '0 1 2 3 0 2 4 1 3 2'

{0: 'a', 1: 'b', 2: 'c', 3: 'ab', 4: 'bc', 5: 'ca', 6: 'aba', 7: 'ac', 8: 'cb', 9: 'bcb', 10: 'ba', 11: 'abc'})
```

</br>

## Huffman
It is simple but effective algorithm.
- Find how many times each symbol is repeated in text
- Create huffman binary tree
- Match letters with their codes

So that symbols with higher appereance rate will be encoded with shorter code in prefic code set, and the average length will be the lest.

Example:
```bash
Initial: 'a b c d d d b c b b b b a'

Encoded: '000100101010110011111000'

{'a': '000', 'c': '001', 'd': '01', 'b': '1'})
```

</br>

## Deflate
It is widely distibruted, modyfied algorithm that combines LZ77 and Huffman coding. That is why deflate encoding provides higher ratio for compression.
1. Encode data with huffman algorithm
2. Use LZ77 to encode sequence of { 0|1 }

```bash
Initial: 'd b c b a b c b b c a b a a a'

Huffman: '0111010100101011010001000000'

{'a': '00', 'c': '010', 'd': '011', 'b': '1'}

Deflate: (0, 0, '0'), (0, 0, '1'), (1, 2, '0'), (2, 4, '0'), (7, 5, '1'), (10, 4, '0'), (4, 4, '0'), (1, 1, '0')
```

</br>

## Tests
To test scripts were created more than 1000 tests, in text format with strings different length and format. Related functions to create test strings are implemented in [generate_texts.py](/generate_texts.py) and saved in directory [Test_cases.](Test_cases)

There are cases of 5 types:
1. Full random - letters chouses absolutely randomly
2. Typical - with distribution for letter occurance possibility
3. Real - text from real documents, books
4. Cyclic - all text consists of one string repeated many times
5. Repeatetive - there are words in string that repeats many time amoung randomly choosen letters.

</br>

## Results
Algorithms were tested on different strings and its results were saved in directory: [Tests_results](Test_results) in .csv files
- Functions to run tests and write results, are implemented in [run_tests.py](run_tests.py).
- Visualised results were created with module [visualization.py](visualization.py)

### Compress
[FOTO1]()

- As we can see all algorithms has linear time complexity to compress and decompress text string O(n), n=length. But with different constants.
- LZ77 and, consequently, Deflate algorithms have the bigger constant and take more time to compress data.
- The fastet compress algorithm is huffman it works in ~10 times faster than other.

### Decompress
[FOTO2]()
- On contrast, Huffman and, consequently, Deflate algorithms have the bigger constant to to decompress data.
- LZ77 and LZW work in 3-5 times faster than Huffman and Deflate
- LZW is the fastest algorithm to compress and decompress date.

### Compressing rate
[FOTO3]()
- All algorithms has higher compression rate for cyclic text, and a few higher for repeatetive, with small difference beetwen real and random tests.
- Huffman algorithm has the less difference beetwen cyclic test cases and other
- On the contrary, LZW is extremely effective for cyclic tests

### By types
[FOTO3]()
- Full random texts take the most time to encode, while cyclic are
- Repeatetive tests are easier to compress but not so much than real and typical tests
- In decompression the difference is even less, but cyclic tests still are easier to decompress in ~1.5 times



More plots are saved in [Plots](Plots) repositoty.

