#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tap-lever',
      version='0.3.1',
      description='Singer.io tap for extracting data from the Lever API',
      author='Fishtown Analytics',
      url='http://fishtownanalytics.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_lever'],
      install_requires=[
          'tap-framework==0.0.5',
      ],
      entry_points='''
          [console_scripts]
          tap-lever=tap_lever:main
      ''',
      packages=find_packages(),
      package_data={
          'tap_lever': [
              'schemas/*.json'
          ]
      })
