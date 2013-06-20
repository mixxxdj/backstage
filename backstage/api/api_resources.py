# -*- coding: UTF-8 -*-
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

from django.conf.urls.defaults import *

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields

from backstage.const.models import *
from backstage.gui.models import *
from backstage.users.models import *


class MIDICompanyResouce(ModelResource):
    class Meta:
        queryset = MIDICompanyDict.objects.all()
        resource_name = "midi/company"
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {'company_name': ALL}

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<company_name>[\w\d_.-]+)/$" \
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),\
                name="api_dispatch_detail"),]


class MIDIControllerResource(ModelResource):
    company = fields.ForeignKey(MIDICompanyResouce, 'company')

    class Meta:
        queryset = MIDIController.objects.all()
        resource_name = "midi/controller"
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {'company': ALL_WITH_RELATIONS,
                     'controller_name': ALL}

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<controller_name>[\w\d_.-]+)/$" \
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),\
                name="api_dispatch_detail"),]
