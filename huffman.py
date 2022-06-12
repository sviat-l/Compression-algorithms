"""
Module with compression and decompression algorithms by huffman coding
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


def compress(text):
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


def decompress(encoded_text: str, language_dict: dict) -> str:
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
