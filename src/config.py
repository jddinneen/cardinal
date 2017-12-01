#!/usr/bin/env python
# coding:utf-8
"""
A collection of different settings and options used by the client
"""

__author__ = "Jesse David Dinneen, Fabian Odoni"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@vuw.ac.nz"
__status__ = "Beta"


DEFAULT_FOLDERS = {"linux": {"Desktop", "Downloads"},
                   "mac": {"Desktop", "Documents", "Downloads", "Library", "Movies",
                           "Music", "Pictures", "Public", "Sites"},
                   "win": {"Contacts", "Desktop", "Documents", "Downloads",
                           "Favorites", "Links", "Music", "Pictures",
                           "Saved Games", "Searches", "Videos"}}


CONSENT_FILE_DIR = 'consent_form.txt'

SUMMARY_FILE_DIR = 'summary_file.txt'

# insert your consent form text, contact info, research ethics information, etc here
# don't forget to also update the welcomeLabel text in wizardUI file to match.
CONSENT_TEXT = "Lorem ipsum -- populate with consent form, contact information, research ethics approval, etc."

# '''
public_key = "\
-----BEGIN PUBLIC KEY-----\n\
#your public key goes here for encrypting collected data\n\
-----END PUBLIC KEY-----"
# '''
