#!/usr/bin/env python
# encoding: utf-8

from nose.tools import eq_

from django_plist_tags import RenderPlistObjectNode

def test_integer():
    expected = u'<integer>42</integer>'
    eq_(render_object(42), expected)
        
def test_float():
    expected = u'<real>42.0</real>'
    eq_(render_object(42.0), expected)
    
def test_string():
    expected = u'<string>this is a string</string>'
    eq_(render_object('this is a string'), expected)
    
def test_array():
    expected = u'<array><integer>1</integer><integer>2</integer></array>'
    eq_(render_object([1,2]), expected)
    eq_(render_object((1,2)), expected)
    
def test_dictionary():
    # only tests one entry to avoid test failures due to random order
    expected = u'<dict><key>one</key><integer>1</integer></dict>'
    eq_(render_object({'one': 1}), expected)
    
def test_booleans():
    eq_(render_object(True), u'<true/>')
    eq_(render_object(False), u'<false/>')
    
def test_simple_object():
    class MyClass(object):
        def __init__(self, a):
            self.a = a
        def as_plist(self):
            return {'covar': self.a }
            
    obj = MyClass(17)
    exp = '<dict><key>covar</key><integer>17</integer></dict>'
    eq_(render_object(obj), exp)
    
def test_recursive_objects():
    class Parent(object):
        def __init__(self):
            self.children = list()
        def as_plist(self):
            return self.children
            
    class Child(object):
        def __init__(self, value):
            self.value = value
        def as_plist(self):
            return self.value
            
    obj = Parent()
    obj.children.append(Child(99))
    obj.children.append(Child('zot'))
    
    exp = '<array><integer>99</integer><string>zot</string></array>'
    eq_(render_object(obj), exp)
    
# TODO test Model instances, default and as_plist override
    
# utility functions used by tests below

def render_object(obj):
    node = RenderPlistObjectNode('obj')
    return node.render({'obj': obj})