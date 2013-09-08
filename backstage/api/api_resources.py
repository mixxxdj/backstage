# -*- coding: UTF-8 -*-
'''
Created: 2013-06-20
Author: weixin
Email: weixindlut@gmail.com
Desc:

'''

from django.conf.urls.defaults import *
from django.db.models import Avg
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from django.db.models import Q
from django.db.models import Max

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash
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
        resource_name = "user/info"
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
        allowed_methods = ["get"]


class MappingPresetObjectResource(ModelResource):

    author = fields.ToManyField(UserInfoResource, 'author')
    preset_source = fields.ForeignKey(MappingPresetSourceDictResource,
                                      'preset_source')
    preset_status = fields.ForeignKey(CertificatedOperationDictResource,
                                      'preset_status')
    version = fields.ForeignKey(MixxxVersionDictResource,
                                'mixxx_version')
    controller_name = fields.ForeignKey(MIDIControllerResource,
                                        'midi_controller')

    class Meta:
        queryset = MappingPresetObject.objects.all()
        resource_name = "midi/preset"
        allowed_methods = ["get"]
        filtering = {'pid': ALL,
                     'preset_name': ALL,
                     'midi_controller': ALL_WITH_RELATIONS}

    def getAuthor(self, bundle):
        authorList = bundle.data["author"]
        authors = []
        for aut in authorList:
            authorID = aut.split('/')[-2]
            try:
                authorname = UserInfo.objects.get(userid=authorID).username
            except Exception:
                pass
            else:
                authors.append(authorname)
        return authors

    def getFile(self, bundle, filetype):
        pid = bundle.data["pid"]
        fileURL = ""
        try:
            fileURL = FileStorage.objects.get(mapping_preset_id=pid,
                                              file_type__category=filetype).file_obj.url
        except Exception:
            pass
        return fileURL

    def getAvgRatings(self, bundle):
        pid = bundle.data["pid"]
        avg = 0
        try:
            comments = PresetComments.objects.filter(preset_mapping_uuid=pid)
        except Exception:
            return avg
        else:
            avg = comments.all().aggregate(Avg('ratings'))['ratings__avg']
            return avg

    def dehydrate(self, bundle):
        pid = bundle.data["pid"]
        try:
            preset = MappingPresetObject.objects.get(pid=pid)
        except Exception:
            pass
        else:
            controller_name = preset.midi_controller.controller_name
            preset_source = preset.preset_source.source
            preset_status = preset.preset_status.category
            version = preset.mixxx_version.version

            bundle.data["controller_name"] = controller_name
            bundle.data["preset_source"] = preset_source
            bundle.data["preset_status"] = preset_status
            bundle.data["version"] = version
            bundle.data["js_file"] = self.getFile(bundle, FILE_JS)
            bundle.data["xml_file"] = self.getFile(bundle, FILE_XML)
            bundle.data["picture_file"] = self.getFile(bundle, FILE_PIC)
            bundle.data["avg_ratings"] = self.getAvgRatings(bundle)
            bundle.data["author"] = self.getAuthor(bundle)
        return bundle

    def prepend_urls(self):
        return [url(r"^(?P<resource_name>%s)/search%s$" %
                    (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('get_search'),
                    name="api_get_search"),
                url(r"^(?P<resource_name>%s)/updatecheck%s$" %
                    (self._meta.resource_name, trailing_slash()),
                    self.wrap_view('update_check'),
                    name="api_update_check"), ]

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        queryList = request.GET.getlist('q')
        if len(queryList) > 0:
            qList = Q(preset_name__icontains=queryList[0])
            for i in range(1, len(queryList)):
                qList = qList | Q(preset_name__icontains=queryList[i])
            sqs = MappingPresetObject.objects.filter(qList)
        else:
            sqs = MappingPresetObject.objects.all()
        objects = []
        for result in sqs:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }
        self.log_throttled_access(request)
        return self.create_response(request, object_list)

    def update_check(self, request ,**kwargs):
        self.method_check(request, allowed=['get'])
        self.throttle_check(request)
        queryDict = request.GET.dict()
        status = CertificatedOperationDict.objects.get(category=CERTIFICATE_PASS)
        object_list = {
            'objects': result
        }
        if queryDict.has_key('preset_name') and queryDict.has_key('controller'):
            try:
                controller=MIDIController.objects.get(controller_name=queryDict.get('controller'))
            except Exception, e:
                print e
            else:
                results = MappingPresetObject.objects.filter(preset_name=queryDict.get('preset_name'),
                                                             midi_controller=controller,
                                                             preset_status=status)
                if len(results) > 0:
                    result = results.order_by("schema_version")
        self.log_throttled_access(request)
        return self.create_response(request, object_list)


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
    file_obj = fields.FileField(attribute="file_obj")
    class Meta:
        queryset = FileStorage.objects.all()
        resource_name = "presetfile"
        allowed_methods = ["get"]
        filtering = {'mapping_preset_id': ALL_WITH_RELATIONS,
                     'file_type': ALL_WITH_RELATIONS,
                     'file_name': ALL}
