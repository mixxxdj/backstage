# -*- coding: UTF-8 -*-
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

from django.conf.urls.defaults import *
from backstage.api.api_resources import *
from tastypie.api import Api

v1_api = Api(api_name="v1")
v1_api.register(MIDIControllerResource())
v1_api.register(MappingPresetObjectResource())
v1_api.register(PresetCommentsResource())
v1_api.register(FileStorageResource())
v1_api.register(UserInfoResource())
v1_api.register(FileTypeDictResource())
v1_api.register(MixxxVersionDictResource())
v1_api.register(CertificatedOperationDictResource())
v1_api.register(MappingPresetSourceDictResource())

urlpatterns = patterns('',
        (r'', include(v1_api.urls)))
