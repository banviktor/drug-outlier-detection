import math


def dist(data_list, a_index, b_index):
    a = dict(data_list[a_index][1])
    b = dict(data_list[b_index][1])
    square_sum = 0.0
    for i in range(0, max( max(a.keys()), max(b.keys()) )):
        ai = a.get(i, 0.0)
        bi = b.get(i, 0.0)
        square_sum += pow(ai-bi, 2.0)
    return math.sqrt(square_sum)


def n_k(data_list, k, a_index):
    distances = ( dist(data_list, a_index, i) for i in range(len(data_list)) )
    a = [ m[1] for m in (sorted((e,i) for i,e in enumerate(distances))) ]
    return a[1:k+1]


def k_distance(data_list, k, a_index):
    return dist(data_list, a_index, n_k(data_list, k, a_index)[-1])


def reachability_distance(data_list, k, a_index, b_index):
    return max(k_distance(data_list, k, b_index), dist(data_list, a_index, b_index))


def read_data():
    data_list = []
    with open("data/freq.ker", "r") as f:
        lines = f.readlines()
        for line in lines:
            line_split = line[line.find(" "):].split(" ")
            data_dict = {}
            for data in line_split[1:]:
                data_split = data.split(":")
                data_dict[int(data_split[0])] = float(data_split[1])
            data_list.append((line[:line.find(" ")], data_dict))
    print(data_list[0])
    return data_list


def main():
    data_list = read_data()
    print(reachability_distance(data_list, 3, 0, 2))

if __name__ == "__main__":
    # execute only if run as a script
    main()
