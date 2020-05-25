from dotenv import load_dotenv, find_dotenv

from cui.common import App
import sys
from data_processing.generate_data import generate_data
from data_analyzing.schedule import AnalyzeSchedule

load_dotenv(find_dotenv())


if __name__ == "__main__":
    if len(sys.argv) != 1:
        if sys.argv[1] == "--analyze":
            AnalyzeSchedule.analyze()
        else:
            generate_data()
    else:
        print("course project")
        App().run()
