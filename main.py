from loguru import logger as log
from algorithms import SchedulingState, SimulatedAnnealingAlgorithm, Handler
from utils import TimeTable, loadTimeTable

N_CLASSES_RESCHEDULE = 20
SESSION_START_RESCHEDULING = 600
EPOCHS = 30
ADJACENCY_STATES = 20

def main():
    log.info("Hello")
    timeTable: TimeTable = loadTimeTable("./data/timetable.pkl")
    log.info(timeTable)
    rescheduleClasses: List[int] = timeTable.availableClasses[:N_CLASSES_RESCHEDULE]
    log.info(f"reschedule for classes: {rescheduleClasses}")
    handler: Handler = Handler(timeTable, rescheduleClasses, SESSION_START_RESCHEDULING, EPOCHS, ADJACENCY_STATES)
    handler.start()

if __name__ == "__main__":
    main()
