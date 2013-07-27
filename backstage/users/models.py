# coding: UTF-8
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''
from django.db import models
from backstage.backend.utilities import get_uuid


class UserInfo(models.Model):
    """
    """
    userid = models.CharField(unique=True, blank=False, max_length=50,
                              verbose_name="id", primary_key=True,
                              default=get_uuid)
    email = models.EmailField(max_length=50, blank=True)
    username = models.CharField(blank=False, max_length=100, unique=True)
    homepage_url = models.URLField(max_length=200, blank=True)
    location = models.CharField(blank=True, max_length=50)
    irc_nickname = models.CharField(blank=True, max_length=50)

    class Meta:
        verbose_name = "user info"
        verbose_name_plural = "user info"

    def __unicode__(self):
        return self.username
