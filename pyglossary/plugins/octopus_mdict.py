# -*- coding: utf-8 -*-
## octopus_mdic.py
## Read Octopus MDict dictionary format, mdx(dictionary)/mdd(data)
##
## Copyright (C) 2013 Xiaoqiang Wang <xiaoqiangwang AT gmail DOT com>
##
## This program is a free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, version 3 of the License.
##
## You can get a copy of GNU General Public License along this program
## But you can always get it from http://www.gnu.org/licenses/gpl.txt
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
## GNU General Public License for more details.

from formats_common import *

import os
from os.path import splitext, isfile, isdir, extsep, basename, dirname

enable = True
format = 'OctopusMdict'
description = 'Octopus MDict'
extentions = ['.mdx']
readOptions = [
    'resPath',## str, directory path
    'encoding',## str
    'substyle',## bool
]
writeOptions = []

class Reader(object):
    def __init__(self, glos):
        self._glos = glos
        self.clear()
    def clear(self):
        self._filename = ''
        self._encoding = ''
        self._substyle = True
        self._mdx = None
        self._mdd = None
        self._mddFilename = ''
        self._dataDir = ''
    def open(self, filename, **options):
        from pyglossary.plugin_lib.readmdict import MDX, MDD
        self._filename = filename
        self._encoding = options.get('encoding', '')
        self._substyle = options.get('substyle', True)
        self._mdx = MDX(filename, self._encoding, self._substyle)
        ###
        filenameNoExt, ext = splitext(self._filename)
        self._dataDir = options.get('resPath', filenameNoExt + '_files')
        mddFilename = ''.join([filenameNoExt, extsep, 'mdd'])
        if isfile(mddFilename):
            self._mdd = MDD(mddFilename)
            self._mddFilename = mddFilename
        ###
        log.pretty(self._mdx.header, 'mdx.header=')
        #for key, value in self._mdx.header.items():
        #    key = key.lower()
        #    self._glos.setInfo(key, value)
        try:
            title = self._mdx.header[b'Title']
        except KeyError:
            pass
        else:
            self._glos.setInfo('title', title)
        self._glos.setInfo('description', self._mdx.header.get(b'Description', ''))
        ###
        try:
            self.writeDataFiles()
        except:
            log.exception('error while saving MDict data files')

    def writeDataFiles(self):
        if not self._mdd:
            return
        if not isdir(self._dataDir):
            os.makedirs(self._dataDir)
        for key, value in self._mdd.items():
            fpath = ''.join([self._dataDir, key.decode('utf-8').replace('\\', os.path.sep)]);
            if not isdir(dirname(fpath)):
                os.makedirs(dirname(fpath))
            log.debug('saving MDict data file: %s'%fpath)
            f = open(fpath, 'wb')
            f.write(value)
            f.close()

    def __iter__(self):
        for word, defi in self._mdx.items():
            word = toStr(word)
            defi = toStr(defi)
            yield Entry(word, defi)

    __len__ = lambda self: len(self._mdx)

    def close(self):
        self.clear()


