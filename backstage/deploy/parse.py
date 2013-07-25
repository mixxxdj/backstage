#coding: UTF-8
import os
from xml.etree import ElementTree as ET

#root name defination
MIXXXVERSION = "mixxxVersion"
SCHEMAVERSION = "schemaVersion"

TREE_INFO = "info"
TREE_CONTROLLER = "controller"

NAME = "name"
AUTHOR = "author"
DESC = "description"
FORUM = "forums"
WIKI = "wiki"
CONTROLLER = "id"
SCRIPTFILES = "scriptfiles"
PICFILES = "picfiles"

FILE = "file"
PIC = "pic"
JS = "js"

BASIC_LIST = (AUTHOR, DESC, FORUM, WIKI, NAME)


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
    ret[XML] = path
    root = ET.parse(path).getroot()
    ret[MIXXXVERSION] = root.get(MIXXXVERSION)
    ret[SCHEMAVERSION] = root.get(SCHEMAVERSION)

    info_node = root.find(TREE_INFO)
    if info_node is None:
        for e in BASIC_LIST:
            ret[e] = None
    else:
        for e in BASIC_LIST:
            node = info_node.find(e)
            ret[e] = node.text if node is not None else None

    controller_node = root.find(TREE_CONTROLLER)
    ret[CONTROLLER] = controller_node.attrib[CONTROLLER] if controller_node is not None else None

    script_node = controller_node.find(SCRIPTFILES)
    if script_node is None:
        ret[JS] = None
    else:
        script_file = script_node.find(FILE)  # currently only get one JS file
        ret[JS] = script_file.get("filename") if script_file is not None else None

    pic_node = controller_node.find(PICFILES)
    if pic_node is None:
        ret[PIC] = None
    else:
        pic_file = pic_node.find(PIC)
        ret[PIC] = pic_file.get("name") if pic_file is not None else None
    print "\n"
    return ret


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
    ret = []
    retfiles = get_specific_files(path)
    for f in retfiles:
        if f:
            ret.append(parse(f))
    return ret
