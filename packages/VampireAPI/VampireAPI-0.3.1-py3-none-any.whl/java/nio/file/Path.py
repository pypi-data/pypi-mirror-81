# SPDX-FileCopyrightText: 2020 - Sebastian Ritter <bastie@users.noreply.github.com>
# SPDX-License-Identifier: Apache-2.0

'''
Created on 01.09.2020

@author: Sͬeͥbͭaͭsͤtͬian
'''
from builtins import str
from java.io.File import File
from java.lang.Object import Object


class Path(Object):
    '''
    classdocs
    '''

    def __init__(self, first: str, *more):
        '''
        Constructor
        '''
        self.path_as_string = first
        for nextParam in more:
            self.path_as_string += File.separator + nextParam

    def toString(self) -> str:
        return self.path_as_string
