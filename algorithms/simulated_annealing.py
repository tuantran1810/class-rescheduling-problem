import sys
from typing import Callable, List
from math import exp
from random import random, choice

class State:
    def __init__(self) -> None:
        raise NotImplemented

    def getScore(self) -> float:
        raise NotImplemented

    def __gt__(self, other) -> bool:
        raise NotImplemented

class SimulatedAnnealingAlgorithm:
    def __init__(self, 
        firstStateFn: Callable[[], State], 
        lossFn: Callable[[State, State], float], 
        nextStatesFn: Callable[[State], State], 
        logFn: Callable[[State], None], 
        initTemp: float = 100.0, 
        coolingRate: float = 0.1,
    ) -> None:
        self.__state: Callable[[], State] = firstStateFn()
        self.__getNextStates: Callable[[State], State] = nextStatesFn
        self.__getLoss: Callable[[State, State], float] = lossFn
        self.__logFn: Callable[[State, float], None] = logFn
        self.__temp: float = initTemp
        self.__coolingRate: float = coolingRate
        
    def __call__(self, epochs):
        for i in range(epochs):
            worseNeighbors: List[State] = list()
            recentState = self.__state
            for nxtState in self.__getNextStates(recentState):
                if nxtState > recentState:
                    recentState = nxtState
                else:
                    loss: float = self.__getLoss(recentState, nxtState)
                    prob: float = exp(-(loss/(self.__temp + sys.float_info.epsilon)))
                    if prob >= random():
                        worseNeighbors.append(nxtState)
                        recentState = nxtState

            if len(worseNeighbors) and (self.__state.getScore() > recentState.getScore()):
                self.__state = choice(worseNeighbors)
            self.__logFn(self.__state)
            self.__temp *= self.__coolingRate
