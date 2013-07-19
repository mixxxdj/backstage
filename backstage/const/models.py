# coding: UTF-8
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc: dict table

'''

from django.db import models

from backstage.const import FILE_XML, FILE_PIC, FILE_JS, FILE_CHOICES
from backstage.const import SOURCE_FORUM, SOURCE_MIXXX, PRESET_SOURCE_CHOICES
from backstage.const import CERTIFICATE_FAILED, CERTIFICATE_PASS
from backstage.const import CERTIFICATE_UNDEFINED
from backstage.const import CERTIFICATE_CHOICES


class FileTypeDict(models.Model):
    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=FILE_CHOICES,
                                verbose_name=u"File type")

    class Meta:
        verbose_name = "File Types"
        verbose_name_plural = "File Types"

    def __unicode__(self):
        return self.get_category_display()

class MixxxVersionDict(models.Model):
    """
    """
    version = models.CharField(max_length=200, blank=False, unique=True,
                               verbose_name=u"mixxx software version")

    class Meta:
        verbose_name = "Mixxx Version"
        verbose_name_plural = "Mixxx Version"

    def __unicode__(self):
        return self.version


class CertificatedOperationDict(models.Model):

    """
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=CERTIFICATE_CHOICES,
                                verbose_name=u"certification")

    class Meta:
        verbose_name = "certification"
        verbose_name_plural = "certification"

    def __unicode__(self):
        return self.get_category_display()


class MappingPresetSourceDict(models.Model):
    """
    """
    source = models.CharField(max_length=30, blank=False, unique=True,
                              choices=PRESET_SOURCE_CHOICES,
                              verbose_name=u"preset mapping")

    class Meta:
        verbose_name = "preset source"
        verbose_name_plural = "preset source"

    def __unicode__(self):
        return self.get_source_display()
