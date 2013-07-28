#coding: UTF-8

import os
import sys
from xml.etree.ElementTree import ElementTree, Element, SubElement

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/amaris/dev-mixxx/backstage/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backstage.settings_dev'

from backstage.gui.models import FileStorage, MappingPresetObject, FileTypeDict


def export(path):
    root = Element('presets')
    xmlFiles = FileStorage.objects.filter(file_type=FileTypeDict.objects.get(category='xml'))
    for f in xmlFiles:
        pid = f.mapping_preset_id.pid
        print pid
        try:
            status = MappingPresetObject.objects.get(pid=pid).preset_status.category
        except Exception:
            print "this pid is not exists in the database"
        else:
            print status
            preset = SubElement(root, 'preset')
            fname = SubElement(preset, 'filename')
            fname.text = f.file_name
            presetID = SubElement(preset, 'pid')
            presetID.text = pid
            presetStatus = SubElement(preset, 'status')
            presetStatus.text = status
    tree = ElementTree(root)
    tree.write(os.path.join(path, 'mapScript.xml'), encoding='utf-8')

if __name__ == "__main__":
    export(path="./")
