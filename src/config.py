#!/usr/bin/env python
# coding:utf-8
"""
A collection of different settings and options used by the client
ToDo: Find better way to store public_key
"""

__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@mail.mcgill.ca"
__status__ = "Beta"


DEFAULT_FOLDERS = {"linux": {"Desktop", "Downloads"},
                   "mac": {"Desktop", "Documents", "Downloads", "Movies",
                           "Music", "Pictures", "Public", "Sites"},
                   "win": {"Contacts", "Desktop", "Documents", "Downloads",
                           "Favorites", "Links", "Music", "Pictures",
                           "Saved Games", "Searches", "Videos"}}


CONSENT_FILE_DIR = 'consent_form.txt'

SUMMARY_FILE_DIR = 'summary_file.txt'

CONSENT_TEXT = "Welcome! You are invited to participate in a study that aims to understand how people manage information on their computers. \
You will be asked to enter some basic information, answer two brief questionnaires, and select locations on your hard drive to be included in data collection. \
This collects basic data about your files and folders, such as how many files are in each folder and how full your hard drive is -- \
file contents are not viewed, file and folder names are not recorded, and you will see the results before choosing to submit them. \
No identifying data is collected. The whole process typically takes about ten minutes, and no there are no known associated risks. \
You may refuse to answer any question or withdraw from the study at any time by exiting the software. \
Your computer must be connected to the internet to proceed.\n\n This study is conducted by Jesse David Dinneen (jesse.dinneen@mail.mcgill.ca), \
a PhD candidate supervised by Prof. Charles-Antoine Julien (charles.julien@mcgill.ca) in the School of Information Studies at McGill University, \
and is approved by McGill University Research Ethics Board (#75-0715, 'Understanding file management behavior'). If you have any questions or \
concerns regarding your rights or welfare as a participant in this research study, please contact the McGill Ethics Manager \
at 514-398-6831 or lynda.mcneil@mcgill.ca"

# '''
public_key = "\
-----BEGIN PUBLIC KEY-----\n\
#public key goes here\n\
-----END PUBLIC KEY-----"
# '''
