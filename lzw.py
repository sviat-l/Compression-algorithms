"""
LZW comression algorithm
"""

def compress(text: str) -> tuple[list, dict]:
    """
    compress text with LZW alorithms.
    Return sequence with numbers and dictionary with strings related to that numbers.

    :param text: string
    :return: result_list: list with sequence with keys
    :return: dct: dict with numbers as keys and related strings as values
    """

    dct, current_dct_code = {}, 0
    # initialize dictionary with used patterns
    for symbol in text:
        if symbol not in dct:
            dct[symbol] = current_dct_code
            current_dct_code += 1

    current_string, result_list = '', []
    for symbol in text:
        # look for current string + next letter
        tmp = current_string + symbol
        if tmp in dct:
            # continue with adding one letter to the string
            current_string = tmp
        else:
            # add elements to result list and dct, continue with string = last letter
            dct[tmp] = current_dct_code
            result_list.append(dct[current_string])
            current_dct_code += 1
            current_string = symbol

    # add last string index to the ansver
    if current_string:
        result_list.append(dct[current_string])
    # reverse dictionary
    dct = {value: key for key, value in dct.items()}

    return result_list, dct


def decompress(compressed_data: tuple[list, dict]) -> str:
    """
    decompress message with LZW algorithm
    :param compressed_data: tuple: (code_sequence, dct)
    :param code_sequence: list with sequence with keys
    :param dct: dict with numbers as keys and related strings as values
    :return: string with decompressd text
    """
    return ''.join(compressed_data[1][x] for x in compressed_data[0])
