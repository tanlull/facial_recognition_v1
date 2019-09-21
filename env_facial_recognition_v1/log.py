## USAGE 
## import log as logger
## logger.init("logger name",logger.INFO)

import logging
import config

logger  = logging.getLogger('LOG')

INFO = logging.INFO
DEBUG = logging.DEBUG
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

def init(logname,loglevel=config.get("GLOBAL", "loglevel")):
    global logger
    logger  = logging.getLogger(logname)0962536559
    logger.setLevel(loglevel)
    ch = logging.StreamHandler()
    ch.setLevel(loglevel)
    formatter = logging.Formatter('[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.warning("LOG Level is {}".format(logging.getLevelName(logger.getEffectiveLevel())))

def getLevel():
    
    return logging.getLevelName(logger.getEffectiveLevel())

def setLevel(level):
    logger.warning("Overriding Log Level to {}".format(logging.getLevelName(level)))
    logger.setLevel(level)

def debug(msg):
    logger.debug(msg)

def info(msg):
    logger.info(msg)

def warning(msg):
    logger.warning(msg)

def error(msg):
    logger.error(msg)

def critical(msg):
    logger.critical(msg)




