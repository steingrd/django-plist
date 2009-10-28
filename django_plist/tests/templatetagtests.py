
from django.test import TestCase

from django_plist.templatetags.django_plist_tags import RenderPlistObjectNode

def render_object(obj):
    """ 
    Utility function used for testing RenderPlistObjectNode
    """
    node = RenderPlistObjectNode('obj')
    return node.render({'obj': obj})


class TemplateNodeRenderTest(TestCase):
    
    def test_int_render_as_integer(self):
        expected = u'<integer>42</integer>'
        fragment = render_object(42)
        self.assertEquals(expected, fragment)
        
    def test_long_render_as_integer(self):
        expected = u'<integer>42</integer>'
        fragment = render_object(42L)
        self.assertEquals(expected, fragment)

    def test_float_render_as_real(self):
        expected = u'<real>42.0</real>'
        fragment = render_object(42.0)
        self.assertEquals(expected, fragment)

    def test_string_render_as_string(self):
        expected = u'<string>this is a string</string>'
        fragment = render_object('this is a string')
        self.assertEquals(expected, fragment)

    def test_tuple_render_as_array(self):
        expected = u'<array><integer>1</integer><integer>2</integer></array>'
        fragment = render_object((1,2))
        self.assertEquals(expected, fragment)
        
    def test_list_render_as_array(self):
        # only tests one entry to avoid test failures due to random order
        expected = u'<array><integer>1</integer><integer>2</integer></array>'
        fragment = render_object([1,2])
        self.assertEquals(expected, fragment)

    def test_dict_render_as_dict(self):
        expected = u'<dict><key>one</key><integer>1</integer></dict>'
        fragment = render_object(dict(one=1))
        self.assertEquals(expected, fragment)

    def test_booleans_render_as_true_and_false(self):
        self.assertEquals('<true/>', render_object(True))
        self.assertEquals('<false/>', render_object(False))
