#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging


def init(file_name=None, log_level=logging.DEBUG):
    """
    Args:
        file_name: log file name.
        log_level: log level.
    """
    _format = '<%(levelname)s> %(asctime)s (%(process)d, %(thread)d) [%(module)s.%(funcName)s:%(lineno)d] %(message)s'
    if file_name:
        logging.basicConfig(filename=file_name, format=_format)
    else:
        logging.basicConfig(format=_format)
    logger = logging.getLogger()
    logger.setLevel(log_level)

