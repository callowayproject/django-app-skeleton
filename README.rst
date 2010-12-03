==========================================
Generating a Packagable Django Application
==========================================

The ``create_app.py`` uses several variables to replace within a "template" directory. The default template directory is included and called "skel".

Running the script
==================

The script requires that ``virtualenv`` and ``virtualenvwrapper`` are installed on your system.

The script is interactive, although you can specify some options when you call it. Calling the script is as easy as::

	python create_app.py

and the script will ask you for everything it needs. 

.. parsed-literal::

	**Application name:** django-coolapp
	**Package name [coolapp]:** 
	**Author [jcooluser]:** Johnny Cooluser
	**Destination directory [/home/jcooluser/app-skel]:** ..
	**Application template directory [/home/jcooluser/app-skel/skel]:**
	**Virtual environment name [django-coolapp]:** coolapp

You can specify some or all of the options when calling the script.

Command-line Options
********************

-a, --author
	The name of the author.

-n, --name
	The name of the application, like 'django-coolapp'.

-p, --package
	The name of the installed package, like 'coolapp'.

-v, --virtenv
	The name of the virtualenv to create.

-d, --dest
	Where to put the new application. Relative paths are recognized.

-t, --template
	The application template to use as a basis for the new application. Relative paths are recognized.


Variable Substitution
=====================

The script creates several substitution variables that it uses to substitute for file names and within text files.


APP_NAME
	The name supplied by ``-n``\ , ``--name``\ , or the answer to *Application name*.

PKG_NAME
	The name supplied by ``-p``\ , ``--package``\ , or the answer to *Package name*. The default is the ``APP_NAME`` without ``django-``\ .

AUTHOR
	The value supplied by ``-a``\ , ``--author``\ , or the answer to *Author*. The default is the current user name.

SECRET_KEY
	A randomly generated string of characters used in the ``settings.py`` file.

VIRTENV
	The name supplied by ``-v``\ , ``--virtenv``\ , or the answer to *Virtual environment name*. The default is the ``APP_NAME``\ .

The variables are referenced by surrounding them with ``$$$$``\ , such as ``$$$$APP_NAME$$$$``\ . Here is an example from the setup.py file::

	setup(
	    name = "$$$$APP_NAME$$$$",
	    version = __import__('$$$$PKG_NAME$$$$').get_version().replace(' ', '-'),
	    url = '',
	    author = '$$$$AUTHOR$$$$',

Contributors
============

Eric Florenzano
Corey Oordt
Jose Soares
Justin Quick
Adam Patterson