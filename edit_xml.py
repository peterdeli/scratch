#!/bin/env python
# Peter Delevoryas
# Version 0.2.2 3/15/2016
# new features:
# 1) generate map file from entire doc
#    used as input to scrub/unscrub
# changes - This one will not use unique map keys -
# SCRUBBED:/path:value

#import pdb

from random import randint, seed
import random
import os
import os.path
import sys
import re
from xml.dom.minidom import *
from xml.dom.minidom import Node
import xml.dom.minidom


#pdb.set_trace()

global path_list
path_list = []

# raw config
global CONFIG_FILE

# all the elements (*) in the raw config
global CONFIG_FILE_ELEMENTS

# boolean
global CONFIG_FILE_LOADED

# number of CONFIG_FILE_ELEMENTS
global CONFIG_FILE_SIZE

# minidom.parse() result, also used for writing out config
global CONFIG_FILE_TREE

# generated from CONFIG_MAP_FILE
global CONFIG_MAP_DICT

# used for generating config map file
global CONFIG_MAP_FILE

# xml paths as unix paths
global CONFIG_PATH_LIST

global CONFIG_PATHS
global CONFIG_SCRUB_PATH_FILE
global CONFIG_SCRUB_PATH_LIST
global CONFIG_SCRUB_PATHS_LOADED
global DEFAULT_SCRUBBED_MAPFILE
global FIELD_DELIMITER
global MENU_LIST
global NODE_LIST
global RANDOM_INDEX
global RANDOM_LIST
global SCRUB_KEY
global SCRUBBED_CONFIG_FILE
global SCRUBBED_CONFIG_MAP_LIST
global SCRUBBED_CONFIG_MAP_LIST_LOADED
global UNSCRUBBED_CONFIG_FILE

# for unscrubbing config files
global UNSCRUB_MAP_FILE
# generated from UNSCRUB_MAP_FILE
global UNSCRUB_CONFIG_MAP_DICT
# generated from UNSCRUB_CONFIG_MAP_DICT
global UNSCRUB_CONFIG_PATHS

global UNSCRUB_CONFIG_MAP_DICT_LOADED
global UNSCRUB_CONFIG_PATHS_LOADED
global UNSCRUB_MAP_FILE_LOADED

global HEADING
global VERSION
global PYTHON_MAJOR_VERSION
global PYTHON_MINOR_VERSION

# variables for traversing doc and generating paths
VERSION = '0.1'
HEADING = "\n#########################\n" + "XML Config Doc Scrubber" + "\nVersion "  + VERSION + "\n#########################\n"


# all the elements (*) in the raw config
CONFIG_FILE_ELEMENTS = []
CONFIG_FILE_LOADED = False
CONFIG_FILE_SIZE = 0
CONFIG_FILE_TREE = ""
CONFIG_FILE=""
CONFIG_MAP_DICT = {}
CONFIG_MAP_FILE = ""
CONFIG_PATH = ''
CONFIG_PATH_LIST = []
CONFIG_PATHS = []
CONFIG_PATHS_LOADED = False
CONFIG_SCRUB_PATH_FILE = ""
CONFIG_SCRUB_PATH_LIST = []
CONFIG_SCRUB_PATHS_LOADED = False
DEFAULT_SCRUBBED_MAPFILE = "scrubbed_config_map.out"

SCRUBBED_CONFIG_MAP_LIST_LOADED = False
UNSCRUB_CONFIG_MAP_DICT_LOADED = False
UNSCRUB_CONFIG_PATHS_LOADED = False
UNSCRUB_MAP_FILE_LOADED = False

FIELD_DELIMITER = ":"
map_list = []
max_random=99999
min_random=999
NODE_LIST = []
RANDOM_INDEX = 0
RANDOM_LIST = []
SCRUB_KEY="SCRUBBED"
scrub_list = []
SCRUBBED_CONFIG_FILE = ""
SCRUBBED_CONFIG_MAP_LIST = []
scrubDelim = ':'
scrubKeyword = 'SCRUBBED'
UNSCRUBBED_CONFIG_FILE = ""
UNSCRUB_MAP_FILE = ""
UNSCRUB_CONFIG_MAP_DICT = {}
UNSCRUB_CONFIG_PATHS = []
PYTHON_MAJOR_VERSION = 2
PYTHON_MINOR_VERSION = 4

