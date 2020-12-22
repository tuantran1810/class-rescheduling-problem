from loguru import logger as log
from dataclasses import dataclass
from typing import (
    Dict,
    List,
    Generator,
    Set,
)
import pickle

@dataclass
class SchedulingRequirement:
    classID: int = 0
    courseID: int = 0
    fromSession: int = 0
    nsessions: int = 0

    def __str__(self) -> str:
        return "schedule {} sessions for class {} with the course {} starting from session {}".format (
            self.nsessions, self.classID, self.courseID, self.fromSession
        )

@dataclass
class SchedulingItem:
    classID:     int = 0
    courseID:    int = 0
    teacherID:   int = 0
    sessionID:    int = 0
    fromSession: int = 0

    def produceTeacherKey(self):
        return "{}-{}".format(self.sessionID, self.teacherID)

    def produceClassKey(self):
        return "{}-{}".format(self.sessionID, self.classID)

    def produceClassCourseKey(self):
        return "{}-{}".format(self.classID, self.courseID)

    def __str__(self) -> str:
        return "class {} learn the course {} with teacher {} on the session {}".format(
            self.classID,
            self.courseID,
            self.teacherID,
            self.sessionID,
        )

class TimeTable:
    def __init__(self):
        self._classIDMap        = {}
        self._courseIDMap       = {}
        self._teacherIDMap      = {}
        self._schedulingItems   = []
        self._courseToTeachers  = {}
        self._teacherToCourses  = {}

    @property
    def classIDMap(self):
        return self._classIDMap
    
    @classIDMap.setter
    def classIDMap(self, ids) -> None:
        self._classIDMap = ids

    @property
    def courseIDMap(self):
        return self._courseIDMap

    @courseIDMap.setter
    def courseIDMap(self, ids) -> None:
        self._courseIDMap = ids

    @property
    def teacherIDMap(self):
        return self._teacherIDMap

    @teacherIDMap.setter
    def teacherIDMap(self, ids) -> None:
        self._teacherIDMap = ids

    def addSchedule(self, sche: SchedulingItem):
        self._schedulingItems.append(sche)

    def getSchedule(self, id: int) -> SchedulingItem:
        return self._schedulingItems[id]

    def Build(self):
        self._buildCourseTeacherMap()
        self._buildTeacherCourseMap()

    def _buildCourseTeacherMap(self):
        if len(self._courseIDMap) == 0 or len(self._teacherIDMap) == 0 or len(self._schedulingItems) == 0:
            log.error("IDs map is not initialize yet")
            return
        for courseid in self._courseIDMap:
            teachers = []
            for value in self._schedulingItems:
                if value.courseID == courseid:
                    teachers.append(value.teacherID)
            if len(teachers) == 0:
                log.warning("the {} course does not have any teacher".format(courseid))
            self._courseToTeachers[courseid] = teachers

    def _buildTeacherCourseMap(self):
        if len(self._courseIDMap) == 0 or len(self._teacherIDMap) == 0 or len(self._schedulingItems) == 0:
            log.error("IDs map is not initialize yet")
            return
        for teacherid in self._teacherIDMap:
            courses = []
            for value in self._schedulingItems:
                if value.teacherID == teacherid:
                    courses.append(value.courseID)
            if len(courses) == 0:
                log.warning("the {} teacher does not have any course".format(teacherid))
            self._teacherToCourses[teacherid] = courses

    def allSchedules(self) -> Generator[SchedulingItem, None, None]:
        for item in self._schedulingItems:
            yield item

    @property
    def courseTeachersMap(self):
        return self._courseToTeachers

    @property
    def availableClasses(self) -> List[int]:
        classSet: Set[int] = set()
        for item in self._schedulingItems:
            classSet.add(item.classID)
        return sorted(classSet)

    def limitClasses(self, classes: List[int]) -> None:
        classesSet: Set[int] = set(classes)
        self._schedulingItems = list(filter(lambda x: x.classID in classesSet, self._schedulingItems))

    def __str__(self) -> str:
        soonestSession: int = 1000000
        latestSession: int = 0
        for item in self._schedulingItems:
            if item.sessionID > latestSession:
                latestSession = item.sessionID
            if item.sessionID < soonestSession:
                soonestSession = item.sessionID
        s: str = "There are {} schedules in timetable.\n \
            {} class ids, {} course ids, {} teacher ids.\n \
            soonest session: {}, latest session: {}.\n \
            all available classes: {}".format(
            len(self._schedulingItems), len(self._classIDMap),
            len(self._courseIDMap), len(self._teacherIDMap),
            soonestSession, latestSession, self.availableClasses)
        return s
