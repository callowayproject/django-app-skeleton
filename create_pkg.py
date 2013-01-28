#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import random
import sys
import subprocess


CONFIG_FILE = os.path.expanduser('~/.djas')
CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
BLACKLIST = (
    'jquery',
    '.tar.gz',
    'admin/css',
    'admin/img',
    'admin/js',
    '/.git/',
    '.svn',
    '.hg',
)


def write_config(config):
    """Writes the config to a file"""
    with open(CONFIG_FILE, 'wb') as conf:
        config.write(conf)


def get_config_value(config, sec, opt, default):
    """Get a config value.

    If the value was not found, write out the default value to the config.

    """
    try:
        return config.get(sec, opt)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        # Ensure the config has the `main` section
        if not config.has_section('main'):
            config.add_section('main')
        config.set(sec, opt, default)
        write_config(config)
        return default


def set_config_value(sec, opt, value):
    """Set a config value.

    Only sets the value if the value is not founc of empty.

    """
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)

    if not config.has_option(sec, opt):
        config.set(sec, opt, value)
    elif config.get(sec, opt) == '':
        config.set(sec, opt, value)
    write_config(config)


def get_config():
    """Gets the configuration file, creates one if it does not exist"""

    defaults = (
        ('author', 'PKG_AUTHOR', ''),
        ('author_email', 'PKG_AUTHOR_EMAIL', ''),
        ('destintation_dir', 'DEST_DIR',  os.getcwd()),
        ('template_dir', 'TMPL_DIR', os.path.abspath(
            os.path.join(os.path.dirname(__file__), 'skel'))),
        ('use_venv', 'USE_VENV', 'n'),
    )

    config = ConfigParser.RawConfigParser()

    if not config.read(CONFIG_FILE):
        config.add_section('main')
        for default in defaults:
            key, var, value = default
            config.set('main', key, value)
        write_config(config)

    return dict([
        (default[1], get_config_value(
            config, 'main', default[0], default[2])) for default in defaults])


def ensure_venv():
    """Ensure virtualenv and virtuelenv wrapper is installed"""
    has_venv = bool(subprocess.Popen(
        ['which', 'virtualenv'],
        stdout=subprocess.PIPE).communicate()[0])

    if not has_venv:
        print 'virtualenv is required to run this script. Please install it ' \
              'with\n  easy_install virtualenv\n\nor\n\n  pip virtualenv'
        sys.exit(1)

    has_venv_wrapper = bool(subprocess.Popen(
        ['which', 'virtualenvwrapper.sh'],
        stdout=subprocess.PIPE).communicate()[0])

    if not has_venv_wrapper:
        print 'virtualenvwrapper is required to run this script. Please' \
              'install it with\n  easy_install virtualenvwrapper\n\nor\n\n' \
              'pip virtualenvwrapper'
        sys.exit(1)


def mk_virtual_env(name, dest):
    """Creates a virtualenv using virtualenv wrapper"""
    print 'Making the virtual environment (%s)...' % name
    create_env_cmds = [
        'source virtualenvwrapper.sh',
        'cd %s' % dest,
        'mkvirtualenv --no-site-packages --distribute %s' % name,
        'easy_install pip'
    ]
    create_pa_cmd = [
        'source virtualenvwrapper.sh',
        'cat > $WORKON_HOME/%s/bin/postactivate'\
        '<<END\n#!/bin/bash/\ncd %s\nEND\n'\
        'chmod +x $WORKON_HOME/%s/bin/postactivate' % (name,
                                                       dest,
                                                       name)
    ]
    subprocess.call([';'.join(create_env_cmds)], env=os.environ,
                    executable='/bin/bash', shell=True)
    subprocess.call([';'.join(create_pa_cmd)], env=os.environ,
                    executable='/bin/bash', shell=True)

    print 'Virtualenv created, type workon %s' % name


def replace(opts, text):
    """Replace certain strings will the supplied text

    `opts` is a dictionary of variables that will be replaced. Similar to
    django, it will look for {{..}} and replace it with the variable value

    Since we want to maintance compatibility with django's `startapp` command
    we need to also replaced `app_name` folders with the supplied value.

    """
    text = text.replace('/app_name', '/{0}'.format(opts['APP_NAME']))
    text = text.replace('/gitignore', '/.gitignore')

    for key, value in opts.iteritems():
        if not value:
            continue
        text = text.replace('{{%s}}' % (key.lower(),), value)
    return text


