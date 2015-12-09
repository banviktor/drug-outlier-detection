import math
import numpy as np
import numexpr as ne
import functools as ft

distances = None
kdistances = None


class Distances:
    data_list = []
    dist_list = []

    def __init__(self, data_list):
        self.data_list = data_list
        self.dist_list = [[0]*len(data_list)]*len(data_list)
        self.calc_distances()

    def calc_distances(self):
        for i, a_data in enumerate(self.data_list):
            for j, b_data in enumerate(self.data_list):
                if a_data == b_data:
                    break
                a = a_data[1]
                b = b_data[1]

                '''
                Faster solution
                http://stackoverflow.com/questions/1401712/how-can-the-euclidean-distance-be-calculated-with-numpy
                '''
                diff = np.linalg.norm(a-b)
                self.dist_list[i][j] = diff

    def dist(self, a_index, b_index):
        a_index, b_index = sorted((a_index, b_index))
        return self.dist_list[a_index][b_index]


def n_k(data_list, k, a_index): # a
    dist = (distances.dist(a_index, i) for i in range(len(data_list)))
    a = [m[1] for m in (sorted((e, i) for i, e in enumerate(dist)))]
    # can be > k
    return a[1:k + 1]


class KDistances:
    kd_dict = {}

    def k_distance(self, data_list, k, a_index): # b = a
        if k not in self.kd_dict:
            self.kd_dict[k] = []
            for i, e in enumerate(data_list):
                self.kd_dict[k].append(distances.dist(i, n_k(data_list, k, i)[-1]))
        return self.kd_dict[k][a_index]


def reachability_distance(data_list, k, a_index, b_index): # c = n*b = n*a
    return max(kdistances.k_distance(data_list, k, b_index), distances.dist(a_index, b_index))


def lrd(data_list, k, a_index): # d = n*c = n*n*b = n*n*a
    rd_sum = 0.0
    for i in range(0, len(data_list)):
        if i != a_index:
            rd_sum += reachability_distance(data_list, k, a_index, i)
    return len(n_k(data_list, k, a_index)) / rd_sum


def lof(data_list, k, a_index): # e = n*d = n*n*n*b
    lof_sum = 0.0
    for b_index in range(len(data_list)):
        if a_index != b_index:
            lof_sum += lrd(data_list, k, b_index)
    return lof_sum / len(n_k(data_list, k, a_index)) / lrd(data_list, k, a_index)


def read_data(source):
    data_list = []
    with open("data/" + source, "r") as f:
        lines = f.readlines()

        # count matrix columns
        cols = 0
        for l in lines:
            split_line = l.split(" ")
            for value in split_line[1:]:
                split_value = value.split(":")
                cols = max(cols, int(split_value[0])+1)

        # read values to a matrix
        for i, line in enumerate(lines):
            split_line = line.split(" ")
            value_list = np.zeros(cols)
            for value in split_line[1:]:
                split_value = value.split(":")
                value_list[int(split_value[0])] = float(split_value[1])
            data_list.append((split_line[0], value_list))
    return data_list


def main():
    import time
    start = time.time()

    data_list = read_data("freq.ker")
    print(data_list[0])
    global distances
    distances = Distances(data_list)
    global kdistances
    kdistances = KDistances()
    print(distances.dist_list[0])
    end = time.time()
    print("Tavolsagmatrix felepitese: " + str(end - start))

    start = time.time()
    print(lrd(data_list, 3, 0))
    end = time.time()
    print("lrd kiszamitasa: " + str(end - start))

    start = time.time()
    print(lof(data_list, 3, 0))
    end = time.time()
    print("LOF kiszamitasa: " + str(end - start))

if __name__ == "__main__":
    # execute only if run as a script
    main()
