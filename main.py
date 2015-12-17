import numpy as np
import functools as ft
import operator as op
import time
import matplotlib.pyplot as plt


class SingleSet:
    def __init__(self, filename, k):
        self.k = k
        self.data = SingleSet.read_data(filename)
        self.distances = []
        for i in range(0, len(self.data)):
            self.distances.insert(i, [0.0]*len(self.data))
        self.__calc_distances()

    @staticmethod
    def read_data(source):
        data_list = []
        with open("data/" + source, "r") as f:
            lines = f.readlines()

            cols = 0
            for l in lines:
                split_line = l.split(" ")
                for value in split_line[1:]:
                    split_value = value.split(":")
                    cols = max(cols, int(split_value[0])+1)

            for i, line in enumerate(lines):
                split_line = line.split(" ")
                value_list = np.zeros(cols)
                for value in split_line[1:]:
                    split_value = value.split(":")
                    value_list[int(split_value[0])] = float(split_value[1])
                data_list.append((split_line[0], value_list))
        return data_list

    def __calc_distances(self):
        for i, a_data in enumerate(self.data):
            for j, b_data in enumerate(self.data):
                if i == j:
                    break
                a = a_data[1]
                b = b_data[1]

                diff = np.linalg.norm(a-b)
                self.distances[i][j] = diff
                self.distances[j][i] = diff

    @ft.lru_cache(maxsize=None)
    def __n_k(self, a_index):
        k = self.k
        dist = self.distances[a_index][:]
        out = []
        for m in (sorted((e, i) for i, e in enumerate(dist))):
            if len(out) < k or (len(out) > 0 and m[0] == dist[out[-1]]):
                if m[1] != a_index:
                    out.append(m[1])
            else:
                break
        return out

    @ft.lru_cache(maxsize=None)
    def __k_distance(self, a_index):
        return self.distances[a_index][self.__n_k(a_index)[-1]]

    @ft.lru_cache(maxsize=None)
    def __lrd(self, a_index):
        nk = self.__n_k(a_index)
        rd_sum = 0.0
        for b_index in nk:
            rd_sum += max(self.__k_distance(b_index), self.distances[a_index][b_index])
        if rd_sum == 0:
            return float("inf")
        return len(nk) / rd_sum

    def lof(self, a_index):
        nk = self.__n_k(a_index)
        lof_sum = 0.0
        for b_index in nk:
            lof_sum += self.__lrd(b_index)

        lrd_a = self.__lrd(a_index)
        if lof_sum == float("inf") and lrd_a == float("inf"):
            return 1.0
        elif lrd_a == float("inf"):
            return 0.0
        elif lof_sum == float("inf"):
            return float("inf")
        return lof_sum / len(nk) / lrd_a


class FusedSet:
    def __init__(self):
        self.data = dict()

    def add_set(self, single_set):
        for i in range(0, len(single_set.data)):
            subject = single_set.data[i][0]
            if not self.data.__contains__(subject):
                self.data[subject] = []
            self.data[subject].append(single_set.lof(i))

    def all_lof(self):
        out = dict()
        for subject, lof_list in self.data.items():
            out[subject] = np.average(lof_list)
        return sorted(out.items(), key=op.itemgetter(1), reverse=True)

    def plot(self):
        lofs = [v[1] for v in self.all_lof()]
        plt.hist(lofs, bins=10, range=(0, 5))
        plt.title("Local Outlier Factor Histogram")
        plt.xlabel("Local Outlier Factor")
        plt.ylabel("Number of values")
        plt.show()


def main():
    start = time.time()
    print("LOF calculation started...")
    fused = FusedSet()
    fused.add_set(SingleSet("freq.ker", 25))
    fused.add_set(SingleSet("maccs.ker", 25))
    fused.add_set(SingleSet("molconnz.ker", 25))
    fused.add_set(SingleSet("target.ker", 25))
    output = open("results.csv", "w")
    for drug, lof in fused.all_lof():
        output.write("{},{}\n".format(drug, lof))
    output.close()
    print("LOF calculation completed. Check the results in results.csv.")
    end = time.time()
    print("Calculation took {} seconds".format(np.round(end - start, 3)))
    fused.plot()

if __name__ == "__main__":
    main()

