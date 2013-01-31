===================
Django App Skeleton
===================

:Version: 1.0.1
:Docs: http://github.com/callowayproject/django-app-skeleton/
:Download: http://pypi.python.org/pypi/django-app-skeleton/
:Source: http://github.com/callowayproject/django-app-skeleton/

==========
Change Log
==========
* **1.0.1**
    * Updated example app so the code is more up to date with django

* **1.0**
    * Default configuration file `.djas`
    * Virtualenv creation is now optional
        * Added command-line argument for using virtualenv
    * `create_app` was renamed to `create_pkg`
    * App skeleton is compatible with django's `startapp` command
    * Bunch of code tweaks, should be easier to read and debug

See all the changes: https://github.com/callowayproject/django-app-skeleton/pull/6

==========================================
Generating a Packagable Django Application
==========================================

The ``create_pkg.py`` uses several variables to replace within a "template"
directory. The default template directory is included and called "skel".

Running the script
==================

First, clone this repo or use `pip` to install the package::

    $ pip install django-app-skeleton


The script is interactive, although you can specify some options when you
call it. Calling the script is as easy as::

	python create_pkg.py

and the script will ask you for everything it needs.

.. parsed-literal::

    **Package Name:** django-coolapp
    **App Name [coolapp]:**
    **Author [johnnycool]:** Johnny Cool
    **Author Email [johnnycool@example.com]:**
    **Destination DIR [/path/to/package/destination]:**
    **Template DIR [/path/to/package/template]:**
    **Use Virtualenv [n]:** y
    **Virtualenv Name [coolapp]:**

You can specify some or all of the options when calling the script.

Command-line Options
********************

Below are the possible commands to supplied the `create_pkg.py` script. If any
of the values are present, no prompt will be displayed for its value.

-a, --author
	The name of the author.

-e, --email
    The email of the author

-p, --package
	The name of the installed package, like 'django-coolapp'.

-n, --name
	The name of the application, like 'coolapp'.

-i, --use-venv
    Wheater or not to create a virtualenv

-v, --virtenv
	The name of the virtualenv to create. Only relative if `--use-venv` is `y`

-d, --dest
	Where to put the new package. Relative paths are recognized.

-t, --template
	The package template to use as a basis for the new application. Relative paths are recognized.


Default Command options
=======================

When the script is first run prompted you for the values or if they are supplied
via the command-line arguments, some of the values are set as defaults.

A configuration filed located at `~/.djas` is created. Below is an example
configuration.

.. parsed-literal::

    [main]
    author = Johnny Cool
    author_email = johnnycool@example.com
    destination_dir = /path/to/package/destination
    template_dir = /path/to/package/template
    use_venv = n


Using just the app skeleton
===========================

If all you want is the `app` skeleton, you can use the following command::

    $ django-admin.py startapp --template=/path/to/django-app-skeleton/skel/app_name

.. note::

    Our `skeleton` is a **package** skeletion, and django's
    `startapp` command expects a **app** skeletion. Therefore the path above
    points to just out **app** skeleton.


Variable Substitution
=====================

The script creates several substitution variables that it uses to substitute
for file names and within text files. If you want to create a custom package
template, below are the possible variables supplied to each file in the
skeleton.


`app_name`
	The name supplied by ``-n``\ , ``--name``\ , or the answer to *Application name*.

`pkg_name`
	The name supplied by ``-p``\ , ``--package``\ , or the answer to *Package name*. The default is the ``APP_NAME`` without ``django-``\ .

`pkg_author`
	The value supplied by ``-a``\ , ``--author``\ , or the answer to *Author*. The default is the current user name.

`pkg_author_email`
    The value supplied by ``-e``\, ``--author_email``\, or the answer to *Author Email*.

`secret_key`
	A randomly generated string of characters used in the ``settings.py`` file.

`venv`
	The name supplied by ``-v``\ , ``--virtenv``\ , or the answer to *Virtual environment name*. The default is the ``APP_NAME``\ .

The variables are referenced by surrounding them with ``{{``\ , such as
``{{app_name}}``\ . Here is an example from the setup.py file::

	setup(
	    name = "{{app_name}}",
	    version = __import__('{{pkg_name}}').get_version().replace(' ', '-'),
	    url = '',
	    author = '{{pkg_author}}',

.. note::

    Previously `$$$$` was used, this was changed to be `{{` in order for the
    template, i.e. `/skel/app_name` to be usable with
    `django-admin.py startapp --template=...`, see below.

    In addition to `{{ .. }}`, anything with the name folder name `app_name` is
    also replaced with its correct value. This is also so make the **app**
    skeleton compatible with django's `startapp` command.


Contributors
============

* Eric Florenzano
* Corey Oordt
* Jose Soares
* Justin Quick
* Adam Patterson
