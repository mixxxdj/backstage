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
v1_api.register(MIDICompanyResouce())
v1_api.register(MIDIControllerResource())

urlpatterns = patterns('',
        (r'', include(v1_api.urls)))
