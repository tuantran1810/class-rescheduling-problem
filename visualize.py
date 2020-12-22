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

def main():
    data = loadData()
    plotTemp(data)
    plotAvgLoss(data)
    plotScore(data)

if __name__ == "__main__":
    main()