#!/usr/bin/python

from setuptools import setup

setup( name='ciscomapper',
  version='0.1',
  description='Draw the scheme of your cisco network. All you need is telnet access and cdp enabled',
  maintainer_email='sergey.zelyukin@gmail.com',
  keywords='cisco cdp network browser',
  license='Apache License, Version 2.0',
  install_requires = [
    'ciscotelnet>=0.1.1 @ git+ssh://git@github.com/sergeyzelyukin/cisco-telnet.git@master',
  ],
  classifiers=[
  'Programming Language :: Python',
  'Programming Language :: Python :: 2',
  'Programming Language :: Python :: 2.7',
  'Topic :: System :: Networking',
  'Topic :: Software Development :: Libraries',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: Apache Software License',
  'Development Status :: 4 - Beta'],
  py_modules=['ciscomapper'])
