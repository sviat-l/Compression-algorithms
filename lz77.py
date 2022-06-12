"""
Compress and decompress data with lz77 algorithm
"""


def compress(text: str, buffer_limit=10) -> tuple[int, int, str]:
    """
    compress text with lz77 algorithm
    :param text: str text to compress
    :param buffer_limit: int optional,  max length for buffer default=10
    :return: tuple( (offset, lenght, next symbol) )
    """
    result = []
    i = 0
    while True:
        offset, length = 0, 0
        buffer = 0, 0, text[max(0, i-buffer_limit): i]
        # iterate and find offset that gives the biggest length
        for j in range(1, len(buffer)+1):
            for k in range(i, len(text)):
                # compare buffer's and text's following letters
                if buffer[-j + (k-i) % j] != text[k]:   break
            if k-i > length:
                offset, length = j, k-i
        i += length + 1

        result.append((offset, length, text[i-1] if i!= len(text) + 1 else ''))
        if i >= len(text):
            return result


def decompress(sequence: tuple[int, int, str]):
    """
    decompress text from lz77 compression
    :param sequence: tuple(offset, lenght, next symbol)
    :return: string with decompressed text
    """
    result = []
    for a, b, symbol in sequence:
        if a != 0:
            result += result[-a:]*(b//a) + result[-a: -a + b%a]
        result.append(symbol)
    return ''.join(result)
