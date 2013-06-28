# coding: UTF-8
'''
Created: 2013-06-21
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''
from django.db import models
from backstage.const.models import *

class MixxxUpdate(models.Model):
    """
    """
    description = models.CharField(max_length=500, blank=True)
    version = models.ForeignKey(MixxxVersionDict, blank=False)
    name = models.CharField(max_length=100, unique=True, blank=False)
    download_url = models.URLField(blank=False)

    class Meta:
        verbose_name = "Mixxx Update"
        verbose_name_plural = "Mixxx Update"
    def __unicode__(self):
        return self.name
