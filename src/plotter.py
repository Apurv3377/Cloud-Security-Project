import csv
import os

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


def find_min_max_range(dict_y_axis):
    global_min = 1234687987  # default value to make sorting work for general range of values.
    global_max = 0
    range = 6
    for key, y_axis_list in dict_y_axis.items():
        if global_min <= min(y_axis_list):
            global_min = global_min;
        else:
            global_min = min(y_axis_list)
        if global_max >= max(y_axis_list):
            global_max = global_max;
        else:
            global_max = max(y_axis_list)

    return global_min, global_max, ((global_max - global_min) / range)


def plot_graph(filename):
    x_axis = []
    y_axis = []
    dic_y = {}
    z_axis = []
    index = 0
    tmp = ""
    flag_hck = True
    is_first_time = True
    is_first_time_x_axis = True
    case = os.path.splitext(filename)[0]
    with open(PATH + filename, 'rt') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            # only once for one mem location
            print("\tIteration for mem location: {}".format(row[0]))
            if flag_hck:
                tmp = int(row[0])
                flag_hck = False
            if is_first_time_x_axis and (tmp == int(row[0])):
                x_axis.append(int(row[1]))
            if (tmp == int(row[0])):
                y_axis.append(int(row[2]))
            else:
                dic_y[index] = y_axis
                y_axis = []
                is_first_time_x_axis = False
                index = index + 1
                y_axis.append(int(row[2]))

            tmp = int(row[0])
        dic_y[index] = y_axis
    find_min_max_range(dic_y)

    # giving a title to the graph
    plt.title(case.upper())
    blue_patch = mpatches.Patch(color='blue', label='Mem Loc 1')
    black_patch = mpatches.Patch(color='black', label='Mem Loc 2')
    yellow_patch = mpatches.Patch(color='yellow', label='Mem Loc 3')
    purple_patch = mpatches.Patch(color='purple', label='Mem Loc 4')
    cyan_patch = mpatches.Patch(color='cyan', label='Mem Loc 5')
    magenta_patch = mpatches.Patch(color='magenta', label='Mem Loc 6')
    grey_patch = mpatches.Patch(color='grey', label='Mem Loc 7')
    pink_patch = mpatches.Patch(color='pink', label='Mem Loc 8')
    maroon_patch = mpatches.Patch(color='maroon', label='Mem Loc 9')
    red_patch = mpatches.Patch(color='red', label='Mem Loc 10')
    orange_patch = mpatches.Patch(color='orange', label='Mem Loc 11')

    fig = plt.figure()
    plt.xlabel('Iterations')
    # naming the y axis
    plt.ylabel('Access Time')
    plt.title(case)

    plt.legend(
        handles=[blue_patch,black_patch,yellow_patch,purple_patch,cyan_patch,magenta_patch,grey_patch,pink_patch,maroon_patch,red_patch,orange_patch])

    min_y_axis, max_y_axis, range_y = find_min_max_range(dic_y)
    colors = ["blue", "black", "yellow", "violet", "cyan", "magenta", "grey", "pink", "maroon" ,"red","orange"]
    for key, y_axis in dic_y.items():
        plt.plot(x_axis, y_axis, color=colors[key])

    plt.xticks(np.arange(min(x_axis), max(x_axis) + 1, (max(x_axis)-min(x_axis))/10))
    plt.yticks(np.arange(min_y_axis, max_y_axis + 1, range_y))
    # plt.show()
    fig.savefig(case + '.png', dpi=1200)


if __name__ == '__main__':
    PATH = "path_to_csv_files"
    plot_graph('result_with_flush.csv')
    plot_graph('result_without_flush.csv')
    plot_graph('result_with_pv_on_diff.csv')
    plot_graph('result_with_pv_on_same.csv')
    print("\tAll graphs saved successfully!")
