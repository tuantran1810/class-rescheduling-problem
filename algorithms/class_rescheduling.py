from dataclasses import dataclass
from algorithms.simulated_annealing import State
from typing import List, Dict, Set, Optional, Any
from random import choice, randint
from utils import SchedulingItem, SchedulingRequirement
from copy import deepcopy

class SchedulingState(State):
    def __init__(self,
        origSchedule: List[SchedulingItem],
        requirements: List[SchedulingRequirement],
        courseTeacherMap: Dict[int, List[int]],
        weight: Dict[str, float],
        sessionMax: int,
    ) -> None:
        self.__origSchedule: List[SchedulingItem] = origSchedule
        self.__courseTeacherMap: Dict[int, List[int]] = courseTeacherMap
        self.__computedSchedule: List[SchedulingItem] = self.__generateSchedule(requirements)
        self.__weight: Dict[str, float] = weight
        self.__sessionMax: int = sessionMax
        self.__score: Optional[float] = None

    def __generateSchedule(self, requirements: List[SchedulingRequirement]) -> List[SchedulingItem]:
        result: List[SchedulingItem] = list()
        for req in requirements:
            teachers: List[int] = self.__courseTeacherMap[req.courseID]
            for i in range(req.nsessions):
                item = SchedulingItem(req.classID, req.courseID, choice(teachers), i + req.fromSession, req.fromSession)
                result.append(item)
        return result

    def duplicate(self) -> Any:
        return deepcopy(self)

    def __violatedTeachers(self) -> int:
        result: int = 0
        validTeachersSet: Set[str] = set()
        for item in self.__origSchedule:
            validTeachersSet.add(item.produceTeacherKey())
        for item in self.__computedSchedule:
            key = item.produceTeacherKey()
            if key in validTeachersSet:
                result += 1
            else:
                validTeachersSet.add(key)
        return result

    def __violatedClasses(self) -> int:
        result: int = 0
        validClassesSet: Set[str] = set()
        for item in self.__origSchedule:
            validClassesSet.add(item.produceClassKey())
        for item in self.__computedSchedule:
            key = item.produceClassKey()
            if key in validClassesSet:
                result += 1
            else:
                validClassesSet.add(key)
        return result

    def __moreSessionsOnCourse(self) -> float:
        moreSessions: int = 0
        totalSessions: Dict[str, int] = dict()
        minSession: Dict[str, int] = dict()
        maxSession: Dict[str, int] = dict()
        for item in self.__computedSchedule:
            key = item.produceClassKey()
            if key not in totalSessions:
                totalSessions[key] = 1
                minSession[key] = item.sessionID
                maxSession[key] = item.sessionID
            else:
                totalSessions[key] += 1
                if item.sessionID > maxSession[key]:
                    maxSession[key] = item.sessionID
                if item.sessionID < minSession[key]:
                    minSession[key] = item.sessionID
        for key in totalSessions:
            total = totalSessions[key]
            maxses = maxSession[key]
            minses = minSession[key]
            tmp = maxses - minses + 1 - total
            if tmp > 0:
                moreSessions += tmp
        return moreSessions

    def __calculateScore(self) -> float:
        vteachers: int = self.__violatedTeachers()
        vclasses: int = self.__violatedClasses()
        moreSessions: int = self.__moreSessionsOnCourse()
        score: float = (vteachers*self.__weight["teachers"] + vclasses*self.__weight["classes"] + moreSessions)*(-1.0)
        self.__score = score
        return score

    def __changeSessionRandomly(self):
        item = choice(self.__computedSchedule)
        item.sessionID = randint(item.fromSession, self.__sessionMax)

    def __changeTeacherRandomly(self):
        item = choice(self.__computedSchedule)
        item.teacherID = choice(self.__courseTeacherMap[item.courseID])

    def permuteSchedule(self, ksessions: int, kteachers: int):
        self.__score = None
        for _ in range(ksessions):
            self.__changeSessionRandomly()
        for _ in range(kteachers):
            self.__changeTeacherRandomly()

    def getScore(self) -> float:
        if self.__score is not None:
            return self.__score
        return self.__calculateScore()

    def __gt__(self, other):
        return self.getScore() > other.getScore()

    def __str__(self) -> str:
        result = "==============================\n\
            There are {} original schedules\n\
            There are {} computed schedules:\n\
            {}\n\
            score: {}".format(
                len(self.__origSchedule),
                len(self.__computedSchedule),
                "\n".join(map(str, self.__computedSchedule)),
                self.getScore(),
            )
        return result
