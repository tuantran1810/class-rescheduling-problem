from loguru import logger as log
from dataclasses import dataclass
from typing import (
    Dict,
)
import pickle

@dataclass
class SchedulingItem:
    classID:   int = 0
    courseID:  int = 0
    teacherID: int = 0
    seasonID:  int = 0

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

    def __str__(self):
        s = "There are {} schedule in timetable.\n \
            {} class id, {} course id, {} teacher id".format(
            len(self._table), len(self._classIDMap),
            len(self._courseIDMap), len(self._teacherIDMap))
