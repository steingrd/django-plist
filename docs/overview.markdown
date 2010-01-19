# django-plist #

django-plist is a Django application that trivializes the serialization of
Django model objects into the XML format used by Property List files on the
Cocoa platform (iPhone/Mac OS X).

django-plist behaves somewhat different than the serialization framework that
comes bundled with Django. django-plist employs the standard Django stack
(generic views, default templates and template tags) and is a regular Django
application in every aspect.

## About this document ##

This document is written in the Markdown format and contains some inline HTML.
This document is also available online at
[http://github.com/steingrd/django-plist/blob/master/docs/overview.markdown][overview].

  [overview]: http://github.com/steingrd/django-plist/blob/master/docs/overview.markdown

## Installing django-plist ##

Please refer to [`INSTALL.markdown`][install] for installation instructions.
Notice the last section on configuring Django and ensure that you have the
correct settings in `INSTALLED_APPS` and `TEMPLATE_LOADER`.

  [install]: http://github.com/steingrd/django-plist/blob/master/INSTALL.markdown

## Using django-plist ##

django-plist is a serialization application for Django models; its only task
is to transform your Django model objects into the XML format used by Property
Files for easier consumption on the Cocoa platform. 

Using django-plist generally means returning XML from some URL endpoint.

This means that you'll have to decide *where* your clients find their
serialized objects and *what* goes into a serialized object, i.e. which
fields should be serialized and in what form.

django-plist provides two methods for serializing model objects into
property list xml:

1. generic views &mdash; the generic views in `django_plist.views.generic`
will probably cover most of your needs.

2. shortcut functions &mdash; if for example additional processing needs to be
done before the result is returned to the client, shortcut functions can be
used to render the result, akin to extending the generic views.

We'll take a look at both of these methods after we've seen exactly how a
model object is serialized.

## Serializing model objects ##

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
      <date>2009-07-06T10:23:00Z</date>
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
    <tr><td>str, unicode, CharField, TextField, SlugField, URLField, TimeField</td><td>&lt;string&gt;</td></tr>
    <tr><td>date, datetime, DateField, DateTimeField</td><td>&lt;date&gt;</td></tr>
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

## Generic views ##

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

### `django_plist.views.generic.plist_array` ###

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

### `django_plist.views.generic.plist_dict` ###

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


## Shortcut functions ##

django-plist comes with two shortcut functions for rendering a arrays and
dict's. 

 * `render_array(iterable, as_plist=None)` &mdash; this function takes an
   iterable object, for example a list, a tuple or a QuerySet and renders the
   object as a property list array.

   The optional keyword argument `as_plist` takes a callable that accepts a
   single object from the iterable. The callable should return a dict, just
   like the `as_plist` method in Model classes. Use this keyword argument to
   pass a callable that customizes serialization without altering the Model
   class.

 * `render_dict(dictionary)` &mdash; this function takes a dictionary object
   and renders the dict as a property list dict.