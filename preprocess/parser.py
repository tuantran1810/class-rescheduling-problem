import csv
import pickle
import os
import utils
from datetime import datetime, timedelta
from loguru import logger as log
from typing import (
    Dict,
    Optional,
    Generic,
    Generator,
    TypeVar,
    List,
    Set,
    Tuple,
    Hashable,
    Any,
    Union,
)

CLASSES_ID_NAME         = "classes.csv"
COURSES_ID_NAME         = "courses.csv"
TEACHER_ID_NAME         = "teachers.csv"
TIMETABLE_NAME          = "timetable.csv"
TIMETABLE_OUTPUT_NAME   = "timetable.pkl"
START_OF_TIMETABLE      = datetime.strptime('01/01/2020', "%m/%d/%Y")
WEEK_DAY_MAP            = {2: 0, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}

class CsvParser:
    def __init__(self, filePath: str):
        self.__filePath = filePath

    def readLine(self) -> Generator[List, None, None]:
        with open(self.__filePath, "r") as csvfile:
            csvreader = csv.reader(csvfile) 
            for line in csvreader:
                yield line

    def readLines(self) -> List:
        return list(self.readLine())

    def __str__(self):
        info = os.stat(self.__filePath)
        return "{}".format(info)

class TimeTableParser:
    def __init__(self, folderData):
        self.path = folderData
        self.timeTable = utils.TimeTable()

    def _buildClasses(self):
        _reader = CsvParser(self.path + "/" + CLASSES_ID_NAME)
        _classid = {}
        for line in _reader.readLine():
            if line is not None and len(line) == 2:
                _classid[line[0]] = line[1]
            else:
                log.warn("Incorrect format: {}".format(line))
        self.timeTable.classIDMap = _classid

    def _buildCourses(self):
        _reader = CsvParser(self.path + "/" + COURSES_ID_NAME)
        _courseid = {}
        for line in _reader.readLine():
            if line is not None and len(line) == 2:
                _courseid[line[0]] = line[1]
            else:
                log.warn("Incorrect format: {}".format(line))
        self.timeTable.courseIDMap = _courseid

    def _buildTeachers(self):
        _reader = CsvParser(self.path + "/" + TEACHER_ID_NAME)
        _teacherid = {}
        for line in _reader.readLine():
            if line is not None and len(line) == 2:
                _teacherid[line[0]] = line[1]
            else:
                log.warn("Incorrect format: {}".format(line))
        self.timeTable.teacherIDMap = _teacherid

    def _buildTimeTable(self):
        _reader = CsvParser(self.path + "/" + TIMETABLE_NAME)
        for line in _reader.readLine():
            if line is not None and len(line) == 9:
                start = datetime.strptime(line[4], "%m/%d/%Y")
                end = datetime.strptime(line[5], "%m/%d/%Y")
                startWeekDay = start.weekday()
                actualWeekDay = WEEK_DAY_MAP[int(line[6])]
                offset = 0
                if startWeekDay > actualWeekDay:
                    offset = 6 - startWeekDay + actualWeekDay + 1
                else:
                    offset = actualWeekDay - startWeekDay + 1
                start = start + timedelta(days=offset)
                for n in range(0, int((end - start).days) + 1, 7):
                    curr = start + timedelta(days=n)
                    duration = (curr - START_OF_TIMETABLE).days
                    if line[7] == 1:
                        duration = 2*duration
                    else:
                        duration = 2*duration + 1
                    self.timeTable.addSchedule(utils.SchedulingItem(line[1], line[2], line[3], duration))

    def Parse(self):
        self._buildClasses()
        self._buildCourses()
        self._buildTeachers()
        self._buildTimeTable()
        self.timeTable.Build()

    def ToPickle(self):
        with open(self.path + "/" + TIMETABLE_OUTPUT_NAME, 'wb') as handle:
            pickle.dump(self.timeTable, handle, protocol=pickle.HIGHEST_PROTOCOL)
