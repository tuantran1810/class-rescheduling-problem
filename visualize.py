import utils
import pickle
import matplotlib.pyplot as plt
import sys

def loadData():
    with open(sys.argv[1], 'rb') as f:
        return pickle.load(f)

def plotTemp(data):
    x = []
    y = []
    for v in data:
        x.append(v[0])
        y.append(v[3])
    plt.plot(x, y)
    plt.ylabel('Temp')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def plotAvgLoss(data):
    x = []
    y = []
    for v in data:
        x.append(v[0])
        y.append(v[2])
    plt.plot(x, y)
    plt.ylabel('avgLoss')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def plotScore(data):
    x = []
    y = []
    for v in data:
        x.append(v[0])
        y.append(v[1])
    plt.plot(x, y)
    plt.ylabel('score')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def plotColumnChart(path):
    classids = {}
    tmp = {}
    with open(path, 'rb') as f:
        data = pickle.load(f)

        for v in data.state.getComputedSchedule():
            if v.classID not in classids:
                classids[v.classID] = 0
                tmp[v.classID] = 0
        for v in data.state.getComputedSchedule():
            classids[v.classID] = max(classids[v.classID], v.sessionID)

    with open('data/timetable.pkl', 'rb') as f:
        data = pickle.load(f)
        for v in data.allSchedules():
            if v.classID in classids.keys():
                tmp[v.classID] = max(tmp[v.classID], v.sessionID)
    x_ = list(classids.keys())
    x = [i for i in range(len(classids))]
    y = [v - tmp[k] for k, v in classids.items()]
    y_ = []
    for k, v in classids.items():
        v_ = int(v/2) if v%2 == 0 else int((v-1)/2)
        v__ = int(tmp[k]/2) if tmp[k]%2 == 0 else int((tmp[k]-1)/2)
        y_.append(v_ - v__)
    plt.bar(x, y, align='center', alpha=0.25)
    plt.yticks(y, y_)
    plt.xticks(x, x_)
    plt.ylabel('number of days')
    plt.xlabel('classid')
    plt.show()

def main():
    data = loadData()
    plotTemp(data)
    plotAvgLoss(data)
    plotScore(data)
    plotColumnChart(sys.argv[2])

if __name__ == "__main__":
    main()