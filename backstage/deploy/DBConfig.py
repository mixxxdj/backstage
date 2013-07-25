# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/amaris/dev-mixxx/backstage/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backstage.settings_dev'
from backstage.const.models import *
from backstage.deploy.parse import midi_parse


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
        authors = record[PRESET_AUTHOR].split(';')
        controller_ID = record[CONTROLLER_ID]
        pic_file = record[PIC]
        js_file = record[JS]
        xml_file = 
        forums = record[FORUM_LINK]
        wiki = record[WIKI_LINK]
        description = record[PRESET_DESC]
        preset_name = record[PRESET_NAME]
        mixxx_version = record[MIXXXVERSION]
        schema_version = record[SCHEMAVERSION]


    pgdb_conn.close()
    print "initializedb ok! leaving ..."
if __name__ == "__main__":
    path="/home/amaris/dev-mixxx/backstage/backstage/xmlparse/controllers"
