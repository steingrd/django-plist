#!/usr/bin/env python
# encoding: utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext

def render_array(iterable, context_instance=None):
    if not context_instance:
        context = RequestContext({'array': iterable})
    else:
        context['array'] = iterable
    return render_to_response('django_plist/array.plist', 
        context_instance=context)
    
def render_dictionary(dictionary, context_instance=None):
    if not context_instance:
        context = RequestContext({'dictionary': dictionary})
    else:
        context['dictionary'] = dictionary
    return render_to_response('django_plist/dictionary.plist', 
        context_instance=context)
