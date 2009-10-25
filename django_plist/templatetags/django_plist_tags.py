#!/usr/bin/env python
# encoding: utf-8

from datetime import date, datetime, time

from django import template
from django.db.models import Model
from django.db.models.query import QuerySet

register = template.Library()

@register.tag(name='render_plist_object')
def do_render_plist_object(parser, token):
    try:
        tag_name, plist_object = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, \
            "render_plist_object requires a single argument"
    return RenderPlistObjectNode(plist_object)
    
class RenderPlistObjectNode(template.Node):
    
    def __init__(self, plist_object_name):
        self.plist_object_name = template.Variable(plist_object_name)
        
    def render(self, context):
        plist_object = self.plist_object_name.resolve(context)
        return self._render_unknown_object(plist_object)
        
    def _render_unknown_object(self, obj):
        # TODO perhaps replace this with something more concise, e.g. a dict
        if obj is None:
            return self._render_string('None')
        elif isinstance(obj, basestring): # FIXME force unicode?
            return self._render_string(obj)
        elif isinstance(obj, bool):
            return self._render_boolean(obj)
        elif isinstance(obj, int):
            return self._render_integer(obj)
        elif isinstance(obj, float):
            return self._render_real(obj)
        elif isinstance(obj, dict):
            return self._render_dictionary(obj)
        elif isinstance(obj, (list, tuple, QuerySet)):
            return self._render_array(obj)
        elif isinstance(obj, (date, datetime, time)):
            return self._render_date(obj)
        else:
            if hasattr(obj, 'as_plist'):
                return self._render_unknown_object(obj.as_plist())
            elif Model in obj.__class__.__bases__:
                return self._render_dictionary(obj.__dict__)
            else:
                # FIXME figure out something better to do than returning this string
                return 'FAILED TO RENDER'            
        
    def _render_boolean(self, obj):
        if obj: 
            return u'<true/>'
        else:
            return u'<false/>'
        
    def _render_date(self, obj):
        return u'<date>%s</date>' % obj.isoformat()

    def _render_string(self, obj):
        return u'<string>%s</string>' % obj
        
    def _render_integer(self, obj):
        return u'<integer>%s</integer>' % obj
        
    def _render_real(self, obj):
        return u'<real>%s</real>' % obj
        
    def _render_array(self, obj):
        xml = u'<array>'
        for elm in obj:
            xml += self._render_unknown_object(elm)
        xml += u'</array>'
        return xml
        
    def _render_dictionary(self, obj):
        xml = u'<dict>'
        for key, val in obj.items():
            xml += u'<key>%s</key>' % key
            xml += self._render_unknown_object(val)
        xml += u'</dict>'
        return xml