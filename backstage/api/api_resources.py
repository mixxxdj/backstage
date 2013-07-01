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
        filtering = {'company_name': ALL,
                     'id':ALL}

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

class MappingPresetObjectResource(ModelResource):
    author = fields.ForeignKey(UserInfoResource, 'author')
    preset_source = fields.ForeignKey(MappingPresetSourceDictResource,
            'preset_source')
    preset_status = fields.ForeignKey(CertificatedOperationDictResource,
            'preset_status')
    version = fields.ForeignKey(MixxxVersionDictResource, 'mixxx_version')
    controller = fields.ForeignKey(MIDIControllerResource, 'midi_controller')

    class Meta:
        queryset = MappingPresetObject.objects.all()
        resource_name = "midi/preset"
        allowed_methods = ["get"]
        filtering = {'pid':ALL,
                'preset_name':ALL,
                'midi_controller':ALL}
    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/(?P<preset_name>[\w\d_.-]+)/$" \
                % self._meta.resource_name,self.wrap_view('dispatch_detail'),\
                name="api_dispatch_detail"),]
class PresetCommentsResource(ModelResource):
    preset_mapping_uuid = fields.ForeignKey(MappingPresetObjectResource,
            'preset_mapping_uuid')
    
    class Meta:
        queryset = PresetComments.objects.all()
        resource_name = "midi/preset/comment"
        allowed_methods = ["get"]
    
class FileStorageResource(ModelResource):
    mapping_preset_id = fields.ForeignKey(MappingPresetObjectResource,
            "mapping_preset_id")
    file_type = fields.ForeignKey(FileTypeDictResource, "file_type")

    class Meta:
        queryset = FileStorage.objects.all()
        resource_name = "midi/preset/file"
        allowed_methods = ["get"]
class UserInfoResource(ModelResource):

    class Meta:
        queryset = UserInfo.objects.all()
        resource_name ="user/info"
        allowed_methods = ["get"]
class FileTypeDictResource(ModelResource):

    class Meta:
        queryset = FileTypeDict.objects.all()
        resource_name = "midi/preset/file/type"
        allowed_methods = ["get"]
class MixxxVersionDictResource(ModelResource):
    class Meta:
        queryset = MixxxVersionDict.objects.all()
        resource_name = "mixxxversion"
        allowed_methods = ["get"]
class CertificatedOperationDictResource(ModelResource):
    class Meta:
        queryset = CertificatedOperationDict.objects.all()
        resource_name = "certification/status"
        allowed_methods = ["get"]
class MappingPresetSourceDictResource(ModelResource):
    class Meta:
        queryset = MappingPresetSourceDict.objects.all()
        resource_name = "midi/preset/source"
        allowed_methods =["get"]

