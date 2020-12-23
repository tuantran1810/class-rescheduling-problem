import sys
import pickle
from loguru import logger as log
from typing import List, Set, Dict, Generator, Optional
from utils import SchedulingRequirement, SchedulingItem, TimeTable
from .simulated_annealing import SimulatedAnnealingAlgorithm, LoggingItem
from .class_rescheduling import SchedulingState, OptimalWeight

class Handler:
    def __init__(self,
        timeTable: TimeTable,
        classesToReschedule: List[int],
        rescheduledSessionStart: int,
        rescheduledSessionEnd: int,
        epochs: int,
        adjacencyStates: int,
        weight: OptimalWeight,
        initTemp: float = 10.0,
        finalTemp: float = 0.01,
        backupPicklePath: str = "data/",
        firstState: Optional[SchedulingState] = None,
    ):
        self.__timeTable: TimeTable = timeTable
        self.__classesToReschedule: Set[int] = set(classesToReschedule)
        self.__rescheduledSessionStart = rescheduledSessionStart
        self.__rescheduledSessionEnd = rescheduledSessionEnd

        self.__requirement, self.__remainingSchedules = self.__preprocess()
        log.info("there are {} schedules remaining and {} requirement items, rescheduling requirements:\n{}".format(
            len(self.__remainingSchedules), len(self.__requirement),
            "\n".join(list(map(str, self.__requirement)))
        ))

        self.__epochs = epochs
        self.__adjacencyStates = adjacencyStates
        self.__bestState: Optional[SchedulingState] = firstState
        self.__weight = weight
        self.__alg: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            self.__getFirstState,
            self.__lossFunction,
            self.__getNextStates,
            self.__logFunction,
            self.__earlyStopFunction,
            initTemp = initTemp,
            finalTemp = finalTemp,
        )  
        self.__statLogging: List[LoggingItem] = []
        self.__backupPath: str = backupPicklePath

    def __getFirstState(self) -> SchedulingState:
        if self.__bestState is None:
            return SchedulingState(
                self.__remainingSchedules,
                self.__requirement,
                self.__timeTable.courseTeachersMap,
                self.__weight,
                self.__rescheduledSessionEnd,
            )
        
        self.__bestState.clearScore()
        self.__bestState.setWeight(self.__weight)
        return self.__bestState

    def __lossFunction(self, state1: SchedulingState, state2: SchedulingState) -> float:
        score1: int = state1.getScore()
        score2: int = state2.getScore()
        return abs(score1 - score2)*1.0

    def __getNextStates(self, state: SchedulingState) -> Generator[SchedulingState, None, None]:
        for _ in range(self.__adjacencyStates):
            nxtState = state.duplicate()
            nxtState.permuteSchedule(2, 2)
            yield nxtState

    def __logFunction(self, logging: LoggingItem) -> None:
        if self.__bestState is None:
            self.__bestState = logging.state
        if logging.state > self.__bestState:
            self.__bestState = logging.state
        log.info(logging)
        if logging.epoch % 1000 == 0 or logging.epoch == self.__epochs-1:
            with open(self.__backupPath + 'state-backup-{}.pkl'.format(logging.epoch), 'wb') as handle:
                pickle.dump(logging, handle, protocol=pickle.HIGHEST_PROTOCOL)
        self.__statLogging.append([logging.epoch, logging.state.getScore(), logging.avgLoss, logging.temp])

    def __earlyStopFunction(self, state: SchedulingState) -> bool:
        return abs(state.getScore()) < sys.float_info.epsilon

    def __preprocess(self):
        requirements: Dict[str, SchedulingRequirement] = {}
        remainingSchedules: List[SchedulingItem] = []
        for item in self.__timeTable.allSchedules():
            if item.classID in self.__classesToReschedule:
                key: str = item.produceClassCourseKey()
                if key not in requirements:
                    requirements[key] = SchedulingRequirement(item.classID, item.courseID, self.__rescheduledSessionStart, 1)
                else:
                    requirements[key].nsessions += 1
            else:
                remainingSchedules.append(item)
        requirementList: List[SchedulingRequirement] = list()
        for _, req in requirements.items():
            requirementList.append(req)
        return requirementList, remainingSchedules

    def start(self) -> SchedulingState:
        self.__alg(self.__epochs)
        return self.__bestState

    def dumpStatLogging(self):
        with open(self.__backupPath + "logging.pkl", 'wb') as handle:
            pickle.dump(self.__statLogging, handle, protocol=pickle.HIGHEST_PROTOCOL)
