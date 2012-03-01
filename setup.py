#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name='django-less-styleguide',
      version='0.0.1',
      url='https://github.com/a-musing-moose/django-less-styleguide',
      author="Jonathan Moss",
      author_email="jonathan.moss@tangentone.com.au",
      description="A Style Guide Generator for LESS files",
      long_description=open('README.rst').read(),
      keywords="LESS, CSS, Style Guide",
      license='BSD',
      platforms=['linux'],
      packages=find_packages(),
      install_requires=[],
      # See http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Unix',
                   'Programming Language :: Python']
      )