def print_heading():
    global HEADING
    print HEADING
def getRandom():
    global RANDOM_INDEX
    global RANDOM_LIST
    rand = RANDOM_LIST[ RANDOM_INDEX ]
    RANDOM_INDEX += 1
    return rand

def load_random_nums(size):
    global RANDOM_INDEX
    global RANDOM_LIST
    global CONFIG_FILE_TREE
    RANDOM_LIST = [ randint(min_random, max_random) for count in xrange(size) ]
    return

#def check_version():
#	if sys.version_info < (2,4):
#		print "This program was tested with version 2.4 and greater, version lower than 2.4 detected"
#		return -1
def init():
    #initialize
    #print "init"
#    version=check_version()
#    if version < 0:
#	exit( version )

    minimum_python_version_float = PYTHON_MAJOR_VERSION + ( PYTHON_MINOR_VERSION / 10.0 )
    current_python_version_float = sys.version_info[0] + ( sys.version_info[1] / 10.0 )
    if current_python_version_float < minimum_python_version_float:
        print "Minimum python version required is " + str(minimum_python_version_float) + "\n" + "Current version: " + str(current_python_version_float)
        exit( 1 )
    
        
    print_heading()
    load_menu_items()

def load_menu_items():
    #load_menu_items
    global MENU_LIST
    
    # load config - gen: paths
    # scrub config  - input: paths output: scrubbed config, map file 
    # unscrub config - input map file from scrub output: config with values
    
    print "load_menu_items"

    MENU_LIST = {
                1:{"Load Config File":load_config},
                3:{"Load Config Paths for Scrubbing":load_config_scrub_paths},
                4:{"Load Map File for Unscrubbing":load_unscrubbing_map},
                5:{"Find/Change a Field":edit_node},
                6:{"Save Current Config File":save_config},
                7:{"Save Current Config Map":save_map},
                2:{"Save Current Config Paths":save_paths},
                8:{"Scrub Current Config File":scrub_config},
                9:{"UnScrub Current Config File":unscrub_config},
                }

    print "loaded menu list"
    
def load_config_unscrub_paths():
    print "load_config_unscrub_paths"
    global CONFIG_UNSCRUB_PATHS_LOADED
    global CONFIG_UNSCRUB_PATH_LIST
    global CONFIG_UNSCRUB_PATH_FILE
    global FIELD_DELIMITER
    mode='r'
    unscrub_file = raw_input("Enter the Unscrub file to load: ")
    
    unscrub_file  = unscrub_file.strip()
    if file_accessible(unscrub_file, mode) == False:
        print "Unable to read file " + unscrub_file
        return False
    else:
        CONFIG_UNSCRUB_PATH_FILE = unscrub_file
        
    unscrubfile = open(CONFIG_UNSCRUB_PATH_FILE, mode)
    CONFIG_UNSCRUB_PATH_LIST = [line.strip() for line in unscrubfile.readlines() ]
#     for line in unscrubfile.readlines():
#         line=line.strip()
#         CONFIG_UNSCRUB_PATH_LIST.append(line)
    
    print "UnScrub path file " + CONFIG_UNSCRUB_PATH_FILE + " loaded."
    CONFIG_UNSCRUB_PATHS_LOADED = True
    unscrubfile.close() 
    return

def load_config_scrub_paths():
    print "load_config_scrub_paths"
            # def
    global CONFIG_SCRUB_PATHS_LOADED
    global CONFIG_SCRUB_PATH_LIST
    global CONFIG_SCRUB_PATH_FILE
    global FIELD_DELIMITER
    mode='r'
    scrub_file = raw_input("Enter the scrub file to load: ")
    
    scrub_file  = scrub_file.strip()
    if file_accessible(scrub_file, mode):
        CONFIG_SCRUB_PATH_FILE = scrub_file
    else:
        print "Unable to read file " + scrub_file
        return False

        
    scrubfile =  open(CONFIG_SCRUB_PATH_FILE,mode)
    CONFIG_SCRUB_PATH_LIST = [line.strip() for line in scrubfile.readlines() ]
