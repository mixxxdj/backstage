#coding: UTF-8

import os
import sys
from xml.etree import ElementTree as ET


#root name defination
TREE_INFO = "info"
TREE_CONTROLLER = "controller"

CONTROLLER_NAME = "name"
CONTROLLER_AUTHOR = "author"
CONTROLLER_DESC = "description"
CONTROLLER_LINKS = "forums"
CONTROLLER_ID = "id"
BASIC_LIST = (CONTROLLER_AUTHOR, CONTROLLER_DESC,
              CONTROLLER_LINKS, CONTROLLER_NAME)
TREE_LIST = (TREE_INFO, TREE_CONTROLLER)


def parse(path=None):
    """
    parse xml into python dict type
    Input:
        file full path
    Output:
        a dict, which can include some midi info
    """
    if path is None:
        print "input args is error"
        return None

    if not os.path.exists(path):
        print "Sorry, our system cannot find this path: %s" % (path)
        return None

    ret = {}
    for e in TREE_LIST:
        ret[e] = {}

    root = ET.parse(path).getroot()
    info_node = root.find(TREE_INFO)
    if info_node is None:
        for e in BASIC_LIST:
            ret[TREE_INFO][e] = None
    else:
        for e in BASIC_LIST:
            node = info_node.find(e)
            ret[TREE_INFO][e] = node.text if node is not None else None

    controller_node = root.find(TREE_CONTROLLER)
    ret[TREE_CONTROLLER][CONTROLLER_ID] = controller_node.attrib[CONTROLLER_ID]

    print ret
    print "\n"
    return ret


def test_parse():
    path = "/Users/amaris/dev/xmlparse/controllers/Akai.midi.xml"
    ret = parse(path)
    print ret


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


def midi_parse(path=None):
    """
    parse all files in input point
    Input:path, which is floder
    Output:a dict, filename is the key, value are the attribute
    """
    ret = {}
    retfiles = get_specific_files(path)
    for f in retfiles:
        if f:
            ret[f] = parse(f)


def test_get_path():
    path = "/Users/amaris/dev/xmlparse/"
    get_specific_files(path)


def test():
    test_parse()
    test_get_path()

if __name__ == "__main__":
    midi_parse(path="/Users/amaris/dev/xmlparse/")
