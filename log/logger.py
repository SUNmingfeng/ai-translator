import os
import sys
from loguru import logger

LOG_FILE = "translation.log"
ROTATION_TIME = "2:00"

class Logger:
    def __init__(self, name="translation", log_dir="logs", debug=False):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_path = os.path.join(log_dir, LOG_FILE)

        logger.remove()

        level = "DEBUG" if debug else "INFO"
        logger.add(sys.stdout, level=level)
        logger.add(log_file_path, rotation=ROTATION_TIME, level="DEBUG")
        self.logger = logger

LOG = Logger( debug=True).logger

if __name__ == "__main__":
    log = Logger(debug=False).logger

    log.debug("This is a debug message.")
    log.info("This is an info message.")
    log.warning("This is a warning message.")
    log.error("This is an error message.")