def mk_pkg(opts, dest, templ_dir):
    """Creates the package file/folder structure"""
    try:
        os.makedirs(dest)
    except OSError:
        pass

    for root, dirs, files in os.walk(templ_dir):
        for filename in files:
            source_fn = os.path.join(root, filename)

            dest_fn = replace(opts, os.path.join(
                dest, root.replace(templ_dir, ''), replace(opts, filename)))

            try:
                os.makedirs(os.path.dirname(dest_fn))
            except OSError:
                pass

            print 'Copying %s to %s' % (source_fn, dest_fn)
            should_replace = True
            for bl_item in BLACKLIST:
                if bl_item in dest_fn:
                    should_replace = False
            data = open(source_fn, 'r').read()
            if should_replace:
                data = replace(opts, data)
            open(dest_fn, 'w').write(data)
            os.chmod(dest_fn, os.stat(source_fn)[0])
    print 'Package created'


def main(options):
    config = get_config()
    cur_user = os.getlogin()
    # Default options
    opts = {
        'APP_NAME': None,
        'PKG_NAME': None,
        'PKG_AUTHOR': None,
        'PKG_AUTHOR_EMAIL': None,
        'PKG_URL': None,
        'VENV': None,
        'SECRET_KEY': ''.join([random.choice(CHARS) for i in xrange(50)]),
        'DEST_DIR': None,
        'TMPL_DIR': None,
        'USE_VENV': None
    }

    # Update the default options wiht the config values
    opts.update(config)

    def prompt(attr, text, default=None):
        """Prompt the user for certain values"""
        if hasattr(options, attr):
            if getattr(options, attr):
                return getattr(options, attr)

        default_text = default and ' [%s]: ' % default or ': '
        new_val = None
        while not new_val:
            new_val = raw_input(text + default_text) or default
        return new_val

    # Package/App Information
    opts['PKG_NAME'] = prompt('pkg_name', 'Package Name')
    opts['APP_NAME'] = prompt(
        'app_name', 'App Name', opts['PKG_NAME'].replace('django-', ''))
    opts['PKG_URL'] = prompt('pkg_url', 'Project URL')

    # Author Information
    opts['PKG_AUTHOR'] = prompt(
        'pkg_author', 'Author Name', opts['PKG_AUTHOR'] or cur_user)
    opts['PKG_AUTHOR_EMAIL'] = prompt(
        'pkg_author_email', 'Author Email', opts['PKG_AUTHOR_EMAIL'])

    set_config_value('main', 'author', opts['PKG_AUTHOR'])
    set_config_value('main', 'author_email', opts['PKG_AUTHOR_EMAIL'])

    # Destination and template directories
    opts['DEST_DIR'] = prompt(
        'destination', 'Destination DIR', opts['DEST_DIR'])
    opts['DEST_DIR'] = os.path.join(opts['DEST_DIR'], opts['PKG_NAME'])

    opts['TMPL_DIR'] = prompt('template', 'Template DIR', opts['TMPL_DIR'])

    tmpl_dir = os.path.realpath(os.path.expanduser(opts['TMPL_DIR']))
    if tmpl_dir[-1] != '/':
        tmpl_dir = tmpl_dir + "/"
    opts['TMPL_DIR'] = tmpl_dir

    # Copy the template and replace the proper values
    mk_pkg(opts, opts['DEST_DIR'], opts['TMPL_DIR'])

    # Virtualenv
    opts['USE_VENV'] = prompt('use_venv', 'Use Virtualenv', 'n')
    if opts['USE_VENV'].lower() in ['y', 'yes', '1']:
        opts['VENV'] = prompt('venv', 'Virtualenv Name', opts['PKG_NAME'])
        mk_virtual_env(opts['VENV'], opts['DEST_DIR'])


if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('-a', '--author', dest='pkg_author',
                      help='The name of the author.')
    parser.add_option('-e', '--author-email', dest='pkg_author_email',
                      help='The email of the author.')
    parser.add_option('-u', '--url', dest='pkg_url',
                      help='The URL of the project page.')
    parser.add_option('-n', '--name', dest='app_name',
                      help='The name of the application, i.e. django-myapp')
    parser.add_option('-p', '--package', dest='pkg_name',
                      help='The name of the installed package, i.e. myapp')
    parser.add_option('-v', '--virtenv', dest='venv',
                      help='The name of the virtualenv.')
    parser.add_option('-d', '--dest', dest='destination',
                      help='Where to put the new application.')
    parser.add_option('-t', '--template', dest='template',
                      help='The application template to use as a basis for '\
                           'the new application.')
    parser.add_option('-i', '--use-venv', dest='use_venv',
                      help='Wheater or not to create the virtuelenv')
    (options, args) = parser.parse_args()

    sys.exit(main(options))
