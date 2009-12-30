#!/usr/bin/env python
# encoding: utf-8

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template import RequestContext, loader


def plist_array(request, queryset, context_processors=None, allow_empty=None):
    queryset = queryset._clone()
    if not allow_empty and len(queryset) == 0:
        raise Http404
    
    context = { 'array': queryset }
    request_context = RequestContext(request, context, context_processors)
            
    template = loader.get_template('django_plist/array.plist')
    return HttpResponse(template.render(request_context))
    
    
def plist_dict(request, queryset, context_processors=None, object_id=None, slug=None, slug_field=None):
    if object_id:
        queryset = queryset.filter(pk=object_id)
    elif slug and slug_field:
        queryset = queryset.filter(**{slug_field: slug})
    else:
        raise AttributeError,"Generic view must be called with either an object_id or a slug/slug_field."
        
    try:
        obj = queryset.get()
    except ObjectDoesNotExist:
        raise Http404, "No %s found matching the query" % (queryset.model._meta.verbose_name)
        
    context = { 'dictionary': obj }
    request_context = RequestContext(request, context, context_processors)
    template = loader.get_template('django_plist/dictionary.plist')
    return HttpResponse(template.render(request_context))