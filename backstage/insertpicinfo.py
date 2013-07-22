#coding: UTF-8

import os
import sys
from xml.etree import ElementTree as ET


#root name defination
TREE_CONTROLLER = "controller"
PICFILES = "picfiles"


def insert_pic_info(path=None):
    """
    insert pic info into the given file
    Input:
        file full path
    """
    if path is None:
        print "input args is error"
        return None

    if not os.path.exists(path):
        print "Sorry, our system cannot find this path: %s" % (path)
        return None

    tree = ET.parse(path)
    root = tree.getroot()
    controller_tag = root.find(TREE_CONTROLLER)
    pic_tag = ET.Element(PICFILES)
    #ET.SubElement(controller_tag, PICFILES)
    pic_tag.text = "pic Test"
    controller_tag.insert(1, pic_tag)
    tree.write(path)
    return


def test_insert():
    path = "/home/amaris/dev-mixxx/backstage/backstage/test/controllers/Akai-LPD8-RK.midi.xml"
    insert_pic_info(path)


def get_specific_files(path=None):
    """
    Get this path and its child path, which file is endwith
    midi.xml

    Input: folder path input point
    Output: a list which is the full file path
    """
    if path is None:
        print "floder input path is None"
        return None

    if not os.path.exists(path):
        print "Sorry, our system cannot find this path: %s" % (path)
        return None

    ret = []

    for folderpath in os.walk(path):
        for filename in os.listdir(folderpath[0]):
            filepath = os.path.join(folderpath[0], filename)
            if filepath.endswith(".midi.xml"):
                ret.append(filepath)

    return ret


def midi_insert(path=None):
    """
    parse all files in the given folderpath
    Input:path, which is folder
    """
    ret = {}
    retfiles = get_specific_files(path)
    for f in retfiles:
        if f:
            ret[f] = insert_pic_info(f)


def test_get_path():
    path = "/Users/amaris/dev/xmlparse/"
    get_specific_files(path)

def test():
    test_insert()
    test_get_path()

if __name__ == "__main__":
   # midi_insert(path="/home/amaris/dev-mixxx/backstage/backstage/xmlparse/controllers")
    test_insert()
