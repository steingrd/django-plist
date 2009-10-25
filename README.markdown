# django-plist #

django-plist is a Django application that trivializes the serialization of
Django model objects into the XML format used by Property List files on the
Cocoa platform (iPhone/Mac OS X).

django-plist behaves somewhat different than the serialization framework that
comes bundled with Django. django-plist employs the standard Django stack
(generic views, default templates and template tags) and is a regular Django
application in every aspect.

  [plmanp]: http://developer.apple.com/documentation/Darwin/Reference/ManPages/man5/plist.5.html
  [plguide]: http://developer.apple.com/documentation/Cocoa/Conceptual/PropertyLists/Introduction/Introduction.html
  [plwiki]: http://en.wikipedia.org/wiki/Property_list
  [pldtd]: http://www.apple.com/DTDs/PropertyList-1.0.dtd
  [pldate]: http://en.wikipedia.org/wiki/ISO_8601

## About this document ##

This document is written in the Markdown format and contains some inline HTML.
This document is also available online at
[http://steingrd.github.com/django-plist/][ghpage].

## Installing django-plist ##

In order to use django-plist you'll need a functional installation of Django
1.0 or later.

There are several ways to install django-plist: using a package management tool
such as `easy_install` or `pip`, or manually installing a Python package from a
source code tarball or a Github checkout.

After the Python package has been installed you'll need to configure your
Django project to use django-plist.

### Installing with `easy_install` ###

The easiest way to install django-plist is to use a Python package management
tool such as [`easy_install`][easy] or [`pip`][pip]. If you are not familiar
with such tools, now might be a good time to get started using them. 

Once one of these tools are up and running you should be able to install
django-plist by executing a single command.

For `easy_install`:

    $ easy_install django-plist

Or if you prefer `pip`:

    $ pip install django-plist

  [easy]: http://peak.telecommunity.com/DevCenter/EasyInstall
  [pip]: http://pypi.python.org/pypi/pip/

### Installing from source code ###

If you prefer to manually install packages or to use `distutils` from the
command line you can download the latest stable version of django-plist from
[http://steingrd.github.com/django-plist/][ghpage].

Extract the downloaded file, inside the directory named
`django-plist` you'll find a directory named `django_plist`. Either move (or
symlink) this directory to somewhere on you Python path, or execute the
`setup.py` script by running:

    $ python setup.py install

Keep in mind that this command installs the package at a system-wide location
and probably needs elevated privileges.

If you have Git installed on your computer, a complete copy of the
django-plist repository can be checked out from Github by typing:

    $ git clone git://github.com/steingrd/django-plist.git

The instructions for installing from a source code tarball applies to a Git
checkout as well.

  [ghpage]: http://steingrd.github.com/django-plist/

### Configuring Django ###

To use django-plist with its default settings you'll need to do the following:

1. Add `django_plist` (note the underscore) to the `INSTALLED_APPS` setting of
   your Django project.

2. The generic views and the shortcut functions make use of templates that are
   bundled with the `django_plist` application. Make sure that the
   `app_directories` template loader is enabled in `settings.py`:


        TEMPLATE_LOADERS = (
            ...
            'django.template.loaders.app_directories.load_template_source',
        )

## Using django-plist ##

django-plist is a serialization application for Django models; its only task
is to transform your Django model objects into the XML format used by Property
Files for easier consumption on the Cocoa platform. 

Using django-plist generally means returning XML from some URL endpoint.

This means that you'll have to decide *where* your clients find their
serialized objects and *what* goes into a serialized object, i.e. which
fields should be serialized and in what form.

django-plist provides three methods for serializing model objects into
property list xml:

1. generic views -- the generic views in `django_plist.views.generic` will
probably cover most of your needs.

2. shortcut functions -- if for example additional processing needs to be done
before the result is returned to the client, shortcut functions can be used to
render the result, akin to extending the generic views.

3. template tags -- the generic views and the templates make use of template
tags to execute the serialization process.

We'll take a look at each of these methods after we've seen exactly how a
model object is serialized.

### Serializing model objects ###

In the examples below we use the standard example of a blog entry. We will
show several examples of how to serialize `Entry` instances into property list
xml. The `Entry` class used is overly simplified:

    class Entry(models.Model):
        title = models.CharField()
        body = models.TextField()
        published = models.DateTimeField()

Instances of this simple model class can be serialized into property list xml
without any adjustments. Instances are serialized as `<dict>` elements by
default:

    <dict>
      <key>id</key>
      <integer>1</integer>
      <key>title</key>
      <string>My Blog Post</string>
      <key>body</key>
      <string>Shortest blog post evah?</string>
      <key>published</key>
      <date>2009-07-06T10:23Z</date>
    </dict>

Each field is represented as a key-value pair, the key is the name of the
field and the following value is a element determined by the field type.
Notice that the implicit primary key is serialized as well.

The default type mapping used by django-plist is given in the following table.
`int`s are serialized into `<integer>` elements, the string types into
`<string>` elements and so on. Notice that Python dictionaries are serialized
as `<dict>` elements and that lists, tuples and querysets are serialized as
`<array>` elements.

<table>
  <thead>
    <tr>
	  <th>Python type</th>
	  <th>Property list type</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>int, IntegerField</td><td>&lt;integer&gt;</td></tr>
    <tr><td>float, FloatField</td><td>&lt;real&gt;</td></tr>
    <tr><td>list, tuple, QuerySet</td><td>&lt;array&gt;</td></tr>
    <tr><td>dict, django.db.Model instances</td><td>&lt;dict&gt;</td></tr>
    <tr><td>bool, BooleanField</td><td>&lt;true&gt;, &lt;false&gt;</td></tr>
    <tr><td>str, unicode, CharField, TextField, SlugField, URLField,</td><td>&lt;string&gt;</td></tr>
    <tr><td>date, datetime, DateField, DateTimeField, TimeField</td><td>&lt;date&gt;</td></tr>
  </tbody>
</table>

By default every field, including the implicit primary key, is serialized. If
you want to omit certain fields or perhaps give them different names or a
different serialized type, you can override this behavior by defining a method
name `as_plist()` in your model class:

	class Entry(models.Model):
	    ...
        def as_plist(self):
            return { 'entry.title': self.title, 'entry.body': self.body }

In the example above, only the title and the body ends up being serialized and
the key names have been slightly modified. The result is this property list
dictionary:

    <dict>
      <key>entry.title</key>
      <string>My Blog Post</string>
      <key>entry.body</key>
      <string>Shortest blog post evah?</string>
    </dict>

### Generic views ###

The easiest and perhaps most common way to use django-plist is to use the
generic views in `django_plist.views.generic`. There's a generic view for
returning an array of objects, for example a QuerySet or a list of objects and
a generic view for returning a singel object based on an object identifier.

Using the generic views is akin to using the Django generic views; configure
the views with a dictionary or extend them by defining your own view and pass
the values to the generic view.

    from django_plist.views.generic import plist_array, plist_dict

    entry_list_info = { 'queryset': Blog.entry.all() }

    urls = urlpatterns('',
        url('^blog/$', plist_array, entry_list_info),
		url('^blog/(?P<object_id>\d+)', plist_array, entry_list_info)
    )

The resulting XML contains the necessary `DOCTYPE` declarations and property
list version elements.

#### `django_plist.views.generic.plist_array` ####

Renders an array of objects, i.e. all the objects in a `QuerySet`.

Required arguments:

* `queryset`: A `QuerySet` that contains the objects.

Optional arguments:

* `allow_empty`: A boolean specifying whether to display the page if no
  objects are available. If this is False and no objects are available, the
  view will raise a 404 instead of displaying an empty page. By default, this
  is True.

* `context_processors`: A list of template-context processors to apply to the
  view's template.

#### `django_plist.views.generic.plist_dict` ####

Renders a single object, either determined by its primary key or a slug.
Returns Http404 if no object is found.

Required arguments:

* `queryset`: A `QuerySet` that contains the object.

* Either `object_id` or (`slug` and `slug_field`) is required.

  If you provide `object_id`, it should be the value of the primary-key field
  for the object being displayed on this page.

  Otherwise, `slug` should be the slug of the given object, and `slug_field`
  should be the name of the slug field in the `QuerySet`'s model. By default,
  `slug_field` is 'slug'.

Optional arguments:

* `context_processors`: A list of template-context processors to apply to the
  view's template.

### Template tags ###

The generic views make use of templates that are bundled with the
`django_plist` Python package. These templates invoke a single template tag to
perform the actual serialization. You can use this template tag in your own
templates by loading the `django_plist_tags` tag library and invoking
`render_plist_object` on any object type. The type mappings mentioned above
apply. Note that the template tag only outputs XML elements for the given
object, not XML and DTD declarations.

    {% load django_plist_tags %}
    ...
    {% render_plist_object object %}

### Shortcut functions ###

django-plist comes with two shortcut functions for rendering a arrays and
dict's. 

 * `render_array(iterable)` &mdash; this function takes an iterable object,
   for example a list, a tuple or a QuerySet and renders the object as a
   property list array.

 * `render_dict(dictionary)` &mdash; this function takes a dictionary object
   and renders the dict as a property list dict.

## Running tests ##

The tests written for django-plist are intended to be run with `nosetests`.

To run the tests (with `nosetests` installed on your system):

    $ export DJANGO_SETTINGS_MODULE=test_settings
    $ nosetests
	----------------------------------------------------------------------
	Ran 20 tests in 0.213s
	
	OK
	