#     for line in scrubfile.readlines():
#         line=line.strip()
#         CONFIG_SCRUB_PATH_LIST.append(line)
    
    print "Scrub path file " + CONFIG_SCRUB_PATH_FILE + " loaded."
    CONFIG_SCRUB_PATHS_LOADED = True
    scrubfile.close()
    return

def create_config_map():
    print "create_config_map"
    # 1) map every line
    # scrub123:/a/b/c:abc123

def scrub_config():
    global CONFIG_FILE
    global CONFIG_PATH_LIST
    global CONFIG_PATHS_LOADED
    global CONFIG_SCRUB_PATH_FILE
    global CONFIG_SCRUB_PATH_LIST
    global SCRUBBED_CONFIG_MAP_LIST
    global SCRUBBED_CONFIG_MAP_LIST_LOADED
    
    # 2 options
    # 1) CONFIG_FILE has >SCRUBBED:<real value>< element
    # 2) CONFIG_FILE has only ><real value><, and CONFIG_PATHS is populated
    
    if not CONFIG_PATHS_LOADED:
        print "You must first select a config file"
        return
    if not CONFIG_SCRUB_PATHS_LOADED:
        print "You must first select a scrub mapping file"
        return
    
    config_file_str="Configuration File: "
    config_file_str_len=len(config_file_str)
    
    scrub_file_str="Scrub file: "
    scrub_file_str_len=len(scrub_file_str)
    
    fmt="%" + str( config_file_str_len if config_file_str_len > scrub_file_str_len else  scrub_file_str_len ) + "s"
    r_config_file_str=fmt % config_file_str
    r_scrub_file_str = fmt % scrub_file_str
    
    while True:
        choice = raw_input("Press return to scrub the current configuration file:\n" + 
                           r_config_file_str + CONFIG_FILE + "\n" + r_scrub_file_str  + 
                           CONFIG_SCRUB_PATH_FILE + "\n(Press 'c' to cancel): " )
        choice=choice.strip()
        if choice == "":
            print "Scrubbing configuration .."
            for node in NODE_LIST:
                node_path = str(node[1])
                # check for array subscripts
                r_search = node_path + "\[[0-9].*\]$"
                match_list = [match.group(0) for item in CONFIG_SCRUB_PATH_LIST for match in [ re.match(r_search, item) ] if match]
                
                if len(match_list) > 1:
                    print "duplicate paths for " + node_path + " : " + str(match_list)
                
                if node_path in CONFIG_SCRUB_PATH_LIST:
                    sys.stdout.write( "Scrubbing data for " + node_path )
                    #random_key = str(getRandom())
                    # build map dict
                    #SCRUBBED_CONFIG_MAP_LIST.append( node_path + FIELD_DELIMITER + SCRUB_KEY + str(getRandom()) + FIELD_DELIMITER + node[0].data )
                    # SCRUBBED_CONFIG_MAP_LIST.append(  SCRUB_KEY + random_key  + FIELD_DELIMITER + node_path + FIELD_DELIMITER + node[0].data )
                    #node[0].data = SCRUB_KEY + random_key

                    SCRUBBED_CONFIG_MAP_LIST.append(  SCRUB_KEY +  FIELD_DELIMITER + node_path + FIELD_DELIMITER + node[0].data )
                    node[0].data = SCRUB_KEY
                    print " .. Done"
                    
            SCRUBBED_CONFIG_MAP_LIST_LOADED = True
            print "Scrub complete for config"
            print "Saving config "
            
            print "Saving map file"
            if save_map():
                print "Map file saved"
            else:
                print "Unable to save map file."
                
            break
        
        elif choice == 'c':
            print "Cancelling scrub"
            break
        else:
            print "Incorrect response"
            continue
    return
    
