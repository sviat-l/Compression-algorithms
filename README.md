# _Compression algorithms_
_Implemented most popular compression algorithms and presented results\
Each algorithm is implemented in eponymous files_

</br>

## LZ77
The main idea is that you look backward in data to find repeating of the following symbols in the buffer. Save compressed data in a sequence of tuples (offset, length, next symbol).
1. offset - shows how many symbols back you should go back
2. length - shows how many symbols you must copy from the offset marker. If it is more than offset, then it goes into a cycle
3. next symbol - a letter that you should add after copping

 Example:
```bash
Initial: 'a a b b b c a b a b c b c'

Encoded: (0, 0, 'a'), (1, 1, 'b'), (1, 2, 'c'), (5, 2, 'a'), (5, 2, 'b'), (0, 0, 'c')
```

</br>

## LZW
The feature of this algorithm is that we create a dictionary to encode/decode text.\
We are looking from the current symbol to the following and find if the string that they form is in the dictionary. If yes, we add its key to the result. If not, we add the substring to the dictionary.

Example:
```bash
Initial: 'a b c a b a c b c b a b c'

Encoded: '0 1 2 3 0 2 4 1 3 2'

{0: 'a', 1: 'b', 2: 'c', 3: 'ab', 4: 'bc', 5: 'ca', 6: 'aba', 7: 'ac', 8: 'cb', 9: 'bcb', 10: 'ba', 11: 'abc'})
```

</br>

## Huffman
It is a simple but effective algorithm.
- Find how many times each symbol is repeated in the text
- Create 
Huffman binary tree
- Match letters with their codes

So that symbols with a higher appearance rate will be encoded with shorter code in the prefix code set, and the average length will be the least.

Example:
```bash
Initial: 'a b c d d d b c b b b b a'

Encoded: '000100101010110011111000'

{'a': '000', 'c': '001', 'd': '01', 'b': '1'})
```

</br>

## Deflate
It is a widely distributed, modified algorithm that combines LZ77 and Huffman coding. That is why deflate encoding provides a higher ratio for compression.
1. Encode data with the Huffman algorithm
2. Use LZ77 to encode the sequence of { 0|1 }

```bash
Initial: 'd b c b a b c b b c a b a a a'

Huffman: '0111010100101011010001000000'

{'a': '00', 'c': '010', 'd': '011', 'b': '1'}

Deflate: (0, 0, '0'), (0, 0, '1'), (1, 2, '0'), (2, 4, '0'), (7, 5, '1'), (10, 4, '0'), (4, 4, '0'), (1, 1, '0')
```

</br>

## Tests
To test scripts were created, more than 1000 tests were in text format with strings of different lengths and formats. Related functions to create test strings are implemented in [generate_texts.py](../main/generate_texts.py) and saved in directory [Test_cases.](../main/Test_cases)

There are cases of 5 types:
1. Full random - letters chouses absolutely randomly
2. Typical - with distribution for letter occurrence possibility
3. Real - text from real documents, books
4. Cyclic - all text consists of one string repeated many times
5. Repetitive - there are words in a string that repeats many times among randomly chosen letters.

</br>

## Results
Algorithms were tested on different strings and its results were saved in directory: [Tests_results](../main/Test_results) in .csv files
- Functions to run tests and write results, are implemented in [run_tests.py](../main/run_tests.py).
- Visualised results were created with module [visualization.py](../main/visualization.py)

### Compress

<p align="center"><img width="520" height="390" src="../main/Plots/Compress time.png"></p>

- As we can see, all algorithms have linear time complexity to compress and decompress text string O(n), n=length. But with different constants.
- LZ77 and, consequently, Deflate algorithms have the bigger constant and take more time to compress data.
- The fastest compress algorithm is Huffman. It works ~10 times faster than others.

### Decompress
<p align="center"><img width="520" height="390" src="../main/Plots/Decompress time.png"></p>

- In contrast, Huffman and, consequently, Deflate algorithms have the bigger constant to decompress data.
- LZ77 and LZW work 3-5 times faster than Huffman and Deflate
- LZW is the fastest algorithm to compress and decompress data.

### Compressing rate
<p align="center"><img width="520" height="390" src="../main/Plots/Compress ratio.png"></p>

- All algorithms have a higher compression rate for cyclic text and a few higher for repetitive, with a slight difference between real and random tests.
- Huffman algorithm has the less difference beetwen cyclic test cases and other
<p align="center"><img width="520" height="390" src="../main/Plots/Compress ratio/lzw.png"></p>

- On the contrary, LZW is extremely effective for cyclic tests

### By types

<p align="center"><img width="520" height="390" src="../main/Plots/Compress time/lz77.png"></p>

- Full random texts take the most time to encode, while cyclic are
- Repetitive tests are easier to compress but not so much as real and typical tests

<p align="center"><img width="520" height="390" src="../main/Plots/Decompress time/huffman.png"></p>
- In decompression the difference is even less, but cyclic tests still are easier to decompress in ~1.5 times

</br>
</br>

More plots are saved in [Plots](../main/Plots) repositoty.
