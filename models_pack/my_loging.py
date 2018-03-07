#! /usr/bin/env python
# -*- coding: utf8 -*-
import logging
import datetime
import os


if os.environ.get('HEROKU') is not None:
    stream_handler = logging.StreamHandler()
    logging._addHandlerRef(stream_handler)
else:
    logging.basicConfig(format='%(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.DEBUG, filename='logs/util_logs.log')


def info(msg):
    logging.info(msg)


def warning(msg):
    logging.warning(msg)


def error(msg):
    logging.error(msg)