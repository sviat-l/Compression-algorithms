"""
LZW comression algorithm
"""


def compress(text: str) -> tuple[str, dict]:
    """
    compress text with LZW alorithms.
    Return sequence with numbers and dictionary with strings related to that numbers.

    :param text: string
    :return: result_list: string with sequence with keys devided with space ' '
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

    return ' '.join(str(x) for x in result_list), dct


def decompress(code_sequence:str, dct: dict) -> str:
    """
    decompress message with LZW algorithm
    :param code_sequence: string with sequence with keys devided by ''
    :param dct: dict with numbers as keys and related strings as values
    :return: string with decompressd text
    """
    return ''.join(dct[int(x)] for x in code_sequence.split())
