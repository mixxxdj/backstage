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
    print "initialize FileTypeDict ..."
    category = ['xml', 'js', 'pic']
    for c in category:
        try:
            FileTypeDict.objects.get(category=c)
        except Exception:
            ftd = FileTypeDict(category=c)
            ftd.save()
    print "initialize CertificatedOperationDict ..."
    category = ['pass', 'failed', 'undefined']
    for c in category:
        try:
            CertificatedOperationDict.objects.get(category=c)
        except Exception:
            cod = CertificatedOperationDict(category=c)
            cod.save()
    print "initialize MappingPresetSourceDict ..."
    source = ['mixxx', 'forum', 'wiki']
    for s in source:
        try:
            MappingPresetSourceDict.objects.get(source=s)
        except Exception:
            mpsd = MappingPresetSourceDict(source=s)
            mpsd.save()


def importAuthors(record, preset):
    if record[AUTHOR] is not None:
        authors = record[AUTHOR].split(';')
        for author in authors:
            try:
                uname = UserInfo.objects.get(username=author)
            except Exception:
                aut = UserInfo.objects.create(username=author)
                aut.save()
                preset.author.add(aut)
                print "build author %s" % author
            else:
                print "Author %s already exists\n" % author
                preset.author.add(uname)
            print "Authors are all inserted!"
    else:
        try:
            uname = UserInfo.objects.get(username='unknown')
        except Exception:
            aut = UserInfo.objects.create(username='unknown')
            aut.save()
            preset.author.add(aut)
        else:
            preset.author.add(uname)


def importFiles(record, preset):
    ret = {'xml': record[XML], 'pic': record[PIC], 'js': record[JS]}
    fs = FileStorage()
    for key in ret.keys():
        value = ret.get(key)
        if value is not None:
            if os.path.exists(value) is True:
                fs.file_name = os.path.basename(value).split('.')[0]
                fs.mapping_preset_id = preset
                fs.file_type = FileTypeDict.objects.get(category=key)
                fs.file_size = os.path.getsize(value)
                f = open(value)
                fs.file_obj.save(os.path.basename(value), File(f))
                fs.save()
                f.close()
                print "insert a file:%s" % fs.file_name


def importControllers(record, preset):
    cname = record[CONTROLLER]
    try:
        controller = MIDIController.objects.get(controller_name=cname)
    except Exception:
        controller = MIDIController.objects.create(controller_name=cname)
        controller.save()
        preset.midi_controller = controller
        print "create and add a new controller: %s" % cname
    else:
        preset.midi_controller = controller
        print "controller %s is inserted ok!" % cname


def importMixxxVersion(record, preset):
    version = record[MIXXXVERSION]
    try:
        mversion = MixxxVersionDict.objects.get(version=version)
    except Exception:
        mversion = MixxxVersionDict.objects.create(version=version)
        mversion.save()
        preset.mixxx_version = mversion
        print "create and add a new version %s" % version
    else:
        preset.mixxx_version = mversion
        print "version %s is inserted ok!" % version


def importPresetData(path):

    records = midi_parse(path)
    for record in records:
        try:
            MappingPresetObject.objects.get(preset_name=record[NAME])
        except Exception:
            preset = MappingPresetObject()
            print "importPresetData-------\n"
            print record
            print "\n"
            preset.preset_name = record[NAME]
            if record[DESC] is not None:
                preset.description = record[DESC]
            else:
                preset.description = ""

            preset.schema_version = record[SCHEMAVERSION]
            forums = record[FORUM]
            wiki = record[WIKI]

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
            importMixxxVersion(record, preset)
            importControllers(record, preset)
            preset.save()
            # UserInfo and MappingPresetObject is a many-many
            # relationship,before importAuthors should save preset
            importAuthors(record, preset)
            print "==========preset %s is inserted ok==========" % record[NAME]
            importFiles(record, preset)

        else:
            print "preset %s is already exists\n" % record[NAME]
    print "all import ok!"


if __name__ == "__main__":
    initializedb()
    path = "/home/amaris/dev-mixxx/backstage/backstage/xmlparse/controllers"
    importPresetData(path)
