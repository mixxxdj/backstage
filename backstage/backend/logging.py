# -*- coding: UTF-8 -*-
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''
#TODO Singleton for logging

from django.utils.log import getLogger

logger = getLogger('django')


def loginfo(p="", label=""):
    logger.info("***"*10)
    logger.info(label)
    logger.info(p)
    logger.info("---"*10)
