#coding: UTF-8

import os
import sys
from xml.etree.ElementTree import ElementTree, Element, SubElement

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('/home/amaris/dev-mixxx/backstage/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'backstage.settings_dev'

RESOURCE_PATH = "./controllers"
MAP_PATH = "./"
from backstage.gui.models import FileStorage, MappingPresetObject, FileTypeDict


def export_files():
    if not os.path.exists(RESOURCE_PATH):
        os.makedirs(RESOURCE_PATH)
    file_objects = FileStorage.objects.all()
    for obj in file_objects:
        fname = os.path.join(RESOURCE_PATH, obj.file_name)
        if os.path.exists(fname):
            print False
            print obj.file_name
        fdest = open(fname, 'wb')
        try:
            fconcent = obj.file_obj.read()
            fdest.write(fconcent)
        finally:
            fdest.close()


def export(path):
    root = Element('presets')
    xmlFiles = FileStorage.objects.filter(file_type=FileTypeDict.objects.get(category='xml'))
    for xml in xmlFiles:
        pid = xml.mapping_preset_id.pid
        print pid
        try:
            status = MappingPresetObject.objects.get(pid=pid).preset_status.category
        except Exception, err:
            print err
        else:
            print status
            preset = SubElement(root, 'preset')
            preset.set('filename', xml.file_name)
            preset.set('pid', pid)
            preset.set('status', status)
    tree = ElementTree(root)
    tree.write(os.path.join(path, 'mapScript.xml'), encoding='utf-8')

if __name__ == "__main__":
    export(path=MAP_PATH)
    export_files()
