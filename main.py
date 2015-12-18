import numpy as np
import functools as ft
import operator as op
import time
import matplotlib.pyplot as plt


class SingleSet:
    def __init__(self, filename, k):
        self.k = k
        # Read data from file.
        self.data = SingleSet.read_data(filename)
        # Initialize distances matrix.
        self.distances = []
        for i in range(len(self.data)):
            self.distances.insert(i, [0.0]*len(self.data))

        # Fill the distance matrix.
        self.__calc_distances()

    @staticmethod
    def read_data(source):
        data_list = []
        with open("data/" + source, "r") as f:
            lines = f.readlines()

            # Determine the dimension of values.
            cols = 0
            for l in lines:
                split_line = l.split(" ")
                for value in split_line[1:]:
                    split_value = value.split(":")
                    # The biggest index in the file will be the dimension.
                    cols = max(cols, int(split_value[0])+1)

            # Fill the data_list list with the file's contents.
            for i, line in enumerate(lines):
                split_line = line.split(" ")
                # Start with 0 vector.
                value_list = np.zeros(cols)
                for value in split_line[1:]:
                    # Set each defined value.
                    split_value = value.split(":")
                    value_list[int(split_value[0])] = float(split_value[1])
                # Append the drug's name and its vector.
                data_list.append((split_line[0], value_list))
        return data_list

    def __calc_distances(self):
        for i, a_data in enumerate(self.data):
            for j, b_data in enumerate(self.data):
                if i == j:
                    # There is already a 0.0 in this position.
                    break

                a = a_data[1]
                b = b_data[1]
                # Calculate the distance between a and b.
                diff = np.linalg.norm(a-b)

                # Fill the matrix symmetrically for faster access in the future.
                self.distances[i][j] = diff
                self.distances[j][i] = diff

    @ft.lru_cache(maxsize=None)
    def __n_k(self, a_index):
        # Fetch a's row from the distance matrix.
        dist = self.distances[a_index][:]
        out = []
        for m in (sorted((e, i) for i, e in enumerate(dist))):
            # Fill while there are less than k points, or the next point is as far as the previous one.
            if len(out) < self.k or (len(out) > 0 and m[0] == dist[out[-1]]):
                if m[1] != a_index:
                    out.append(m[1])
            else:
                break
        return out

    @ft.lru_cache(maxsize=None)
    def __k_distance(self, a_index):
        # The furthest point of the k closest neighbors is the k-distance.
        return self.distances[a_index][self.__n_k(a_index)[-1]]

    @ft.lru_cache(maxsize=None)
    def __lrd(self, a_index):
        nk = self.__n_k(a_index)
        rd_sum = 0.0
        for b_index in nk:
            # Sum of reachability distances.
            rd_sum += max(self.__k_distance(b_index), self.distances[a_index][b_index])
        if rd_sum == 0:
            # With duplicate points the lrd can become infinite.
            return float("inf")
        return len(nk) / rd_sum

    def lof(self, a_index):
        nk = self.__n_k(a_index)
        lof_sum = 0.0
        for b_index in nk:
            lof_sum += self.__lrd(b_index)

        lrd_a = self.__lrd(a_index)
        # Handle infinite values manually.
        if lof_sum == float("inf") and lrd_a == float("inf"):
            return 1.0
        elif lrd_a == float("inf"):
            return 0.0
        elif lof_sum == float("inf"):
            return float("inf")
        # If there are no infinite values use the regular formula.
        return lof_sum / len(nk) / lrd_a


class FusedSet:
    def __init__(self):
        # Initialize an empty dictionary.
        self.data = dict()

    def add_set(self, single_set):
        for i in range(len(single_set.data)):
            # Determine the drug's name.
            subject = single_set.data[i][0]

            # If there is no entry for the subject yet, initialize with an empty list.
            if subject not in self.data:
                self.data[subject] = []

            # Append the drug's LOF.
            self.data[subject].append(single_set.lof(i))

    def all_lof(self):
        out = dict()
        # Calculate the average of LOFs of each drug.
        for subject, lof_list in self.data.items():
            out[subject] = np.average(lof_list)
        # Sort: biggest LOF first.
        return sorted(out.items(), key=op.itemgetter(1), reverse=True)

    def plot(self):
        # Draw a plot using the fused LOF values.
        lofs = [v[1] for v in self.all_lof()]
        plt.hist(lofs, bins=10, range=(0, 5))
        plt.title("Local Outlier Factor Histogram")
        plt.xlabel("Local Outlier Factor")
        plt.ylabel("Number of values")
        plt.show()


def main():
    start = time.time()
    print("Local Outlier Factor calculator")
    print("Created by:")
    print("  Aron Karolyi")
    print("  Viktor Ban")
    print("")
    print("LOF calculation started...")
    fused = FusedSet()
    fused.add_set(SingleSet("freq.ker", 25))
    fused.add_set(SingleSet("maccs.ker", 25))
    fused.add_set(SingleSet("molconnz.ker", 25))
    fused.add_set(SingleSet("target.ker", 25))
    with open('results.csv', 'w') as output:
        for drug, lof in fused.all_lof():
            output.write("{},{}\n".format(drug, lof))
    print("LOF calculation completed. Check the results in results.csv.")
    end = time.time()
    print("Calculation took {} seconds".format(np.round(end - start, 3)))
    fused.plot()

if __name__ == "__main__":
    main()
