from formats_common import *

enable = False
format = 'Unknown'
description = 'Unknown'
extentions = []
readOptions = []
writeOptions = []
supportsAlternates = False

import sys, os
from os.path import (
    join,
    split,
    splitext,
    isfile,
    isdir,
    exists,
)

import logging

log = logging.getLogger('root')

from paths import rootDir
sys.path.insert(0, rootDir)

from pyglossary import core
from pyglossary.file_utils import FileLineWrapper
from pyglossary.text_utils import toStr, toBytes
from pyglossary.os_utils import indir
from pyglossary.entry import Entry


