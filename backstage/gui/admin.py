# coding: UTF-8
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

from django.contrib import admin
from backstage.gui.models import *

RegisterClass = (FileStorage,
                 PresetComments,
                 MIDIController,
                 MappingPresetObject,
                 )

for item in RegisterClass:
    admin.site.register(item)
