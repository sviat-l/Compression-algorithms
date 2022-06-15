# _Compression algorithms_
_Implemented most popular compression algorithms and presented results\
Each algorithm is implemented in eponymous files_

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


Results:
(/main/Plots/Compress time/lz77.png)
(/main/Plots/Decompress time/lz77.png)

## LZW
The feature for this algorithm is that we create dictionary to encode / decode text.\
We are looking from current symbol to the following and find is string that they form is in dictionary, if yes we add its key to result, if not we add substring to the dictionary.

Example:
```bash
Initial: 'a b c a b a c b c b a b c'

Encoded: '0 1 2 3 0 2 4 1 3 2'

{0: 'a', 1: 'b', 2: 'c', 3: 'ab', 4: 'bc', 5: 'ca', 6: 'aba', 7: 'ac', 8: 'cb', 9: 'bcb', 10: 'ba', 11: 'abc'})
```

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
## Tests
To test scripts were created more than 1000 tests, in text format with strings different length and format. Related functions to create test strings are implemented in [generate_texts.py](/generate_texts.py) and saved in directory [Test_cases.](Test_cases)

There are cases of 5 types:
1. Full random - letters chouses absolutely randomly
2. Typical - with distribution for letter occurance possibility
3. Real - text from real documents, books
4. Cyclic - all text consists of one string repeated many times
5. Repeatetive - there are words in string that repeats many time amoung randomly choosen letters.

## Results
Algorithms were tested on different strings and its results were saved in directory: [Tests_results](Test_results) in .csv files.
Functions to run tests and write results, are implemented in [run_tests.py](run_tests.py).
Visualised results were created with module [visualization.py](visualization.py) and saved in [Plots](Plots) reporetoty.
[FOTO1]()
[FOTO2]()
[FOTO3]()
