__author__ = 'jmpews'
import logging
def initLogging(logFilename='run.log'):
    """Init for logging
    """
    logging.basicConfig(
        level = logging.DEBUG,
        format = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        datefmt = '%m-%d %H:%M',
        filename = logFilename,
        filemode = 'w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)