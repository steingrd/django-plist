
from django.conf.urls.defaults import *

from testapp.models import Author, Blog

urlpatterns = patterns('',
    (r'^blogs_noempty/$', 'django_plist.views.generic.plist_array', 
        {'queryset': Blog.objects.all(), 'allow_empty': False}),
        
    (r'^blogs_allowempty/$', 'django_plist.views.generic.plist_array', 
        {'queryset': Blog.objects.all(), 'allow_empty': True}),
        
    (r'^authors_allowempty/$', 'django_plist.views.generic.plist_array',  
        {'queryset': Author.objects.all(), 'allow_empty': True}),
)

