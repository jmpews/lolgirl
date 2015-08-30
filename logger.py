__author__ = 'jmpews'
import logging
def initLogging(logFilename='run.log'):
    """Init for logging
    """
    # logging.basicConfig(
    #     level = logging.NOTSET,
    #     format = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
    #     datefmt = '%m-%d %H:%M',
    #     filename = logFilename,
    #     filemode = 'w')

    logger=logging.getLogger()
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    logfile=logging.FileHandler(logFilename)
    logfile.setLevel(logging.NOTSET)
    logfile.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.NOTSET)
    console.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(logfile)
    return logger