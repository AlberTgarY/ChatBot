import logging
import logging.handlers
import datetime
import logging.config
import configparser
import os

# read config file
config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
LOG_path = config.get("path", "inspec_log_path")

def get_log():

    # create folder if doesnt exist
    if not os.path.exists(LOG_path):
        os.mkdir(config.get("path", "inspec_log_path"))

    # configuring logger
    logger = logging.getLogger("Logger1")
    if not logger.handlers:
        logger.propagate = 0
        # set common handler
        handler = logging.handlers.TimedRotatingFileHandler(LOG_path+'Debug_LOG.log', when='midnight', interval=1,
                                                            backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set debug handler
        debug_handler = logging.handlers.TimedRotatingFileHandler(LOG_path+'LOG.log', when='midnight', interval=1,
                                                                  backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        debug_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set level
        debug_handler.setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)

        # set handler
        logger.addHandler(handler)
        logger.addHandler(debug_handler)

    return logger
