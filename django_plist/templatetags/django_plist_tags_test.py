#!/usr/bin/env python
# encoding: utf-8

from datetime import date, datetime, time
from django.db import models
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
    

# TODO implement remaining fields

#decimal = models.DecimalField(blank=True,null=True)
#file = models.FileField(blank=True,null=True)
#filepath = models.FilePathField(blank=True,null=True)
#image = models.ImageField(blank=True,null=True)
#nullboolean = models.NullBooleanField(blank=True,null=True)
#xml = models.XMLField(blank=True,null=True)
    
NONE_FIELD = '<key>id</key><string>None</string>'

def test_time_model_field():
    class TimeModel(models.Model):
        time = models.TimeField()
    obj = TimeModel(time=time(15,05,45))
    exp = '<dict>%s<key>time</key><date>15:05:45</date></dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_date_model_field():
    class DateModel(models.Model):
        date = models.DateField()
    obj = DateModel(date=date(2009,10,22))
    exp = '<dict><key>date</key><date>2009-10-22</date>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_datetime_model_field():
    class DateTimeModel(models.Model):
        datetime = models.DateTimeField()
    obj = DateTimeModel(datetime=datetime(2009,10,22,15,5,45))
    exp = '<dict>%s<key>datetime</key><date>2009-10-22T15:05:45</date></dict>'  % NONE_FIELD
    eq_(render_object(obj), exp)

def test_ipaddress_model_field():
    class IPAddressModel(models.Model):
        ip = models.IPAddressField()
    obj = IPAddressModel(ip='127.0.0.1')
    exp = '<dict><key>ip</key><string>127.0.0.1</string>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_text_model_field():
    class TextModel(models.Model):
        text = models.TextField()
    obj = TextModel(text='some text')
    exp = '<dict><key>text</key><string>some text</string>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_cvs_model_field():
    class CVSModel(models.Model):
        cvs = models.CommaSeparatedIntegerField()
    obj = CVSModel(cvs='a,b,c')
    exp = '<dict>%s<key>cvs</key><string>a,b,c</string></dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_integer_model_field():
    class IntegerModel(models.Model):
        integer = models.IntegerField()
    obj = IntegerModel(integer=42)
    exp = '<dict><key>integer</key><integer>42</integer>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_slug_model_field():
    class SlugModel(models.Model):
        slug = models.SlugField()
    obj = SlugModel(slug='my-slug')
    exp = '<dict>%s<key>slug</key><string>my-slug</string></dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_url_model_field():
    class URLModel(models.Model):
        url = models.URLField()
    obj = URLModel(url='http://example.com/')
    exp = '<dict><key>url</key><string>http://example.com/</string>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_email_model_field():
    class EmailModel(models.Model):
        email = models.EmailField()
    obj = EmailModel(email='example@example.com')
    exp = '<dict>%s<key>email</key><string>example@example.com</string></dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_boolean_model_field():
    class BooleanModel(models.Model):
        boolean = models.BooleanField()
    obj = BooleanModel(boolean=True)
    exp = '<dict><key>boolean</key><true/>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

def test_char_model_field():
    class CharModel(models.Model):
        char = models.CharField()
    obj = CharModel(char='a few characters')
    exp = '<dict><key>char</key><string>a few characters</string>%s</dict>' % NONE_FIELD
    eq_(render_object(obj), exp)

# utility functions used by tests below

def render_object(obj):
    node = RenderPlistObjectNode('obj')
    return node.render({'obj': obj})