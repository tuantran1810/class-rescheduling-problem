from loguru import logger as log
import preprocess

def main():
    pre = preprocess.TimeTableParser('data')
    pre.Parse()
    pre.ToPickle()

if __name__ == "__main__":
    main()
