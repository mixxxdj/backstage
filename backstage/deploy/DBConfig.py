# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/amaris/dev-mixxx/backstage/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backstage.settings_dev'
from backstage.const.models import *
from backstage.users.models import *
from backstage.gui.models import *
from backstage.deploy.parse import *
from django.core.files import File


def initializedb():
    print "initializedb enter ..."
    print "initialize FileTypeDict ..."
    category = ['xml', 'js', 'pic']
    for c in category:
        ftd = FileTypeDict(category=c)
        ftd.save()
    print "initialize CertificatedOperationDict ..."
    category = ['pass', 'failed', 'undefined']
    for c in category:
        cod = CertificatedOperationDict(category=c)
        cod.save()
    print "initialize MappingPresetSourceDict ..."
    source = ['mixxx', 'forum', 'wiki']
    for s in source:
        mpsd = MappingPresetSourceDict(source=s)
        mpsd.save()


def importPresetData(path):
    records = midi_parse(path)
    for record in records:
        preset = MappingPresetObject()

        authors = record[PRESET_AUTHOR].split(';')
        for author in authors:
            aut = UserInfo.objects.create(username=author)
            preset.author.add(aut)

        controller = MIDIController.objects.create(controller_name=record[CONTROLLER_ID])
        preset.midi_controller = controller

        preset.preset_name = record[PRESET_NAME]
        preset.description = record[PRESET_DESC]
        preset.mixxx_version = record[MIXXXVERSION]
        preset.schema_version = record[SCHEMAVERSION]
        forums = record[FORUM_LINK]
        wiki = record[WIKI_LINK]
        if forums is not None:
            preset.url = forums
            preset.preset_source = MappingPresetSourceDict.objects.get(source='forum')
        elif wiki is not None:
            preset.url = wiki
            preset.preset_source = MappingPresetSourceDict.objects.get(source='wiki')
        else:
            preset.url = "www.mixxx.org"
            preset.preset_source = MappingPresetSourceDict.objects.get(source='mixxx')
        preset.preset_status = CertificatedOperationDict.objects.get(category='pass')
        preset.save()

        xml_file = record[XML]
        pic_file = record[PIC]
        js_file = record[JS]
        ret = {'xml': xml_file, 'pic': pic_file, 'js': js_file}
        fs = FileStorage()
        for key in ret.keys():
            value = ret.get(key)
            if value is not None:
                fs.file_name = os.path.basename(value).split('.')[0]
                fs.mapping_preset_id = preset
                fs.file_type = FileTypeDict.objects.get(category=key)
                f = open(value)
                fs.file_obj.save(os.path.basename((value), File(f)))
                f.close()
                fs.save()

if __name__ == "__main__":
    initializedb()
    path = "/home/amaris/dev-mixxx/backstage/backstage/xmlparse/controllers"
    importPresetData(path)