def unscrub_config():
    global CONFIG_FILE
    global CONFIG_PATH_LIST
    global CONFIG_PATHS_LOADED
    global CONFIG_SCRUB_PATH_FILE
    global CONFIG_SCRUB_PATH_LIST
    global SCRUBBED_CONFIG_MAP_LIST
    
    global UNSCRUB_MAP_FILE
    global UNSCRUB_CONFIG_PATHS
    global FIELD_DELIMITER
    global UNSCRUB_CONFIG_MAP_DICT
    
    global UNSCRUB_MAP_FILE_LOADED
    global UNSCRUB_CONFIG_MAP_DICT_LOADED
    global UNSCRUB_CONFIG_PATHS_LOADED
    global NODE_LIST
    
    # 2 options
    # 1) CONFIG_FILE has >SCRUBBED:<real value>< element
    # 2) CONFIG_FILE has only ><real value><, and CONFIG_PATHS is populated
    
    if not UNSCRUB_MAP_FILE_LOADED:
        print "You must first load an unscrub map file"
        return

    if not UNSCRUB_CONFIG_MAP_DICT_LOADED:
        print "The unscrub map has not been loaded. Please load an unscrub map file."
        return
    while True:
        choice = raw_input("Press return to unscrub the current config " + CONFIG_FILE + " unscrub file: " + UNSCRUB_MAP_FILE + ", 'c' to cancel." )
        choice=choice.strip()
        if choice == "":
            print "UnScrubbing configuration .."
            for node in NODE_LIST:
                
                #keymatch = [ km for key in UNSCRUB_CONFIG_MAP_DICT.keys() if key == node[0].data ]
                node_path = str(node[1])
                for key in UNSCRUB_CONFIG_MAP_DICT.keys():

                    if key == node_path:
                        # changed: no longer unique scrubbed value
                        # must compare path as well
                        print "Unscrubbing path " + node_path + ":" + node[0].data
                        node[0].data = UNSCRUB_CONFIG_MAP_DICT[key][1]
                        
#                 if node_path in UNSCRUB_CONFIG_PATHS:
#                     key_match = ""
#                     random_key = str(getRandom())
#                     sys.stdout.write( "UnScrubbing data for " + node_path )
#                     # get correct scrub key
#                     #(key,path,value) = line.strip().split(FIELD_DELIMITER)
#                     #UNSCRUB_CONFIG_MAP_DICT[key] = (path,value)
#                     
#                     # for key in UNSCRUB_CONFIG_MAP_DICT.keys():
#                     # UNSCRUB_CONFIG_PATHS.append( UNSCRUB_CONFIG_MAP_DICT[key][0] )
#                     # node[0].data should match UNSCRUB_CONFIG_MAP_DICT[key]
#                     #unscrub_data_key = [ key_match for key in UNSCRUB_CONFIG_MAP_DICT.keys() if key == node[0].data]
#                     for key in UNSCRUB_CONFIG_MAP_DICT.keys():
#                         if key == node[0].data:
#                             unscrub_data = UNSCRUB_CONFIG_MAP_DICT[key][1]
#                             node[0].data = unscrub_data
#                     print " .. Done"
                    
                
            print "UnScrub complete for config"
            break
        elif choice == 'c':
            print "Cancelling scrub"
            break
        else:
            print "Incorrect response"
            continue
    return

    
def quit():
    print "quit() called, exiting .."
    exit
    
def load_scrubbed_config():
    # def
    print "load_scrubbed_config"
def file_exists(filepath):
    try:
        if os.path.isfile(filepath):
            return True
        else:
            return False
    except: 
        e = sys.exc_info()[0]
        return False
        
    
def file_accessible(filepath, mode):
        #Check if a file exists and is accessible.
        e=""
        f_exists=False
        try:
            if os.path.isfile(filepath):
                f_exists = True
            f = open(filepath, mode)
            f.close()

        #except IOError as e:
        except: 
            e = sys.exc_info()[0]
            return False
        
        if mode == "w" or mode == "W" and f_exists == False:
            os.remove(filepath)
            
        return True

def print_loaded_map():
    global CONFIG_MAP_FILE
    mode = 'r'
    if file_accessible(CONFIG_MAP_FILE, mode):
        print "loaded map file: " + CONFIG_MAP_FILE
        return True
    else:
        print "Unable to load map file " + CONFIG_MAP_FILE
        return False
    
def print_loaded_config():
    global CONFIG_FILE
    mode = 'r'
    if file_accessible(CONFIG_FILE, mode):
        print "loaded config: " + CONFIG_FILE
        return True
    else:
        print "No config file loaded"
        return False

