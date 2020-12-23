import utils
import pickle
import matplotlib.pyplot as plt
import sys

def loadData():
    with open('output/logging.pkl', 'rb') as f:
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
    with open(path, 'rb') as f:
        data = pickle.load(f)
        classids = {}
        for v in data.state.getComputedSchedule():
            if v.classID not in classids:
                classids[v.classID] = 0
        for v in data.state.getComputedSchedule():
            classids[v.classID] = max(classids[v.classID], v.sessionID)
        x = list(classids.keys())
        y = [i - min(classids.values()) + 2 for i in classids.values()]
        y_ = [utils.session2Date(i).split(' ')[0] for i in classids.values()]

        plt.bar(x, y, align='center', alpha=0.25)
        plt.yticks(y, y_)
        plt.xticks(x, x)
        plt.ylabel('date')
        plt.xlabel('classid')
        plt.show()


def main():
    data = loadData()
    plotTemp(data)
    plotAvgLoss(data)
    plotScore(data)
    plotColumnChart(sys.argv[1])

if __name__ == "__main__":
    main()