import numpy as np
import functools as ft


class CalculateLof:

    distances = None
    lofs = []
    k = 0

    class Distances:
        data_list = []
        dist_list = []

        def __init__(self, data_list):
            self.data_list = data_list
            self.dist_list = []
            for i in range(0, len(data_list)):
                self.dist_list.insert(i, [0.0]*len(data_list))
            self.calc_distances()

        def calc_distances(self):
            for i, a_data in enumerate(self.data_list):
                for j, b_data in enumerate(self.data_list):
                    if i == j:
                        break
                    a = a_data[1]
                    b = b_data[1]

                    diff = np.linalg.norm(a-b)
                    self.dist_list[i][j] = diff
                    self.dist_list[j][i] = diff

        def dist(self, a_index, b_index):
            return self.dist_list[a_index][b_index]

    @ft.lru_cache(maxsize=None)
    def n_k(self, a_index):
        k = self.k
        dist = self.distances.dist_list[a_index][:]
        out = []
        for m in (sorted((e, i) for i, e in enumerate(dist))):
            if len(out) < k or (len(out) > 0 and m[0] == dist[out[len(out)-1]]):
                if m[1] != a_index:
                    out.append(m[1])
            else:
                break
        return out

    @ft.lru_cache(maxsize=None)
    def k_distance(self, a_index):
        return self.distances.dist(a_index, self.n_k(a_index)[-1])

    def reachability_distance(self, a_index, b_index):
        return max(self.k_distance(b_index), self.distances.dist(a_index, b_index))

    @ft.lru_cache(maxsize=None)
    def lrd(self, a_index):
        nk = self.n_k(a_index)
        rd_sum = 0.0
        for b_index in nk:
            rd_sum += self.reachability_distance(a_index, b_index)
        if rd_sum == 0:
            return float("inf")
        return len(nk) / rd_sum

    def lof(self, a_index):
        nk = self.n_k(a_index)
        lof_sum = 0.0
        for b_index in nk:
            lof_sum += self.lrd(b_index)
        return lof_sum / len(nk) / self.lrd(a_index)

    def calc_lof(self):
        for i, e in enumerate(self.distances.data_list):
            self.lofs.append(self.lof(i))

    @staticmethod
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

    def __init__(self, filename, k):
        self.k = k
        import time
        start = time.time()

        data_list = CalculateLof.read_data(filename)
        print(data_list[0])
        self.distances = CalculateLof.Distances(data_list)
        print(self.distances.dist_list[35])
        end = time.time()
        print("Tavolsagmatrix felepitese: " + str(end - start))

        '''
        start = time.time()
        print(self.lrd(0))
        end = time.time()
        print("lrd kiszamitasa: " + str(end - start))
        '''

        '''
        start = time.time()
        print(self.lof(0))
        end = time.time()
        print("LOF kiszamitasa: " + str(end - start))
        '''

        start = time.time()
        self.calc_lof()
        print(self.lofs[0])
        end = time.time()
        print("Osszes LOF kiszamitasa: " + str(end - start))

        print(self.lofs[:10])
        print(self.lrd.cache_info())


def main():
    import time
    start = time.time()
    calculateLof = CalculateLof("freq.ker", 3)
    calculateLof = CalculateLof("maccs.ker", 3)
    calculateLof = CalculateLof("molconnz.ker", 3)
    calculateLof = CalculateLof("target.ker", 3)
    end = time.time()
    print("Minden: " + str(end - start))

if __name__ == "__main__":
    # execute only if run as a script
    main()