# build dictionary of node/path
def walk_xml_node(path, node):
    replace_data =''
    unscrubbed_data = ''
    global NODE_LIST
    global CONFIG_PATH_LIST
    global FIELD_DELIMITER
    
    # array of hashes
    # 
    if node.nodeType == node.TEXT_NODE:
        if node.data.strip() != "":
            # the end of the path
            sys.stdout.write(".")
            
            NODE_LIST.append(( node, path ))
            CONFIG_PATH_LIST.append(path)
            
            #create global config_mapping
            # 
            # /path/to/nodel -> data
            map_str = path + " -> " + node.data
            #print map_str
            path_list.append(map_str)
            #scrub_list.append( path + scrubDelim + replace_data + scrubDelim + unscrubbed_data )
            scrub_list.append( SCRUB_KEY  + FIELD_DELIMITER + path + FIELD_DELIMITER + node.data )
            
        else:
            # 'directories'
            if path not in path_list:
                sys.stdout.write(".")
                #print  path
                path_list.append(path)
            
    else:
        for cnode in node.childNodes:
            if cnode.nodeName == "#text":
                walk_xml_node( path, cnode)
            else:  
                walk_xml_node( path + "/" + cnode.nodeName, cnode)
    
    
    return 0

def load_config():
        # def
        global CONFIG_FILE
        global CONFIG_FILE_TREE
        global CONFIG_FILE_LOADED
        global CONFIG_FILE_SIZE
        global CONFIG_FILE_ELEMENTS
        global CONFIG_PATHS_LOADED
        
        mode='r'
        config = raw_input("Enter the config.xml file name: ")
        CONFIG_FILE = config.strip()
        if file_accessible(CONFIG_FILE, mode) == False:
            print "Unable to read config file " + config
            CONFIG_FILE_LOADED = False
            return False
        
        CONFIG_FILE_TREE = xml.dom.minidom.parse(CONFIG_FILE)
        print "config file " + config + " loaded."
        CONFIG_FILE_ELEMENTS = CONFIG_FILE_TREE.getElementsByTagName('*')
        CONFIG_FILE_SIZE = CONFIG_FILE_ELEMENTS.length
        load_random_nums(CONFIG_FILE_SIZE)
        CONFIG_FILE_LOADED = True
        
        print "Generating paths .. "
        result = walk_xml_node("", CONFIG_FILE_TREE)
        print "\ndone\n"
        
        if result == 0:
            CONFIG_PATHS_LOADED = True
            # write config_map from scrub_list[]
        
        #return 0 if result == 0 else -1
        
        
def load_unscrubbed_config():
        # def1
        print "load_unscrubbed_config():"

def scrub_field():
        # def
        print "scrub_field():"

def edit_node():
        # def
        print "edit_node():"
        node_list = []
        node_path = ""
        tag_path = raw_input("Enter the path of the tag to edit: ")
        # find in node list
        tag_path = tag_path.strip()
        for item in NODE_LIST:
            node_path = str(item[1])
            if tag_path in node_path:
                node_list.append(item)
        # node_list = [ item  for item in NODE_LIST if item[1] == tag_path ]
        if len(node_list) < 1:
            print "No matches found for path " + tag_path
            return
        else:
            print "matches: "
            node_indexes = []
            for idx, node in enumerate(node_list):
                node_indexes.append((idx + 1))
                print str( (idx + 1 ) ) + ") path: " + str(node[1]) + " value: " +  str(node[0].data)
                
            selections = raw_input ( "Select items to change: " ).strip()
            selection_list = selections.split()
            if [selection for selection in selection_list if selection in str(node_indexes)]:
                print("Enter the new value for selection(s) ('c' to cancel): ")
                for index in selection_list:
                    idx = int(index)
                    real_index = ( idx - 1 )
                    new_value = raw_input( "Enter the new value for " + str( index  ) + ") path: " + str(node_list[real_index][1]) + " value: " +  str(node_list[real_index][0].data) + ": " )
                    new_value = new_value.strip()
                    node_list[real_index][0].data = new_value
            else:
                    print "Incorrect Selections: " + selections
        raw_input("Press 'Enter' to return to main menu: ")
