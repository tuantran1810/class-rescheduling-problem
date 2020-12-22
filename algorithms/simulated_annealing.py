import sys
from typing import Callable, List
from math import exp, log
from random import random, choice
from dataclasses import dataclass

class State:
    def __init__(self) -> None:
        raise NotImplemented

    def getScore(self) -> float:
        raise NotImplemented

    def __gt__(self, other) -> bool:
        raise NotImplemented

@dataclass
class LoggingItem:
    epoch: int = -1
    state: State = None
    avgLoss: float = -1.0
    temp: float = -1.0

    def __str__(self) -> str:
        return "[Epoch {}] -- score: {}, average loss: {:.3f}, temperature: {:.3f}".format(
            self.epoch, self.state.getScore(), self.avgLoss, self.temp,
        )

class SimulatedAnnealingAlgorithm:
    def __init__(self,
        firstStateFn: Callable[[], State],
        lossFn: Callable[[State, State], float],
        nextStatesFn: Callable[[State], State],
        logFn: Callable[[LoggingItem], None],
        earlyStopFn: Callable[[State], bool],
        initTemp: float = 100.0,
        finalTemp: float = 1.0,
    ) -> None:
        self.__state: Callable[[], State] = firstStateFn()
        self.__getNextStates: Callable[[State], State] = nextStatesFn
        self.__getLoss: Callable[[State, State], float] = lossFn
        self.__logFn: Callable[[LoggingItem], None] = logFn
        self.__earlyStopFn: Callable[[State], bool] = earlyStopFn
        self.__temp: float = initTemp
        self.__finalTemp: float = finalTemp

    def __updateTemp(self, epochs: int):
        alpha: float = 1 - (log(self.__temp) - log(self.__finalTemp))/epochs
        self.__temp *= alpha

    def __call__(self, epochs):
        for i in range(epochs):
            totalLoss: float = 0.0
            cnt: int = 0
            recentState = self.__state
            for nxtState in self.__getNextStates(recentState):
                if nxtState > recentState:
                    recentState = nxtState
                else:
                    loss: float = self.__getLoss(recentState, nxtState)
                    prob: float = exp(-(loss/(self.__temp + sys.float_info.epsilon)))
                    # print(f"loss = {loss}, prob = {prob}, temp = {self.__temp}")
                    if prob >= random():
                        recentState = nxtState
                    totalLoss += loss
                    cnt += 1

            self.__state = recentState

            avgLoss: float = -1.0
            if cnt > 0:
                avgLoss = totalLoss/cnt
            logging: LoggingItem = LoggingItem(
                epoch = i,
                state = recentState,
                avgLoss = avgLoss,
                temp = self.__temp,
            )
            self.__logFn(logging)

            if self.__earlyStopFn(recentState):
                return
            self.__updateTemp(epochs)
