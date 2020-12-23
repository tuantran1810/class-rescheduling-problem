import sys
from loguru import logger as log
from runner import Runner

def main():
    log.info("Start!!!")
    configPath, dataPath, outputPath = sys.argv[1], sys.argv[2], sys.argv[3]
    runner: Runner = Runner(configPath, dataPath)
    runner()
    log.info("End!!!")

if __name__ == "__main__":
    main()
