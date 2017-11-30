#!/usr/bin/env python
# coding:utf-8
"""
Definitions of classes used by the client to store the data from walk.py and
calculate the summary in review.py
"""

__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@vuw.ac.nz"
__status__ = "Beta"


class File:
    """ Stores data about files analyzed """

    def __init__(self):
        self.a_time = -1
        self.c_time = -1
        self.extension = ""
        self.file_id = 0
        self.file_size = -1
        self.full_name_length = -1
        self.hard_link_duplicate = False
        self.letters = -1
        self.m_time = -1
        self.name_duplicate = False
        self.numbers = -1
        self.special_chars = -1
        self.white_spaces = -1


class Drive:
    """ Stores data about drives analyzed """

    def __init__(self):
        self.disk_code = ""
        self.free = -1
        self.size = -1
        self.used = -1


class Node:
    """ Stores data about nodes (folders) analyzed """

    def __init__(self):
        self.c_time = -1
        self.children = []
        self.default = False
        self.depth = -1
        self.file_list = []
        self.hard_link_duplicate = False
        self.hidden_children = -1
        self.hidden_files = 0
        self.letters = -1
        self.m_time = -1
        self.name_duplicate = False
        self.name_length = -1
        self.name_length = -1
        self.node_id = 0
        self.numbers = -1
        self.path_children = []
        self.special_chars = -1
        self.symlinks = -1
        self.unknown_children = 0
        self.white_spaces = -1


class Results:
    """
    Stores the aggregated final data to be analyzed in
    review.py and then transmitted to the researchers.
    """

    def __init__(self):
        self.cloud_services = {}
        self.computer_description = {}
        self.demographics = {}
        self.drives = []
        self.installed_file_managers = {}
        self.node_lists = []
        self.operating_system = ""
        self.personality_results = {}
        self.sod_results = {}
        self.time_stamps = {}
