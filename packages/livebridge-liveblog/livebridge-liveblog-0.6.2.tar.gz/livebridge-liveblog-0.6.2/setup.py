# -*- coding: utf-8 -*-
#
# Copyright 2016, 2018 dpa-infocom GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from setuptools import setup, find_packages

version = '0.6.2'

setup(name='livebridge-liveblog',
      version=version,
      description="Liveblog plugin for Livebridge.",
      long_description="""\
Allows to use Sourcefabric Liveblog as source or target (experimental) for Livebridge.\
See https://github.com/dpa-newslab/livebridge-liveblog for more infos.
""",
      classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Communications",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Other Audience",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Environment :: Plugins",
        ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords=['liveticker','scribblelive','syndication','realtime'],
      author='dpa-infocom GmbH',
      maintainer='Martin Borho',
      maintainer_email='martin@borho.net',
      url='https://github.com/dpa-newslab/livebridge-scribblelive',
      license='Apache Software License (http://www.apache.org/licenses/LICENSE-2.0)',
      packages=find_packages(exclude=['tests', 'htmlcov']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "livebridge>=0.26.0"
      ])
