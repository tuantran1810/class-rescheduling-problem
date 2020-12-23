import yaml
from loguru import logger as log
from algorithms import Handler, SchedulingState, OptimalWeight
from utils import TimeTable, loadTimeTable
from typing import Dict, Any, List, Tuple, Callable

def getHandlers(config: Dict[str, Any], timeTableData: TimeTable) -> Tuple[Callable[[], Handler], Callable[[SchedulingState], Handler]]:
    limitedClasses: List[int] = list()
    if "all_classes" in config:
        limitedClasses = config["all_classes"]
    
    if len(limitedClasses) > 0:
        timeTableData.limitClasses(limitedClasses)
    log.info(f"Time table:\n{timeTableData}")

    rescheduledClasses: List[int] = config["rescheduled_classes"]
    startSession: int = config["first_rescheduled_session"]
    endSession: int = config["last_rescheduled_session"]
    adjStates: int = config["adjacency_states"]
    
    phase1: Dict[str, Any] = config["phase1"]
    phase2: Dict[str, Any] = config["phase2"]
    weight1: Dict[str, float] = phase1["weight"]
    weight2: Dict[str, float] = phase2["weight"]
    epochs1: int = phase1["epochs"]
    epochs2: int = phase2["epochs"]
    initTemp1: float = phase1["init_temp"]
    initTemp2: float = phase2["init_temp"]
    finalTemp1: float = phase1["final_temp"]
    finalTemp2: float = phase2["final_temp"]

    outputPath: str = config["output_path"]
    log.info(f"Reschedule for classes: {rescheduledClasses} from session {startSession} to {endSession}, output at: {outputPath}")

    def handler1() -> Handler:
        log.info(f"Run SA Phase 1 with {adjStates} adjacency states, {epochs1} epochs, weight: {weight1}, temp range: {initTemp1}-{finalTemp1}")

        handler: Handler = Handler(
            timeTableData,
            rescheduledClasses,
            startSession,
            endSession,
            epochs1,
            adjStates,
            OptimalWeight(weight1["classes"], weight1["teachers"], weight1["sessions"]),
            initTemp1,
            finalTemp1,
            outputPath,
            None,
        )
        return handler

    def handler2(state: SchedulingState) -> Handler:
        log.info(f"Run SA Phase 2 with {adjStates} adjacency states, {epochs2} epochs, weight: {weight2}, temp range: {initTemp2}-{finalTemp2}")

        handler: Handler = Handler(
            timeTableData,
            rescheduledClasses,
            startSession,
            endSession,
            epochs2,
            adjStates,
            OptimalWeight(weight2["classes"], weight2["teachers"], weight2["sessions"]),
            initTemp2,
            finalTemp2,
            outputPath,
            state,
        )
        return handler
    return handler1, handler2

class Runner:
    def __init__(self, configPath: str, dataPath: str):
        self.__timeTable: TimeTable = loadTimeTable(dataPath)
        with open(configPath) as fd:
            config: Dict[str, Any] = yaml.load(fd, Loader = yaml.FullLoader)
            self.__getHandler1, self.__getHandler2 = getHandlers(config, self.__timeTable)

    def __call__(self) -> None:
        handler1: Handler = self.__getHandler1()
        log.info("Start running Phase 1")
        state: SchedulingState = handler1.start()
        handler1.dumpStatLogging()
        log.info(f"Done Phase 1. Output state: {state}")

        handler2: Handler = self.__getHandler2(state)
        log.info("Start running Phase 2")
        state: SchedulingState = handler2.start()
        handler2.dumpStatLogging()
        log.info(f"Done Phase 2. Output state: {state}")
