from loguru import logger as log
from algorithms import Handler, SchedulingState
from utils import TimeTable, loadTimeTable

LIMIT_CLASSES = 2
N_CLASSES_RESCHEDULE = 1
SESSION_START_RESCHEDULING = 600
EPOCHS = 500
ADJACENCY_STATES = 10

def main():
    log.info("Hello")
    timeTable: TimeTable = loadTimeTable("./data/timetable.pkl")
    log.info(timeTable)

    limitedClasses: List[int] = [2, 3, 4, 7, 9, 11, 17, 18, 19, 22]
    log.info(f"limit in {LIMIT_CLASSES} classes: {limitedClasses}")
    timeTable.limitClasses(limitedClasses)
    log.info(timeTable)

    rescheduleClasses: List[int] = [2, 3, 4]
    log.info(f"reschedule for classes: {rescheduleClasses}")
    handler: Handler = Handler(timeTable, rescheduleClasses, SESSION_START_RESCHEDULING, EPOCHS, ADJACENCY_STATES, initTemp=10.0, finalTemp=0.01)
    bestState: SchedulingState = handler.start()

    log.info("===========Phase 2===========")
    bestState.setWeight(
        {
            "classes": 1000.0,
            "teachers": 1000.0,
            "sessions": 1.0,
        }
    )
    bestState.clearScore()
    handlerPhase2: Handler = Handler(timeTable, rescheduleClasses, SESSION_START_RESCHEDULING, EPOCHS*20, ADJACENCY_STATES, initTemp=100.0, finalTemp=0.01, firstState = bestState)
    print(handlerPhase2.start())

if __name__ == "__main__":
    main()
