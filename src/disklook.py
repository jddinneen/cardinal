#!/usr/bin/env python
# coding:utf-8
"""
Collects data about any visible disks
"""

from classes import Drive
import sys
import subprocess
import ctypes
if sys.platform in ('Windows',  'win32', 'cygwin', 'nt'):
    import win32api

__author__ = "Jesse David Dinneen"
__copyright__ = "Copyright 2015, JDD"
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Jesse David Dinneen"
__email__ = "jesse.dinneen@mail.mcgill.ca"
__status__ = "Beta"


def windows_disk_look(dir):
    """ Function just for windows (called below if needed). """
    total_bytes = ctypes.c_ulonglong(0)
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dir), None, ctypes.pointer(total_bytes), ctypes.pointer(free_bytes))
    a = total_bytes.value / 1024 / 1024  # MEGABYTES FORMAT
    b = free_bytes.value / 1024 / 1024
    retlist = [a, b]
    return retlist


def get_hardware_data():
    """
    Collects hardware data about the different drives to be analyzed.
    Different methods for Linux, Windows and Mac OS used.
    """
    drives = []
    if sys.platform in ('Windows',  'win32', 'cygwin', 'nt'):  # windows approach
        drive_list = win32api.GetLogicalDriveStrings()
        drive_list = drive_list.split('\000')[:-1]
        for founddrive in drive_list:
            this_drive = Drive()
            drive_info = windows_disk_look(founddrive)
            this_drive.disk_code = founddrive
            this_drive.size = drive_info[0]  # EACH OF THESE STORED IN MEGABYTES
            this_drive.free = drive_info[1]
            this_drive.used = drive_info[0] - drive_info[1]
            drives.append(this_drive)

    elif sys.platform in ('linux',  'linux2', 'linux3', 'darwin'):  # POSIX approach
        system_drive_string = ""
        df = subprocess.Popen(["df", "-H"], stdout=subprocess.PIPE)  # use df to get disk info
        df_results = df.communicate()[0].decode("utf-8")
        df_results = df_results.replace(',', '.')
        df_array = df_results.splitlines()

        if sys.platform in ('linux',  'linux2',  'linux3'):
            system_drive_string = "/dev/sd"  # linux disk prefix
        elif sys.platform in 'darwin':
            system_drive_string = "/dev/disk"  # mac disk prefix

        for line in df_array:
            if system_drive_string in line:
                this_drive = Drive()
                values = line.split(" ")
                newvalues = []

                for v in values:
                    if (len(v) > 0):
                        newvalues.append(v)

                this_drive.disk_code = newvalues[0]
                rawsizestring = newvalues[1]
                rawusedstring = newvalues[2]
                rawfreestring = newvalues[3]

                if len(rawsizestring) > 1:
                    sizefloat = float(rawsizestring[:-1])
                    if ('T' in rawsizestring) or ('t' in rawsizestring):  # EACH OF THESE STORED IN MEGABYTES
                        this_drive.size = sizefloat * 1024 * 1024
                    elif ('G' in rawsizestring) or ('g' in rawsizestring):
                        this_drive.size = sizefloat * 1024
                    elif ('M' in rawsizestring) or ('m' in rawsizestring):
                        this_drive.size = sizefloat
                    elif ('K' in rawsizestring) or ('k' in rawsizestring):
                        this_drive.size = sizefloat / 1024
                    else:
                        this_drive.size = -2
                else:
                    if rawsizestring == "0":
                        this_drive.size = 0
                    else:
                        this_drive.size = -2
                
                if len(rawusedstring) > 1:
                    usedfloat = float(rawusedstring[:-1])
                    if ('T' in rawusedstring) or ('t' in rawusedstring):
                        this_drive.used = usedfloat * 1024 * 1024
                    elif ('G' in rawusedstring) or ('g' in rawusedstring):
                        this_drive.used = usedfloat * 1024
                    elif ('M' in rawusedstring) or ('m' in rawusedstring):
                        this_drive.used = usedfloat
                    elif ('K' in rawusedstring) or ('k' in rawusedstring):
                        this_drive.used = usedfloat / 1024
                    else:
                        this_drive.used = -2
                else:
                    if rawusedstring == "0":
                        this_drive.used = 0
                    else:
                        this_drive.used = -2
                
                if len(rawfreestring) > 1:
                    freefloat = float(rawfreestring[:-1])
                    if ('T' in rawfreestring) or ('t' in rawfreestring):
                        this_drive.free = freefloat * 1024 * 1024
                    elif ('G' in rawfreestring) or ('g' in rawfreestring):
                        this_drive.free = freefloat * 1024
                    elif ('M' in rawfreestring) or ('m' in rawfreestring):
                        this_drive.free = freefloat
                    elif ('K' in rawfreestring) or ('k' in rawfreestring):
                        this_drive.free = freefloat / 1024
                    else:
                        this_drive.free = -2
                else:
                    if rawfreestring == "0":
                        this_drive.free = 0
                    else:
                        this_drive.free = -2
                
                drives.append(this_drive)

    return drives
