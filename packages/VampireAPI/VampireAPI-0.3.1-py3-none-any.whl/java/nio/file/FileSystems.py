# SPDX-FileCopyrightText: 2020 - Sebastian Ritter <bastie@users.noreply.github.com>
# SPDX-License-Identifier: Apache-2.0

'''
Created on 01.09.2020

@author: Sͬeͥbͭaͭsͤtͬian
'''
from builtins import staticmethod
from java.nio.file.FileSystem import FileSystem
from java.lang.Object import Object
from java.nio.file.FileSystem import __vampire_DefaulFileSystem__


class FileSystems(Object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    @staticmethod
    def getDefault() -> FileSystem:
        return __vampire_DefaulFileSystem__()
