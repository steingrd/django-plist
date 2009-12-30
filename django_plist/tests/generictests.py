
from django.test import TestCase
from django.conf import settings 
from django.core.management import call_command 
from django.db.models.loading import load_app

from testapp.models import Author

class TestAppModelsTestCase(TestCase):
    """
    Base class for tests using testapp.models. setUp registers this as an 
    app and invokes syncdb to create test tables. Once someone solves #7835,
    remove this class.
    
    """
    def setUp(self):
        self.old_installed_apps = settings.INSTALLED_APPS 
        settings.INSTALLED_APPS += ('django_plist.tests.testapp',)
        settings.DEBUG = True
        load_app('django_plist.tests.testapp')
        call_command('syncdb', verbosity=0, interactive=False)
        
    def tearDown(self):
        settings.INSTALLED_APPS = self.old_installed_apps
        

class ArrayGenericView(TestAppModelsTestCase):
    
    urls = 'django_plist.tests.testurls'
    fixtures = ('authors.json',)
    
    def test_empty_queryset_with_allow_empty_renders_empty_array(self):
        response = self.client.get('/blogs_allowempty/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, '<array></array>')

    def test_empty_queryset_on_default_view_returns_404(self):
        response = self.client.get('/blogs_noempty/')
        self.assertEquals(404, response.status_code)
    
    def test_queryset_with_objects_renders_objects(self):
        self.assertEquals(2, Author.objects.all().count())
        response = self.client.get('/authors_allowempty/')
        self.assertEquals(200, response.status_code)
        self.assertContains(response, '<key>email</key><string>bob@example.com</string>')
        self.assertContains(response, '<key>email</key><string>bill@example.com</string>')
        

