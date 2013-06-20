# coding: UTF-8
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

import datetime

from django.db import models
from django.conf import settings

from backstage.const.models import *
from backstage.users.models import *
from backstage.backend.utilities import get_uuid


class MIDIController(models.Model):
    """
    """
    mid =  models.CharField(unique=True, blank=False, max_length=50,
                            verbose_name="id", primary_key=True,
                            default=get_uuid)
    company = models.ForeignKey(MIDICompanyDict, blank=False)
    description = models.CharField(max_length=500, blank=True)
    controller_name = models.CharField(max_length=100, blank=False, unique=True)
    
    class Meta:
        verbose_name = "midi controller"
        verbose_name_plural = "midi controller"

    def __unicode__(self):
        return self.controller_name


class MappingPresetObject(models.Model):
    """
    """
    pid =  models.CharField(unique=True, blank=False, max_length=50,
                            verbose_name="id", primary_key=True,
                            default=get_uuid)
    author = models.ForeignKey(UserInfo, blank=False)
    url = models.URLField(blank=False)
    description = models.TextField(blank=True)
    preset_source = models.ForeignKey(MappingPresetSourceDict, blank=False)
    preset_status = models.ForeignKey(CertificatedOperationDict, blank=False)
    mixxx_version = models.ForeignKey(MixxxVersionDict, blank=False)
    preset_name = models.CharField(max_length=100, unique=True, blank=False)
    midi_controller = models.ForeignKey(MIDIController, blank=False)
    add_date = models.DateTimeField(blank=False,
                                    default = lambda:datetime.datetime.now())

    class Meta:
        verbose_name = "midi controller preset"
        verbose_name_plural = "midi controller preset"

    def __unicode__(self):
        return self.preset_name


class PresetComments(models.Model):
    """
    """
    mid =  models.CharField(unique=True, blank=False, max_length=50,
                            verbose_name="id", primary_key=True,
                            default=get_uuid)
    comments = models.TextField(blank=True)
    comment_author = models.CharField(max_length=40, blank=False)
    ratings = models.FloatField(blank=False, default=0.0)
    preset_mapping_uuid = models.ForeignKey(MappingPresetObject, blank=False)
    date = models.DateTimeField(blank=False, 
                                default = lambda:datetime.datetime.now())

    class Meta:
        verbose_name = "preset comments"
        verbose_name_plural = "preset comments"

    def __unicode__(self):
        return self.mid


class FileStorage(models.Model):
    """
    """
    fid =  models.CharField(unique=True, blank=False, max_length=50,
                            verbose_name="id", primary_key=True,
                            default=get_uuid)
    mapping_preset_id = models.ForeignKey(MappingPresetObject, blank=False)
    file_type = models.ForeignKey(FileTypeDict, blank=False)
    file_size = models.CharField(max_length=50, blank=True, default=None)
    file_showname = models.CharField(max_length=50, blank=False)
    file_obj = models.FileField(upload_to=settings.PROCESS_FILE_PATH + "/%Y/%m/%d")

    class Meta:
        verbose_name = "File Storage"
        verbose_name_plural = "File Storage"

    def __unicode__(self):
        return self.fid
