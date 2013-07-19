# -*- coding: UTF-8 -*-
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

from django.conf.urls.defaults import *
from django.db.models import Avg 
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie import fields

from backstage.const.models import *
from backstage.gui.models import *
from backstage.users.models import *

class MIDIControllerResource(ModelResource):

    class Meta:
        queryset = MIDIController.objects.all()
        resource_name = "midi/controller"
        allowed_methods = ["get"]
        authentication = Authentication()
        authorization = Authorization()
        filtering = {'controller_name': ALL}

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
        resource_name = "midi/presetsource"
        allowed_methods =["get"]

class MappingPresetObjectResource(ModelResource):

    author = fields.ToManyField(UserInfoResource, 'author')
    preset_source = fields.ForeignKey(MappingPresetSourceDictResource,
            'preset_source')
    preset_status = fields.ForeignKey(CertificatedOperationDictResource,
            'preset_status')
    version = fields.ForeignKey(MixxxVersionDictResource, 'mixxx_version')
    controller_name = fields.ForeignKey(MIDIControllerResource, 'midi_controller')

    class Meta:
        queryset = MappingPresetObject.objects.all()
        resource_name = "midi/preset"
        allowed_methods = ["get"]
        filtering = {'pid' : ALL,
                'preset_name' : ALL,
                'midi_controller' : ALL_WITH_RELATIONS}

    def dehydrate(self, bundle):
        pid = bundle.data["pid"]
        controller_name = MappingPresetObject.objects.get(pid=pid).midi_controller.controller_name
        preset_source = MappingPresetObject.objects.get(pid=pid).preset_source.source
        preset_status = MappingPresetObject.objects.get(pid=pid).preset_status.category
        version = MappingPresetObject.objects.get(pid=pid).mixxx_version.version
        bundle.data["controller_name"] = controller_name
        bundle.data["preset_source"] = preset_source
        bundle.data["preset_status"] = preset_status
        bundle.data["version"] = version
        bundle.data["picture_file"] = FileStorage.objects.get(mapping_preset_id=pid,file_type=FileTypeDict.objects.get(category=FILE_PIC)).file_obj.url
        #bundle.data["js_file"] = FileStorage.objects.get(mapping_preset_id=pid,file_type=FileTypeDict.objects.get(category=FILE_JS)).file_obj
        bundle.data["xml_file"] = FileStorage.objects.get(mapping_preset_id=pid,file_type=FileTypeDict.objects.get(category=FILE_XML)).file_obj.url
        comments = PresetComments.objects.filter(preset_mapping_uuid=pid)
        bundle.data["avg_ratings"] = comments.all().aggregate(Avg('ratings'))['ratings__avg']
        authorList = bundle.data["author"]
        authors = []
        for aut in authorList:
            authorID = aut.split('/')[-2]
            authors.append(UserInfo.objects.get(userid=authorID).username)
        bundle.data["author"] = authors
        return bundle


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
        resource_name = "presetfile"
        allowed_methods = ["get"]
        filtering = {'mapping_preset_id': ALL_WITH_RELATIONS,
                     'file_type': ALL_WITH_RELATIONS,
                     'file_name': ALL}

    def dehydrate(self, bundle):
        fid = bundle.data["id"]
        bundle.data["file_type"] = FileStorage.objects.get(id=fid).file_type.category
        bundle.data["mapping_preset_id"] = FileStorage.objects.get(id=fid).mapping_preset_id.pid
        return bundle
