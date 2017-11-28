#!/usr/bin/env python
""" walks specified disk locations, collects metadata about files and folders. """

from config import DEFAULT_FOLDERS
from classes import File, Node

import sys
import os
import datetime
print('python version ', sys.version)
try:
    from scandir import walk as scandir
    print('found scandir.walk, will use that')
except:
    from os import walk as scandir
    print('didnt find scandir.walk, will use os.walk')

if sys.platform in ['Windows',  'win32']:
    import ctypes


__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@mail.mcgill.ca"
__status__ = "Beta"


HOME = os.path.expanduser("~")


def scan(locations,  ignores):
    """ Walks through the file system and analyzes the files and folders"""
    startTime = datetime.datetime.now()

    node_lists = []
    temp_filename_set = set()
    temp_foldername_set = set()
    dirs_analyzed = 0
    files_analyzed = 0

    # Search and mark the default folders found in the file system
    if sys.platform in ['Windows',  'win32']:
        default_locations = {os.path.join(HOME, folder) for folder in DEFAULT_FOLDERS["win"]}
        iTunes_folder = os.path.join(HOME, "My Music\iTunes")
        ignores.append(itunes_folder)
    elif sys.platform in ['darwin']:
        default_locations = {os.path.join(HOME, folder) for folder in DEFAULT_FOLDERS["mac"]}
        apps_folder = os.path.join(HOME, "Applications")
        itunes_folder = os.path.join(HOME, "Music/iTunes")
        library_folder = os.path.join(HOME, "Library")
        ignores.append(apps_folder)
        ignores.append(itunes_folder)
        ignores.append(library_folder)
    elif sys.platform in ['linux',  'linux2',  'linux3']:
        default_locations = {os.path.join(HOME, folder) for folder in DEFAULT_FOLDERS["linux"]}
    else:
        raise "Platform not detected"

    for location in locations:
        norm_location = str(location)
        the_nodes = {}
        temp_nodes = {}
        node_id_counter = 0
        file_id_counter = 0

        def add_depths(node_id, depth):
            """ assigns depth to node, does same for children, their children... """
            temp_node = the_nodes[node_id]
            temp_node.depth = depth
            for child in temp_node.children:
                add_depths(child, depth + 1)
            the_nodes[node_id] = temp_node

        def is_hidden_file(root, f):
            """ checks to see if file is hidden (OS-sensitive) """
            if sys.platform in ['Windows',  'win32']:
                try:
                    full_path = os.path.join(root, f)
                    attrs = ctypes.windll.kernel32.GetFileAttributesW(full_path)
                    assert attrs != -1
                    result = bool(attrs & 2)
                except (AttributeError, AssertionError):
                    result = False
                return result
            else: #POSIX style hidden files. TODO: add provision for mac 'hidden' flag as users can manually hide folders using this mac-specific flag.
                if str(f).startswith('.'):
                    return True
                else:
                    return False

        def is_symlink_file(root, f):
            """ checks to see if a file is a shortcut or symlink (OS-sensitive) """
            if sys.platform in ['Windows',  'win32']:
                if str(f)[-4:] == '.lnk':
                    return True
                else:
                    return False
            else:
                if os.path.islink(os.path.join(root, f)):
                    return True
                else:
                    return False

        # the actual walk process and the main observations made at each step
        for root, dirs, files in scandir(norm_location,  topdown=True,  onerror=None,  followlinks=False):
            this_node = Node()
            root_head_tail = os.path.split(root)
            node_id_counter += 1
            this_node.node_id = str(node_id_counter)
            this_node.name_length = len(root_head_tail[1])

            if root in default_locations:
                this_node.default = True
            #TO DO: check to see if it is the desktop, if so, mark the folder (will require appro. folder property)

            this_node.letters = sum(char.isalpha() for char in root_head_tail[1])
            this_node.numbers = sum(char.isdigit() for char in root_head_tail[1])

            this_node.white_spaces = sum(char.isspace() for char in root_head_tail[1])
            this_node.special_chars = sum(not char.isdigit() and not char.isalpha() and not char.isspace() for char in root_head_tail[1])

            if root_head_tail[1] in temp_foldername_set:
                this_node.name_duplicate = True
            else:
                temp_foldername_set.add(root_head_tail[1])

            try:
                root_stat_info = os.stat(root)
                this_node.m_time = datetime.datetime.fromtimestamp(root_stat_info.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                this_node.c_time = datetime.datetime.fromtimestamp(root_stat_info.st_ctime).strftime("%Y-%m-%d %H:%M:%S")

                if root_stat_info.st_nlink > 1:
                    this_node.hard_link_duplicate = True
            except:
                this_node.m_time = -2
                this_node.c_time = -2

            original_dirs = len(dirs)
            # Removes folders to be ignored from walk
            for ignore in ignores:
                norm_ignore = str(ignore)
                dirs[:] = [d for d in dirs if not ((os.path.join(root, d) in norm_ignore) and (norm_ignore in os.path.join(root, d)))]

            ignored_children = (original_dirs - len(dirs))
            dirs[:] = [d for d in dirs if os.access(os.path.join(root, d), os.W_OK)]

            inaccessible_children = (original_dirs - (len(dirs) + ignored_children))
            dirs[:] = [d for d in dirs if not d[0] == '.']

            this_node.hidden_children = (original_dirs - (len(dirs) + ignored_children + inaccessible_children))
            dirs[:] = [d for d in dirs if not (os.path.islink(os.path.join(root, d)))]

            # store number of dirs that are actually symlinks
            this_node.symlinks = (original_dirs - (len(dirs) + ignored_children + inaccessible_children + this_node.hidden_children))

            for d in dirs:
                dirs_analyzed += 1
                # print("Scanning directory #{}: {}".format(dirs_analyzed, os.path.join(root, d)))
                this_node.path_children.append(os.path.join(root, d))

            for f in files:
                files_analyzed += 1
                # print("Scanning file #{}: {}".format(files_analyzed, os.path.join(root, f)))

                if is_symlink_file(root, f):
                    # increment node.symlinks for each 'file' symlink found (counted in the same variable as folder symlinks)
                    this_node.symlinks += 1
                elif is_hidden_file(root, f):
                    this_node.hidden_files += 1
                else:
                    this_file = File()
                    file_id_counter += 1
                    this_file.file_id = file_id_counter
                    this_file.full_name_length = len(str(f))

                    try: #sometimes statinfo is not available
                        statinfo = os.stat(os.path.join(root, f))
                    except:
                        statinfo = False

                    if statinfo:
                        if statinfo.st_nlink > 1:
                            this_file.hard_link_duplicate = True

                        try: #sometimes even when statinfo is available, particular stats are missing
                            this_file.a_time = datetime.datetime.fromtimestamp(statinfo.st_atime).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            this_file.a_time = -2
                        try:
                            this_file.m_time = datetime.datetime.fromtimestamp(statinfo.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            this_file.m_time = -2
                        try:
                            this_file.c_time = datetime.datetime.fromtimestamp(statinfo.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
                        except:
                            this_file.c_time = -2

                        this_file.file_size = statinfo.st_size
                        if this_file.file_size == 0:
                            try:
                                this_file.file_size = os.path.getsize(os.path.join(root, f))
                            except:
                                this_file.file_size = -2
                    
                    else:
                        this_file.a_time = -2
                        this_file.m_time = -2
                        this_file.c_time = -2
                        this_file.file_size = -2

                    if str(f) in temp_filename_set:
                        this_file.name_duplicate = True
                    else:
                        temp_filename_set.add(str(f))

                    if '.' in f:
                        split_name = f.rsplit('.', 1)
                        this_file.extension = split_name[1]
                        this_file.letters = sum(c.isalpha() for c in split_name[0])
                        this_file.numbers = sum(c.isdigit() for c in split_name[0])
                        this_file.white_spaces = sum(c.isspace() for c in split_name[0])
                        this_file.special_chars = sum(not c.isdigit() and not c.isalpha() and not c.isspace() for c in split_name[0])
                    else:
                        this_file.letters = sum(c.isalpha() for c in f)
                        this_file.numbers = sum(c.isdigit() for c in f)
                        this_file.white_spaces = sum(c.isspace() for c in f)
                        this_file.special_chars = sum(not c.isdigit() and not c.isalpha() and not c.isspace() for c in f)
                    this_node.file_list.append(this_file)

            # this is done so that paths need not be permanently stored, but node relationships can be recorded
            for temp_id, temp_node in list(temp_nodes.items()):
                if (len(temp_node.path_children) < 1):
                    the_nodes[temp_id] = temp_node
                    del temp_nodes[temp_id]
                else:
                    for path_child in temp_node.path_children:
                        if ((root in path_child) and (path_child in root)):
                            temp_node.children.append(str(this_node.node_id))
                            temp_node.path_children.remove(path_child)

            if len(this_node.path_children) > 0:
                temp_nodes[this_node.node_id] = this_node
            else:
                the_nodes[this_node.node_id] = this_node

        while len(temp_nodes) > 0:
            for temp_id, temp_node in list(temp_nodes.items()):
                while len(temp_node.path_children) > 0:
                    for path_child in temp_node.path_children:
                        temp_node.unknown_children += 1
                        temp_node.path_children.remove(path_child)
                the_nodes[temp_id] = temp_node
                del temp_nodes[temp_id]

        node_lists.append(the_nodes)

        add_depths("1", 0)  # call the earlier defined function, starting from the top
    runtime = datetime.datetime.now() - startTime
    print("Walking runtime: {}".format(runtime))
    return node_lists
