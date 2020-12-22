import sys
from loguru import logger as log
from typing import List, Set, Dict, Generator, Optional
from utils import SchedulingRequirement, SchedulingItem, TimeTable
from .simulated_annealing import SimulatedAnnealingAlgorithm, LoggingItem
from .class_rescheduling import SchedulingState

class Handler:
    def __init__(self,
        timeTable: TimeTable,
        classesToReschedule: List[int],
        rescheduledSessionStart: int,
        epochs: int,
        adjacencyStates: int,
    ):
        self.__timeTable: TimeTable = timeTable
        self.__classesToReschedule: Set[int] = set(classesToReschedule)
        self.__rescheduledSessionStart = rescheduledSessionStart
        self.__requirement, self.__remainingSchedules = self.__preprocess()
        log.info("there are {} schedules remaining and {} requirement items, rescheduling requirements:\n{}".format(
            len(self.__remainingSchedules), len(self.__requirement),
            "\n".join(list(map(str, self.__requirement)))
        ))
        self.__epochs = epochs
        self.__adjacencyStates = adjacencyStates
        self.__alg: SimulatedAnnealingAlgorithm = SimulatedAnnealingAlgorithm(
            self.__getFirstState,
            self.__lossFunction,
            self.__getNextStates,
            self.__logFunction,
            self.__earlyStopFunction,
            initTemp = 10,
            finalTemp = 0.01,
        )
        self.__bestState: Optional[SchedulingState] = None

    def __getFirstState(self) -> SchedulingState:
        return SchedulingState(
            self.__remainingSchedules,
            self.__requirement,
            self.__timeTable.courseTeachersMap,
            {
                "classes": 1.0,
                "teachers": 1.0,
            },
            900,
        )

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
