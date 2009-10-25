#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext

def render_array(iterable):
    context = {'array': iterable}
    return render_to_response('django_plist/array.plist', context)
    
def render_dictionary(dictionary):
    context = {'dictionary': dictionary}
    return render_to_response('django_plist/dictionary.plist', context)
