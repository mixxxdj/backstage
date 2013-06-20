# coding: UTF-8
'''
Created on 

@author: 

Desc: const defination
'''

__all__ = ["", ]

FILE_PIC = "pic"
FILE_XML = "xml"

FILE_CHOICES = (
    (FILE_PIC, u"picture"),
    (FILE_XML, u"xml"),
)

SOURCE_MIXXX = "mixxx"
SOURCE_FORUM = "forum"

PRESET_SOURCE_CHOICES = (
    (SOURCE_MIXXX, u"mixxx offical"),
    (SOURCE_FORUM, u"forum"),
)

CERTIFICATE_PASS = "pass"
CERTIFICATE_FAILED = "failed"
CERTIFICATE_UNDEFINED = "undefined"

CERTIFICATE_CHOICES = (
    (CERTIFICATE_PASS, u"certificated by mixxx"),
    (CERTIFICATE_FAILED, u"Failed"),
    (CERTIFICATE_UNDEFINED, u"still certificating and testing"),
)

#TODO: Add more dict item
