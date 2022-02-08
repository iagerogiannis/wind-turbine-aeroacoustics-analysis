from itertools import chain


def bubble_sort(array, arrays):
    n = len(array)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
                for array_i in arrays:
                    array_i[j], array_i[j + 1] = array_i[j + 1], array_i[j]


def bubble_sort_dicts(array, property):
    n = len(array)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if array[j][property] > array[j + 1][property]:
                array[j], array[j + 1] = array[j + 1], array[j]


def flatten_2d_list(array):
    return list(chain.from_iterable(array))
