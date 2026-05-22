import logging
import os


class ProjectLogger:

    def __init__(self, log_dir="logs"):

        os.makedirs(log_dir, exist_ok=True)

        log_path = os.path.join(
            log_dir,
            "system.log"
        )

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_path),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(
            "DroneSystem"
        )

    def info(self, message):

        self.logger.info(message)

    def warning(self, message):

        self.logger.warning(message)

    def error(self, message):

        self.logger.error(message)