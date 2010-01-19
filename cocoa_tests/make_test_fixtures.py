#!/usr/bin/env python

import sys, os.path
sys.path.append(os.path.realpath(".."))
os.environ['DJANGO_SETTINGS_MODULE'] = __name__

import datetime

from django_plist.templatetags.django_plist_tags import RenderPlistObjectNode


def make_dict_plist():
    d = {
        'str': 'a string',
        'unicode': u'a unicode string',
        'integer': 42,
        'false': False,
        'true': True,
        'datetime': datetime.datetime.now(),
        'date': datetime.date.today(),
    }
    
    node = RenderPlistObjectNode('obj')
    fout = open('test_dict.plist', 'w')
    fout.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    fout.write('<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">')
    fout.write('<plist version="1.0">')
    fout.write(node.render({'obj': d}))
    fout.write('</plist>')

if __name__ == '__main__':
    make_dict_plist()