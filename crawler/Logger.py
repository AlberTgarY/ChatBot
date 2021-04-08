import logging
import logging.handlers
import datetime
import logging.config
import configparser
import os

'''
This file is the Logging module for crawler, it creates 2 kinds of logfile. 
The LOG.log only records the INFO level message and
the Debug_LOG.log will record DEBUG and INFO messages, which includes more detailed information,
author: ZHAN YICHENG 03/04/2021
'''
# read config file
config = configparser.RawConfigParser()
config.read("../cfg/cfg.ini")
LOG_path = config.get("path", "log_path")


def get_log():

    # create folder if doesnt exist
    if not os.path.exists(LOG_path):
        os.mkdir(config.get("path", "log_path"))

    # configuring logger
    logger = logging.getLogger("Logger")
    if not logger.handlers:
        logger.propagate = 0
        # set common handler
        handler = logging.handlers.TimedRotatingFileHandler(LOG_path+'Debug_LOG.log', when='midnight', interval=1,
                                                            backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set debug handler
        info_handler = logging.handlers.TimedRotatingFileHandler(LOG_path+'LOG.log', when='midnight', interval=1,
                                                                  backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        info_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set level
        info_handler.setLevel(logging.INFO)
        logger.setLevel(logging.DEBUG)

        # set handler
        logger.addHandler(handler)
        logger.addHandler(info_handler)

    return logger
