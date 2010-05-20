#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

django_plist_packages = [
    'django_plist',
    'django_plist.views',
    'django_plist.templatetags',
    'django_plist.tests',
    'django_plist.tests.testapp'
]

django_plist_templates = [
    'templates/django_plist/array.plist',
    'templates/django_plist/dictionary.plist',
    'tests/testapp/fixtures/authors.json'
]

long_description = """
============
django-plist
============

django-plist is a Django application that trivializes the serialization of
Django model objects into the XML format used by Property List files on the
Cocoa platform (iPhone/Mac OS X).

Installing
==========
Please refer to `INSTALL.markdown` for installation instructions. Notice the
last section on configuring Django and ensure that you have the correct
settings in `INSTALLED_APPS` and `TEMPLATE_LOADER`. 

Using
=====
Usage instructions can be found in `docs/overview.markdown` which is also
available online. """ + "\n\n" + open('CHANGELOG.txt').read()

setup(name='django-plist',
      version='0.6',
      author='Steingrim Dovland',
      author_email='steingrd@ifi.uio.no',
      url='http://wiki.github.com/steingrd/django-plist',
      description='Django app for serializing objects into Cocoa Property List XML',
      long_description=long_description,
      packages=django_plist_packages,
      package_data={'django_plist': django_plist_templates},
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python'])
