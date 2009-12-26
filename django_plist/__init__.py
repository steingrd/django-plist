#!/usr/bin/env python
# encoding: utf-8

from itertools import imap
from django.shortcuts import render_to_response
from django.template import RequestContext

def render_array(iterable, as_plist=None):
    if as_plist is not None:
        iterable = imap(as_plist, iterable)
    context = {'array': iterable}
    return render_to_response('django_plist/array.plist', context)
    
def render_dictionary(dictionary):
    if dictionary is None:
        dictionary = {}
    context = {'dictionary': dictionary}
    return render_to_response('django_plist/dictionary.plist', context)
