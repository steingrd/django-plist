#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

django_plist_packages = [
    'django_plist',
    'django_plist.views',
    'django_plist.templatetags',
]

setup(name='django-plist',
      version='0.1',
      author='Steingrim Dovland',
      author_email='steingrd@ifi.uio.no',
      url='http://steingrd.github.com/django-plist/',
      packages=django_plist_packages,
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: Python'])
