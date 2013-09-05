# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/amaris/dev-mixxx/backstage/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backstage.settings_dev'

from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
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
            else:
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
    for key, value in ret.items():
        if value is not None:
            if os.path.isfile(value) is True:
                with File(open(value, 'r')) as f:
                    filename = os.path.basename(value)
                    try:
                        FileStorage.objects.get(file_name=filename)
                    except Exception, e:
                        print e
                        fs = FileStorage()
                        fs.file_name = filename
                        fs.mapping_preset_id = preset
                        fs.file_type = FileTypeDict.objects.get(category=key)
                        fs.file_size = os.path.getsize(value)
                        fs.file_obj = f
                        fs.save()
                        print "insert a file:%s" % os.path.basename(value)
                    else:
                        print "file already exists"


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


def importOnePreset(path):
    record = parse(path)
    return importPresetData(record)


def importMultiPresets(directory):
    records = midi_parse(directory)
    for record in records:
        importPresetData(record)
    print "all import ok!"


def importPresetData(record):

    try:
        controller = MIDIController.objects.get(controller_name=record[CONTROLLER])
        MappingPresetObject.objects.get(midi_controller=controller,
                                        preset_name=record[NAME],
                                        schema_version=record[SCHEMAVERSION])
    except MultipleObjectsReturned:
        print "already\n"
        return ""
    except ObjectDoesNotExist:
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
        return preset.pid
    else:
        print "preset %s is already exists\n" % record[NAME]
        return ""


if __name__ == "__main__":
    initializedb()
    path = "/home/amaris/dev-mixxx/backstage/backstage/test/controllers"
    importMultiPresets(path)