def edit_scrubbed_node():
        # def
        print "edit_scrubbed_node():"

def unscrub_node():
        # def
        print " unscrub_node():"

def translate_quotes( text_list ):
    text_list = text_list.replace("&quot;", "\"")
    return text_list
                 
def save_config():
    global CONFIG_FILE
    global CONFIG_FILE_TREE
        # def
    print "save_config():"
    outfile = CONFIG_FILE + ".out"
    if file_accessible(outfile, 'w') == False :
        print "Unable to save config file. Check for existing config file: " + outfile + " or permissions."
        return
    out_handle = open(outfile, "w")
    CONFIG_FILE_TREE.writexml(out_handle,encoding='UTF-8')
    out_handle.close()
    ## Change all &quot; to ""
    print "Filtering out double-quote encodings .."
    if file_accessible(outfile, 'r') == False:
        print "Unable to open config file " + outfile + " for reading."
        return
    
    out_handle = open(outfile, "r")
    all_text = out_handle.read()
    out_handle.close()
    #all_text = text.replace("&quot;", "\"")
    all_text = translate_quotes(all_text)
    out_handle = open(outfile, "w")
    out_handle.write(all_text)
    out_handle.close()
    print ".. done."
    print "Config saved to " + outfile


def main_menu():
    # main_menu
    global MENU_LIST
    print "main_menu"
    print "\nSelect an option:\n"
    descr="NO CHOICE"
    
    index=1
    menu_len = len(MENU_LIST)
    menu_keys = MENU_LIST.keys()
    sorted_keys = sorted(menu_keys)
    #1:{"load config file":load_config},
    for item in sorted_keys:
#     for item in MENU_LIST.keys():
        #                 1:{"load config file":load_config},
            descr = MENU_LIST[item].keys()[0]
            print  str(item) + ") " + descr
            index += 1
        
    choice = raw_input( "\nChoice: (1-" + str(menu_len) + "), 'q' to quit: " )
    choice=choice.strip()
    if choice == 'q':
        return choice
    elif choice == '':
        print "Please make a selection"
        return
    elif choice.isdigit() == False or int(choice) < 1 or int(choice) > menu_len :
        print "Incorrect choice. please select a number between 1 and " + str(menu_len)
        # replace with return
        #main_menu()
        return
    else:
        print "You selected " + choice + "): " + MENU_LIST[int(choice)].keys()[0]
        #go = raw_input(  "Press return to run " + choice  + ") ( " + str(MENU_LIST[int(choice)].values()[0]) + ")"  )
        #go = raw_input(  "Press return to run " + choice  + ") ( " + str(MENU_LIST[int(choice)].keys()[0]) + " ) ('c' to cancel): "  ).strip()
        # run the function
        go = ""
        if go == "":
            MENU_LIST[int(choice)].values()[0]()
        elif go == "c":
            return
        else:
            print "Incorrect response"
            
        
    return
    
def main():
    # main
    init()
    print "main"
    loop = True
    while loop:
        choice = main_menu()
        if choice == 'q':
            loop = False
            quit()
            
    
def parse_doc():
    print "parse_doc"

def load_map():
    print "load map"
            # def   
    global CONFIG_MAP_FILE
    global CONFIG_PATHS
    global FIELD_DELIMITER
    mode='r'
    mapfile = raw_input("Enter the map file to load: ")
    
    CONFIG_MAP_FILE = mapfile.strip()
    if file_accessible(CONFIG_MAP_FILE, mode) == False:
        print "Unable to read map file " + CONFIG_MAP_FILE
        return False
    
    mapfile = open(CONFIG_MAP_FILE,mode)
    for line in mapfile.readlines():
        has_delim = FIELD_DELIMITER in line 
        if has_delim == False:
            print "No field delimiters found in mapfile entry: " + line
            continue
        else: 
            [key,value] = line.strip().split(FIELD_DELIMITER)
            CONFIG_MAP_DICT[key] = value 
        
    CONFIG_PATHS = CONFIG_MAP_DICT.keys()
    
    print "Map file " + CONFIG_MAP_FILE + " loaded."
    print "Config path list created from " + CONFIG_MAP_FILE
    mapfile.close()
    return

    
