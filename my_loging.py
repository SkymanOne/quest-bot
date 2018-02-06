import logging
import datetime

logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG, filename='logs/util_' +
                                                  str(datetime.datetime.now().time()) + '.log')


def info(msg):
    logging.info(msg)


def warning(msg):
    logging.warning(msg)


def error(msg):
    logging.error(msg)