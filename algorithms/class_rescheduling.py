from dataclasses import dataclass
from algorithms.simulated_annealing import State
from typing import List, Dict, Set, Optional
from random import choice, randint

@dataclass
class SchedulingItem:
    classId: int
    courseId: int
    teacherId: int
    sessionId: int
    fromSession: int = -1

    def produceTeacherKey(self):
        return "{}-{}".format(self.sessionId, self.teacherId)

    def produceClassKey(self):
        return "{}-{}".format(self.sessionId, self.classId)

@dataclass
class SchedulingRequirement:
    classId: int
    courseId: int
    fromSession: int
    nsessions: int

class SchedulingState(State):
    def __init__(self, 
        origSchedule: List[SchedulingItem], 
        requirements: List[SchedulingRequirement],
        courseTeacherMap: Dict[int][List[int]],
        weight: Dict[str][float],
        sessionMax: int,
    ) -> None:
        self.__origSchedule: List[SchedulingItem] = origSchedule
        self.__courseTeacherMap: Dict[int][List[int]] = courseTeacherMap
        self.__computedSchedule: List[SchedulingItem] = self.__generateSchedule(requirements)
        self.__weight: Dict[str][float] = weight
        self.__sessionMax = sessionMax
        self.__score: Optional[float] = None

    def __generateSchedule(self, requirements: List[SchedulingRequirement]) -> List[SchedulingItem]:
        result: List[SchedulingItem] = list()
        for req in requirements:
            teachers: List[int] = self.__courseTeacherMap[req.courseId]
            for i in range(req.nsessions):
                item = SchedulingItem(req.classId, req.courseId, choice(teachers), i + req.fromSession, req.fromSession)
                result.append(item)
        return result
    
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

    def __violatedClasses(self):
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

    def __calculateScore(self) -> float:
        vteachers: int = self.__violatedTeachers()
        vclasses: int = self.__violatedClasses()
        score: float = (vteachers*self.__weight["teachers"] + vclasses*self.__weight["classes"])*(-1.0)
        self.__score = score
        return score

    def __changeSessionRandomly(self):
        item = choice(self.__computedSchedule)
        item.sessionId = randint(item.fromSession, self.__sessionRange)

    def __changeTeacherRandomly(self):
        item = choice(self.__computedSchedule)
        item.teacherId = choice(self.__courseTeacherMap[item.courseId])

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