def load_unscrubbing_map():
    print "load_unscrubbing_map"
    global UNSCRUB_MAP_FILE
    global UNSCRUB_CONFIG_PATHS
    global FIELD_DELIMITER
    global UNSCRUB_CONFIG_MAP_DICT
    global UNSCRUB_CONFIG_MAP_DICT_LOADED
    global UNSCRUB_CONFIG_PATHS_LOADED
    global UNSCRUB_MAP_FILE_LOADED
    mode='r'
    mapfile = raw_input("Enter the map file to load: ")
    
    UNSCRUB_MAP_FILE = mapfile.strip()
    if file_accessible(UNSCRUB_MAP_FILE, mode) == False:
        print "Unable to read map file " + UNSCRUB_MAP_FILE
        return False
    #  scrubbed123:/a/b/c:myValue
    mapfile =  open(UNSCRUB_MAP_FILE,mode)
    for line in mapfile.readlines():
        has_delim = FIELD_DELIMITER in line
        if has_delim == False:
            print "No field delimiters found in mapfile entry: " + line
            continue
        else:    
            (key,path,value) = line.strip().split(FIELD_DELIMITER,2)
            UNSCRUB_CONFIG_MAP_DICT[path] = (key,value)
            
    for key in UNSCRUB_CONFIG_MAP_DICT.keys():
        UNSCRUB_CONFIG_PATHS.append( UNSCRUB_CONFIG_MAP_DICT[key] )
        
    
    print "Map file " + UNSCRUB_MAP_FILE + " loaded."
    print "Config mappings created from " + UNSCRUB_MAP_FILE
    UNSCRUB_CONFIG_MAP_DICT_LOADED = True
    UNSCRUB_CONFIG_PATHS_LOADED = True
    UNSCRUB_MAP_FILE_LOADED = True
    mapfile.close()
    return
    
    
def load_config_paths():
    print "load_config_paths"
    # 
    
def save_map():
    print "save_map"
    global SCRUBBED_CONFIG_MAP_LIST
    global DEFAULT_SCRUBBED_MAPFILE
    global SCRUBBED_CONFIG_MAP_LIST_LOADED
    
    mode="w"
    # don't overwrite existing
    if file_exists( DEFAULT_SCRUBBED_MAPFILE ):
        print "Unable to save map file. Either found existing map file: " + DEFAULT_SCRUBBED_MAPFILE + " or error checking if it already exists. Please rename or move."
        return False
    
    if SCRUBBED_CONFIG_MAP_LIST_LOADED == False:
        print "No configuration map loaded"
        return False
        
    
    mapfile = open(DEFAULT_SCRUBBED_MAPFILE,mode)
    for line in SCRUBBED_CONFIG_MAP_LIST:
        mapfile.write( line + "\n" )
            
    mapfile.close()
    print "Saved config mapfile " + DEFAULT_SCRUBBED_MAPFILE
    
    return True

def save_paths():
    print "save_paths"
    global CONFIG_PATHS_LOADED
    global CONFIG_PATH_LIST
    config_path_list = []
    
    if CONFIG_PATHS_LOADED:
        outfile = CONFIG_FILE + ".paths.out"
        if os.path.isfile(outfile):
            print "Unable to save path file. Found existing path file: " + outfile + ". Please rename or move."
            return
        out_handle = open(outfile, "w")
        # map duplicates as arrays
        ar_idx = 1
        for path in CONFIG_PATH_LIST:
            config_path_list = [ path for var in CONFIG_PATH_LIST if var == path ]
            if len(config_path_list) > 1:
                for p in config_path_list:
                    subscr = "[" + str(ar_idx) + "]"
                    ar_idx += 1
                    p = p + subscr
                    CONFIG_PATH_LIST[CONFIG_PATH_LIST.index(path)] = p
                ar_idx = 1
                config_path_list = []
            
        for path in CONFIG_PATH_LIST:
            out_handle.write(path + "\n")
        out_handle.close()
        print "Config path  saved to " + outfile
    else:
        print "No config file loaded"
        
    return
        
    
main()
