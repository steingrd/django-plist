# Installing django-plist #

In order to use django-plist you'll need a functional installation of Django
1.0 or later.

There are several ways to install django-plist: using a package management tool
such as `easy_install` or `pip`, or manually installing a Python package from a
source code tarball or a Github checkout.

After the Python package has been installed you'll need to configure your
Django project to use django-plist.

## About this document ##

This document is written in the Markdown format and contains some inline HTML.
This document is also available online at
[http://github.com/steingrd/django-plist/blob/master/INSTALL.markdown][install].

  [install]: http://github.com/steingrd/django-plist/blob/master/INSTALL.markdown

## Installing with `easy_install` ##

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

## Installing from source code ##

If you prefer to manually install packages or to use `distutils` from the
command line you can download the latest stable version of django-plist from
[http://pypi.python.org/pypi/django-plist][pypy2].

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

  [pypy2]: http://pypi.python.org/pypi/django-plist

## Configuring Django ##

To use django-plist with its default settings you'll need to do the following:

* Add `django_plist` (note the underscore) to the `INSTALLED_APPS` setting of
   your Django project.

* If you installed django-plist using easy_install or installed it as an
  "egg", you'll need to add a template loader that enables loading files from
  a Python egg:

         TEMPLATE_LOADERS = (
             ...
             'django.template.loaders.eggs.load_template_source',
         )

* If you installed django-plist from source or you used pip, you'll need to
  add a template loader that enables loading files from a application
  directory:

         TEMPLATE_LOADERS = (
             ...
             'django.template.loaders.app_directories.load_template_source',
         )
