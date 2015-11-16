import math

d = []


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
                    continue
                if len(a_data[1]) < len(b_data[1]):
                    a, b = list(a_data[1]), list(b_data[1])
                else:
                    b, a = list(a_data[1]), list(b_data[1])
                square_sum = 0.0
                for k in range(len(a)):
                    ak = a[k]
                    bk = b[k]
                    square_sum += pow(ak - bk, 2.0)
                for k in range(len(a), len(b)):
                    bk = b[k]
                    square_sum += pow(bk, 2.0)
                self.dist_list[i][j] = math.sqrt(square_sum)

    def dist(self, a_index, b_index):
        return self.dist_list[a_index][b_index]


def n_k(data_list, k, a_index):
    distances = (d.dist(a_index, i) for i in range(len(data_list)))
    a = [m[1] for m in (sorted((e, i) for i, e in enumerate(distances)))]
    # can be > k
    return a[1:k + 1]


def k_distance(data_list, k, a_index):
    return d.dist(a_index, n_k(data_list, k, a_index)[-1])


def reachability_distance(data_list, k, a_index, b_index):
    return max(k_distance(data_list, k, b_index), d.dist(a_index, b_index))


def lrd(data_list, k, a_index):
    rd_sum = 0.0
    for i in range(0, len(data_list)):
        if i != a_index:
            rd_sum += reachability_distance(data_list, k, a_index, i)
    return len(n_k(data_list, k, a_index)) / rd_sum


def read_data(source):
    data_list = []
    with open("data/" + source, "r") as f:
        lines = f.readlines()

        # count matrix columns
        cols = 0
        for l in lines:
            cols = max(cols, l.count(":"))

        # read values to a matrix
        print(data_list)
        for i, line in enumerate(lines):
            split_line = line.split(" ")
            value_list = []*cols
            for value in split_line[1:]:
                split_value = value.split(":")
                while len(value_list) < int(split_value[0]):
                    value_list.append(0.0)
                value_list.append(float(split_value[1]))
            data_list.append((split_line[0], value_list))
    return data_list


def main():
    data_list = read_data("freq.ker")
    print(data_list[0])
    global d
    d = Distances(data_list)
    # slow
    #print(lrd(data_list, 3, 0))


if __name__ == "__main__":
    # execute only if run as a script
    main()
