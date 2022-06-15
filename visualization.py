"""
Module to create graphs to compare test results
"""
from matplotlib  import pyplot as plt


ALGORITHMS = ['lz77', 'lzw', 'huffman', 'deflate']
TEST_TYPES = ['cyclic', 'full_random', 'typical', 'repeatetive',]
RESULT_PATH = 'Tests_results/'
COLOURS = {'cyclic':'b', 'full_random' :'g', 'typical': 'r', 'repeatetive' : 'y',
           'lz77':'b', 'lzw' :'g', 'huffman': 'r', 'deflate' : 'y'}
PLOT_TYPES_DICT ={'Compress time':[1, 1000], 'Decompress time':[2, 1000], 'Compress ratio':[3,1]}


def get_graph_data(algorithm:str, plot_type:str):
    """
    return dictionary with results for tests

    :param algorithm: string with algorithm name
    :param plot_type: determind dependency format (length, f(length))
    ..: one of (Compress time, Decmpress time, Compress ratio)
    :param save: bool value, if False - show the plot

    Return:
        dictionary with keys test format name and values result tuple
        {test format:(time, compress value),...}
    """
    dct_results = {}
    with open(f'{RESULT_PATH}{algorithm}.csv', 'r', encoding='utf-8') as res_file:
        for _ in range(4):
            tests_type = res_file.readline().split('---')[1]
            dct_results[tests_type] = [], []
            for _ in range(40):
                value_average = 0
                # get avarage time for compression for stated length
                for _ in range(5):
                    test_result_data = res_file.readline().strip().split('  ,  ')
                    lng = int(test_result_data[0])
                    compress_value = float(test_result_data[PLOT_TYPES_DICT[plot_type][0]])\
                                                           *PLOT_TYPES_DICT[plot_type][1]
                    value_average += compress_value/5
                dct_results[tests_type][0].append(lng)
                dct_results[tests_type][1].append(value_average)
    return dct_results


def algo_graph_data(algorithm:str, plot_type:str):
    """
    return tuple with results for tests

    :param algorithm: string with algorithm name
    :param plot_type: determind dependency format (length, f(length))
    ..: one of (Compress time, Decmpress time, Compress ratio)
    :param save: bool value, if False - show the plot

    Return:
        tuple with length list, and compress value for that lengths
        ([times], [compress values])
    """
    all_values_dct = get_graph_data(algorithm, plot_type)
    length_list = all_values_dct['full_random'][0]
    compress_values = [(sum(all_values_dct[key][1][l] for key in all_values_dct))/5
                        for l in range(len(length_list))]
    return length_list, compress_values



def create_graphs(graph_type:str, algorithm=None, save=False):
    """
    create and save grapth with results for testes
    (compression value, test_length) for each data format or algorithm
    :param algorithm: string with algorithm name or None
        if value not None then labels are algorithms names
        if None then plot for one algorithms results in different test formats
    :param graph_type: determind dependency format (length, f(length))
    ..: one of (Compress time, Decmpress time, Compress ratio)
    :param save: bool value, if False - show the plot

    return None
    """
    if algorithm:
        data_dct = get_graph_data(algorithm, graph_type)
        plt.title(f'{algorithm}')
        save_path = f"Plots/{graph_type}/{algorithm}"
    else:
        data_dct = {algo:algo_graph_data(algo, graph_type) for algo in ALGORITHMS}
        plt.title(f'{graph_type}')
        save_path = f"Plots/{graph_type}"

    plt.grid(color='grey', linestyle='dashdot', linewidth=0.2)
    plt.xlabel('text length')
    plt.ylabel(f'{graph_type}, ms' if graph_type!= 'Compress ratio' else f'{graph_type}' )
    for lable, data in data_dct.items():
        plt.plot(data[0], data[1], label=lable, color=COLOURS[lable])
    plt.legend()
    if save:
        plt.savefig(save_path)
    else:
        plt.show()
    plt.clf()


def main(save_value:bool):
    """
    main function to draw all graphs

    :param save_value: bool value, True if want save graphs,
        False if you want just to see them
    """
    for plot_type in PLOT_TYPES_DICT:
        for algo in ALGORITHMS:
            create_graphs(plot_type,algorithm=algo, save=save_value)
        create_graphs(plot_type,algorithm=None, save=save_value)

if __name__ == '__main__':
    SAVE = False
    main(SAVE)
