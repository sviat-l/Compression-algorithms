"""
Module with compression and decompression algorithms by deflate coding
"""
import heapq


class Node:
    """
    Node class for binary tree
    """

    def __init__(self, freq, symbol='', left=None, right=None) -> None:
        """
        Init values for binary tree node:
            left, right children, symbol and frequent number
        """
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol

    def __lt__(self, other) -> bool:
        return self.freq < other.freq

    def __le__(self, other) -> bool:
        return self.freq <= other.freq

    def __eq__(self, other) -> bool:
        return self.freq == other.freq

    def __repr__(self) -> str:
        return f"Node(freq={self.freq}, symbol={self.symbol})"


def create_tree(frequency_dct):
    """
    Create and return binary tree from frequency dictionary
    :param frequency_dct: dictionary with occurancy number
    """
    tree_nodes = [Node(freq, s) for s, freq in frequency_dct.items()]
    if len(tree_nodes) == 1:
        return Node(0, '', tree_nodes[0])
    heapq.heapify(tree_nodes)
    while len(tree_nodes) > 1:
        rnode = heapq.heappop(tree_nodes)
        lnode = heapq.heappop(tree_nodes)
        heapq.heappush(tree_nodes, Node(
            lnode.freq + rnode.freq, '', lnode, rnode))
    return tree_nodes[0] if tree_nodes else None


def find_codes(node: Node, code: list, dct: dict) -> dict:
    """
    find codes for letters from binary tree using recursion
    :param node: binary tree node
    :param code: list with code sequnce for symbol
    :param dct: dictionary with translation keys
    :return: dictionary with translation keys
    """
    if node.symbol:
        dct[node.symbol] = code
    if node.left:
        dct = find_codes(node.left, code + ['0'], dct)
    if node.right:
        dct = find_codes(node.right, code + ['1'], dct)
    return dct


def lz77_compress(text: str, buffer_limit=10) -> tuple[int, int, str]:
    """
    compress text with lz77 algorithm
    :param text: str text to compress
    :param buffer_limit: int optional, max length for buffer, default=10
    :return: tuple[(offset, lenght, next symbol)]
    """
    result = []
    i = 0
    while True:
        offset, length = 0, 0
        buffer = text[max(0, i-buffer_limit): i]
        # iterate and find offset that gives the biggest length
        for j in range(1, len(buffer)+1):
            for k in range(i, len(text)):
                # compare buffer's and text's following letters
                if buffer[-j + (k-i) % j] != text[k]:
                    break
            if k-i > length:
                offset, length = j, k-i
        i += length + 1

        result.append((offset, length, text[i-1] if i!= len(text) + 1 else ''))
        if i >= len(text):
            return result


def huffman_compress(text):
    """
    Compress data with huffman coding

    :param text: string with decoded text
    :return param encoded_text: string with (0,1) sequence
    :return param language_dct: dictionary for translating from one language to another
     keys - letters in initial alphabet, values encoded letters  ex.: {'a':'01'...}
    """
    freq_dct = {}
    for symbol in text:
        freq_dct[symbol] = freq_dct.get(symbol, 0) + 1

    huffman_tree = create_tree(freq_dct)
    if not huffman_tree:
        return '', {}

    encode_dct = find_codes(huffman_tree, [], {})
    language_dict = {s: ''.join(code) for s, code in encode_dct.items()}
    encoded = ''.join(language_dict[s] for s in text)
    return encoded, language_dict


def huffman_decompress(encoded_text: str, language_dict: dict) -> str:
    """
    decompress text from huffman compression
    with language transformation dictionary

    :param encoded_text: string with (0,1) sequence
    :param language_dct: dictionary for translating from one language to another
     keys - letters in initial alphabet, values encoded letters  ex.: {'a':'01'...}
    :return: string with decoded text
    """
    language_dict = {code: s for s, code in language_dict.items()}
    decoded = []
    current_string = ''
    for symbol in encoded_text:
        tmp = current_string + symbol
        if tmp in language_dict:
            decoded.append(language_dict[tmp])
            tmp = ''
        current_string = tmp
    return ''.join(decoded)


def lz77_decompress(sequence: tuple[int, int, str]):
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

def compress(text)-> tuple[ tuple[int, int, str], dict[str:str]]:
    """
    compress data with deflate algorithm
    :param text: string text to compress
    return (sequence, huffman_dict)
    :return: sequence: tuple(offset, lenght, next symbol) from lz77 algorithm
    :return: huffman_dict: dictionary for translating huffman encoding
    """
    # return tuple(map(lambda x: (lz77_compress(x[0]), x[1]), [huffman_compress(text)]))[0]
    huffman_encoded, huffman_dict = huffman_compress(text)
    sequence = lz77_compress(huffman_encoded)
    return sequence, huffman_dict

def decompress(sequence: tuple[int, int, str], huffman_dict: dict[str:str]):
    """
    decompress data with deflate algorithm
    :param sequence: tuple(offset, lenght, next symbol) from lz77 algorithm
    :param huffman_dict: dictionary for translating huffman encoding
    """
    return huffman_decompress(lz77_decompress(sequence), huffman_dict)
