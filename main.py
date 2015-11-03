def readData():
    dataList = []
    with open("data/freq.ker", "r") as f:
        lines = f.readlines()
        print(lines[0])
        for line in lines:
            splitLine = line.split(" ")
            valueList = []
            for value in splitLine[1:]:
                splitValue = value.split(":")
                while (len(valueList) < int(splitValue[0]) ):
                    valueList.append(0.0)
                valueList.append(float(splitValue[1]))
            dataList.append( (splitLine[0], valueList) )
        print(dataList[0])

def main():
    readData()

if __name__ == "__main__":
    # execute only if run as a script
    main()
