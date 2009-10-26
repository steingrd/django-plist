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




## Running tests ##

The tests written for django-plist are intended to be run with `nosetests`.

To run the tests (with `nosetests` installed on your system):

    $ export DJANGO_SETTINGS_MODULE=test_settings
    $ nosetests
	----------------------------------------------------------------------
	Ran 20 tests in 0.213s
	
	OK
	
