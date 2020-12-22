import utils
import pickle
import matplotlib.pyplot as plt

def loadData():
    with open('data/logging.pkl', 'rb') as f:
        return pickle.load(f)

def plotTemp(data):
    x = []
    y = []
    for v in data:
        x.append(v.epoch)
        y.append(v.temp)
    plt.plot(x, y)
    plt.ylabel('Temp')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def plotAvgLoss(data):
    x = []
    y = []
    for v in data:
        x.append(v.epoch)
        y.append(v.avgLoss)
    plt.plot(x, y)
    plt.ylabel('avgLoss')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def plotScore(data):
    x = []
    y = []
    for v in data:
        x.append(v.epoch)
        y.append(v.state.getScore())
    plt.plot(x, y)
    plt.ylabel('score')
    plt.xlabel('Epoch')
    # plt.title('')
    plt.show()

def main():
    data = loadData()
    plotTemp(data)
    plotAvgLoss(data)
    plotScore(data)

if __name__ == "__main__":
    main()