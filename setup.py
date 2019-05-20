#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This module is part of the opsi PackageBuilder
see: https://forum.opsi.org/viewforum.php?f=22

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = 'Holger Pandel'
__copyright__ = "Copyright 2013-2017, Holger Pandel"
__license__ = "MIT"
__maintainer__ = "Holger Pandel"
__email__ = "holger.pandel@googlemail.com"
__status__ = "Production"


#import ez_setup
#ez_setup.use_setuptools()

import os
import platform

from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

if platform.system() == "Windows":
    data=[('oPB/core/x86', ['oPB/core/x86/MapDrive.dll']),
                ('oPB/core/x64', ['oPB/core/x64/MapDrive.dll']),
                ('oPB/help', ['oPB/help/opsiPackageBuilder.qch']),
                ('oPB/help', ['oPB/help/opsipackagebuilder.qhc'])]
else:
    data=[('oPB/help', ['oPB/help/opsiPackageBuilder.qch']),
                ('oPB/help', ['oPB/help/opsipackagebuilder.qhc'])]

setup(name="opsiPackageBuilder",
      version="8.4.2",
      description="opsi PackageBuilder - software distribution packaging tool",
      author="Holger Pandel",
      author_email="holger.pandel@googlemail.com",
      url="https://forum.opsi.org/viewforum.php?f=22",
      packages=find_packages(exclude=['tests*', 'ez_setup.py']),
      scripts=["opsipackagebuilder.py"],
      long_description="""opsiPackageBuilder""",
      license="MIT",
      platforms=["Windows", "Linux"],
      package_data={
          # Include any *.ui files found in the 'oPB.ui' package, too:
          'oPB.ui': ['*.ui', '*.qss'],
      },
      data_files=data,
      install_requires=["pyqt5>=5.6",
                        "spur",
                        "pycryptodome"
                        ],
    entry_points={
          'gui_scripts': [
              'opsipackagebuilder = oPB.runner:Main',
              'opb-helpviewer = oPB.runner:HelpViewerMain'
          ]
    },
)
