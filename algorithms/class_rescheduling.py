from dataclasses import dataclass
from algorithms.simulated_annealing import State
from typing import List, Dict, Set
from random import choice

@dataclass
class SchedulingItem:
    classId: int
    courseId: int
    teacherId: int
    sessionId: int

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
    ) -> None:
        self.__origSchedule: List[SchedulingItem] = origSchedule
        self.__courseTeacherMap = courseTeacherMap
        self.__computedSchedule: List[SchedulingItem] = self.__generateSchedule(requirements)

        self.__validTeachersSet: Set[str] = set()
        for item in self.__origSchedule:
            self.__validTeacherSet.add(item.produceTeacherKey())

        self.__validClassesSet: Set[str] = set()
        for item in self.__origSchedule:
            self.__validClassesSet.add(item.produceClassKey())

    def __generateSchedule(self, requirements: List[SchedulingRequirement]) -> List[SchedulingItem]:
        result: List[SchedulingItem] = list()
        for req in requirements:
            teachers: List[int] = self.__courseTeacherMap[req.courseId]
            for i in range(req.nsessions):
                item = SchedulingItem(req.classId, req.courseId, choice(teachers), i + req.fromSession)
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
