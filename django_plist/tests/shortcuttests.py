
from django.test import TestCase

from django_plist import render_array, render_dictionary

class RenderArrayTest(TestCase):
    
    def test_empty_iterable_renders_empty_array(self):
        response = render_array([])
        self.assertContains(response, '<array></array>')
        
    def test_none_object_renders_empty_array(self):
        response = render_array(None)
        self.assertContains(response, '<array></array>')
        
    def test_iterable_renders_objects_as_array(self):
        response = render_array([1,2,3])
        self.assertContains(response, '<array><integer>1</integer><integer>2</integer><integer>3</integer></array>')
        
    def test_as_plist_kwarg_is_invoked_on_iterable_objects(self):
        def to_int(binary):
            return int(binary, 2)
        response = render_array(['1', '10', '11'], as_plist=to_int)
        self.assertContains(response, '<array><integer>1</integer><integer>2</integer><integer>3</integer></array>')
        
        
class RenderDictionaryTest(TestCase):
    
    def test_empty_dict_renders_empty_dict(self):
        response = render_dictionary({})
        self.assertContains(response, '<dict></dict>')
        
    def test_none_object_renders_empty_dict(self):
        response = render_dictionary(None)
        self.assertContains(response, '<dict></dict>')
        
    def test_dict_renders_as_dict(self):
        response = render_dictionary({'foo': 42})
        self.assertContains(response, '<dict><key>foo</key><integer>42</integer></dict>')
        
