#coding: UTF-8

import os
from xml.etree import ElementTree as ET

#root name defination
TREE_INFO = "info"
TREE_CONTROLLER = "controller"

PRESET_NAME = "name"
PICFILES = "picfiles"
PIC = "pic"


def insert_pic_info(path=None):
    """
    insert pic info into the given file
    Input:
        file full path
    """
    if path is None:
        print "input args is error"
        return

    if not os.path.exists(path):
        print "Sorry, our system cannot find this path: %s" % (path)
        return

    tree = ET.parse(path)
    root = tree.getroot()
    controller_tag = root.find(TREE_CONTROLLER)
    pic_tag = ET.Element(PICFILES)
    pic_name = get_pic_name(path)
    if pic_name is not None:
        pic = ET.SubElement(pic_tag, PIC)
        pic.set('name', pic_name)
    controller_tag.insert(1, pic_tag)
    tree.write(path)
    return


def get_pic_name(path=None):
    """
    get picture name, same with preset name
    """
    if path is None:
        print "input args is error"
        return None
    if not os.path.exists(path):
        print "Sorry, our system cannot find this path: %s" % (path)
        return None
    pic_jpg = path.replace('.midi.xml', '.jpg')
    pic_png = path.replace('.midi.xml', '.png')
    pic_gif = path.replace('.midi.xml', '.gif')
    if os.path.exists(pic_jpg):
        return os.path.basename(pic_jpg)
    elif os.path.exists(pic_png):
        return os.path.basename(pic_png)
    elif os.path.exists(pic_gif):
        return os.path.basename(pic_gif)
    else:
        print "no pic files for this preset file%s" % os.path.basename(path)
        return None


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


if __name__ == "__main__":
    midi_insert(path="./../test/controllers")
