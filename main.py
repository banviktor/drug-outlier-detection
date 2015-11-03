import math

def dist(a_dict, b_dict):
    a = dict(a_dict)
    b = dict(b_dict)
    squaresum = 0.0
    for i in range(0, max( max(a.keys()), max(b.keys()) )):
        ai = a.get(i, 0.0)
        bi = b.get(i, 0.0)
        squaresum += pow(ai-bi, 2.0)
    return math.sqrt(squaresum)


def read_data():
    data_list = []
    with open("data/freq.ker", "r") as f:
        lines = f.readlines()
        for line in lines:
            line_split = line[line.find(" "):].split(" ")
            data_dict = {}
            for data in line_split[1:]:
                data_split = data.split(":")
                data_dict[ int(data_split[0]) ] = float(data_split[1])
            data_list.append( (line[:line.find(" ")], data_dict) )
    print(data_list[0])
    return data_list


def main():
    data_list = read_data()
    distance = dist(data_list[0][1], data_list[1][1])
    print(distance)

if __name__ == "__main__":
    # execute only if run as a script
    main()
