from src.Psych import Psych
from src.Logger import log_info, log_init

if __name__ == "__main__":
    log_init()

    psych = Psych()
    log_info("Work started")
    psych.run()