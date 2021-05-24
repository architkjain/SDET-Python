import os
import re
from importlib import import_module
from datetime import datetime, timedelta
import time
from framework import Paths
import shutil
import logging
import csv
import framework
from framework import suite
import os


class PyUtils:
    @staticmethod
    def getmodulename(modpath):
        return os.path.splitext(os.path.basename(modpath))[0]

    @staticmethod
    def import_class(cl):
        d = cl.rfind(".")
        classname = cl[d + 1:len(cl)]
        m = __import__(cl[0:d], globals(), locals(), [classname])
        return getattr(m, classname)

    @staticmethod
    def has_attribute(strmodulepath, attributetocheck):
        mod = import_module(strmodulepath)
        # mod = import_module("tests.v" + Config.get_value('App.Version').replace('.', '_') +
        #                     '.' + testcase['groupname'])
        for attrib_in_module in dir(mod):
            if '__' in attrib_in_module:
                pass
            elif hasattr(eval('mod.' + attrib_in_module), attributetocheck):
                return True

    @staticmethod
    def get_group_init(modpath):
        mod = import_module(modpath)
        groupinitfunc = None

        for attrib_in_module in dir(mod):
            if '__' in attrib_in_module:
                pass
            elif hasattr(eval('mod.' + attrib_in_module), 'decorator'):
                functochk = eval('mod.' + attrib_in_module)
                if functochk.__dict__['decorator'].__name__ == 'groupInit':
                    groupinitfunc = functochk
        return groupinitfunc

    @staticmethod
    def get_group_cleanup(modpath):
        mod = import_module(modpath)
        groupcleanupfunc = None

        for attrib_in_module in dir(mod):
            if '__' in attrib_in_module:
                pass
            elif hasattr(eval('mod.' + attrib_in_module), 'decorator'):
                functochk = eval('mod.' + attrib_in_module)
                if functochk.__dict__['decorator'].__name__ == 'groupCleanup':
                    groupcleanupfunc = functochk
        return groupcleanupfunc


class LogUtils:
    log_dir_path = None
    logs_backup_dir_path = None

    @staticmethod
    def backup_logs():
        LogUtils.log_dir_path = Paths.logs_dir
        LogUtils.logs_backup_dir_path = Paths.logs_backup_dir

        files_to_backup = []

        for root, directories, files in os.walk(LogUtils.log_dir_path):
            for filename in files:
                source_file = os.path.join(root, filename)
                destination_file = os.path.join(LogUtils.logs_backup_dir_path, filename)
                file_dict = {'source': source_file, 'destination': destination_file}
                files_to_backup.append(file_dict)

        if not os.path.isdir(LogUtils.logs_backup_dir_path):
            os.mkdir(LogUtils.logs_backup_dir_path)

        for fl in files_to_backup:
            shutil.move(fl['source'], fl['destination'])
