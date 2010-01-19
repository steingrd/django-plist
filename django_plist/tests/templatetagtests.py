
from datetime import date, datetime, time

from django.db import models
from django.test import TestCase

from django_plist.templatetags.django_plist_tags import RenderPlistObjectNode, \
    PropertyListSerializationFailedError


# TODO implement remaining fields
#
#decimal = models.DecimalField()
#file = models.FileField()
#filepath = models.FilePathField()
#image = models.ImageField()
#nullboolean = models.NullBooleanField()
#xml = models.XMLField()


NONE_FIELD = '<key>id</key><string>None</string>'


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
        
    def test_string_contents_is_xml_escaped(self):
        expected = u'<string>&lt; &amp; &gt;</string>'
        fragment = render_object('< & >')
        self.assertEquals(expected, fragment)
        
    def test_dict_key_names_is_xml_escaped(self):
        expected = u'<dict><key>&lt;&gt;</key><integer>1</integer></dict>'
        fragment = render_object({'<>': 1})
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

    def test_non_model_without_as_plist_method_raises_exception(self):
        class MyClass(object):
            pass
        func = lambda: render_object(MyClass())
        self.assertRaises(PropertyListSerializationFailedError, func)

    def test_object_with_as_plist_method(self):
        class MyClass(object):
            def __init__(self, a):
                self.a = a
            def as_plist(self):
                return {'covar': self.a }
        
        expected = '<dict><key>covar</key><integer>17</integer></dict>'
        fragment = render_object(MyClass(17))
        self.assertEquals(expected, fragment)

    def test_time_model_field(self):
        class TimeModel(models.Model):
            time = models.TimeField()
        expected = '<dict>%s<key>time</key><string>15:05:45</string></dict>' % NONE_FIELD
        fragment = render_object(TimeModel(time=time(15,05,45)))
        self.assertEquals(expected, fragment)

    def test_date_model_field(self):
        class DateModel(models.Model):
            date = models.DateField()
        fragment = render_object(DateModel(date=date(2009,10,22)))
        expected = '<dict><key>date</key><date>2009-10-22T00:00:00Z</date>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_datetime_model_field(self):
        class DateTimeModel(models.Model):
            datetime = models.DateTimeField()
        fragment = render_object(DateTimeModel(datetime=datetime(2009,10,22,15,5,45)))
        expected = '<dict>%s<key>datetime</key><date>2009-10-22T15:05:45Z</date></dict>'  % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_datetime_does_not_render_fractions_of_seconds(self):
        now = datetime.now()
        fragment = render_object(now)
        expected = '<date>%s</date>' % now.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.assertEquals(expected, fragment)

    def test_ipaddress_model_field(self):
        class IPAddressModel(models.Model):
            ip = models.IPAddressField()
        fragment = render_object(IPAddressModel(ip='127.0.0.1'))
        expected = '<dict><key>ip</key><string>127.0.0.1</string>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_text_model_field(self):
        class TextModel(models.Model):
            text = models.TextField()
        fragment = render_object(TextModel(text='some text'))
        expected = '<dict><key>text</key><string>some text</string>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_cvs_model_field(self):
        class CVSModel(models.Model):
            cvs = models.CommaSeparatedIntegerField()
        fragment = render_object(CVSModel(cvs='a,b,c'))
        expected = '<dict>%s<key>cvs</key><string>a,b,c</string></dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_integer_model_field(self):
        class IntegerModel(models.Model):
            integer = models.IntegerField()
        fragment = render_object(IntegerModel(integer=42))
        expected = '<dict><key>integer</key><integer>42</integer>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_slug_model_field(self):
        class SlugModel(models.Model):
            slug = models.SlugField()
        fragment = render_object(SlugModel(slug='my-slug'))
        expected = '<dict>%s<key>slug</key><string>my-slug</string></dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_url_model_field(self):
        class URLModel(models.Model):
            url = models.URLField()
        fragment = render_object(URLModel(url='http://example.com/'))
        expected = '<dict><key>url</key><string>http://example.com/</string>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_email_model_field(self):
        class EmailModel(models.Model):
            email = models.EmailField()
        fragment = render_object(EmailModel(email='example@example.com'))
        expected = '<dict>%s<key>email</key><string>example@example.com</string></dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_boolean_model_field(self):
        class BooleanModel(models.Model):
            boolean = models.BooleanField()
        fragment = render_object(BooleanModel(boolean=True))
        expected = '<dict><key>boolean</key><true/>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

    def test_char_model_field(self):
        class CharModel(models.Model):
            char = models.CharField()
        fragment = render_object(CharModel(char='a few characters'))
        expected = '<dict><key>char</key><string>a few characters</string>%s</dict>' % NONE_FIELD
        self.assertEquals(expected, fragment)

