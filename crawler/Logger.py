import logging
import logging.handlers
import datetime
import logging.config


def get_log():
    # configuring logger
    logger = logging.getLogger("Logger")
    if not logger.handlers:
        logger.propagate = 0
        # set common handler
        handler = logging.handlers.TimedRotatingFileHandler('../Log/LOG.log', when='midnight', interval=1,
                                                            backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set debug handler
        debug_handler = logging.handlers.TimedRotatingFileHandler('../Log/Debug_LOG.log', when='midnight', interval=1,
                                                                  backupCount=7, atTime=datetime.time(0, 0, 0, 0))
        debug_handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

        # set level
        logger.setLevel(logging.INFO)
        debug_handler.setLevel(logging.DEBUG)

        # set handler
        logger.addHandler(handler)
        logger.addHandler(debug_handler)

    return logger
