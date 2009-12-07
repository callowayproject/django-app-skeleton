#!/usr/bin/env python

import os, random, subprocess

CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
BLACKLIST = (
    'jquery',
    '.tar.gz',
    'admin/css',
    'admin/img',
    'admin/js',
    '/.git/'
)

def replace(repl, text):
    text = text.replace('/gitignore', '/.gitignore')
    for key, value in repl.iteritems():
        text = text.replace('$$$$%s$$$$' % (key,), value)
    return text

def main():
    repl = {}
    an = raw_input('Application name: ')
    repl['APP_NAME'] = an
    
    dest_dir = raw_input('Destination directory (currently at %s): ' % (os.getcwd(),))
    dest = os.path.join(dest_dir, repl['APP_NAME'])
    os.makedirs(dest)
    
    for root, dirs, files in os.walk('./skel/'):
        for filename in files:
            source_fn = os.path.join(root, filename)
            dest_fn = replace(repl, os.path.join(dest, root.replace('./skel/', ''), replace(repl, filename)))
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
                data = replace(repl, data)
            open(dest_fn, 'w').write(data)
            os.chmod(dest_fn, os.stat(source_fn)[0])
    repl['virtenv'] = raw_input('Virtual environment name (e.g. %s): ' % an)
    if not repl['virtenv']:
        repl['virtenv'] = an
    
    print "Making the virtual environment (%s)..." % repl['virtenv']
    subprocess.call(['source /usr/local/bin/virtualenvwrapper_bashrc;cd %s;mkvirtualenv --no-site-packages %s;easy_install pip' % (dest, repl['virtenv']), ], env=os.environ, executable='/bin/bash', shell=True)
    subprocess.call(['source /usr/local/bin/virtualenvwrapper_bashrc;cat > $WORKON_HOME/%s/bin/postactivate <<END\n#!/bin/bash/\ncd %s\nEND\nchmod +x $WORKON_HOME/%s/bin/postactivate'%(repl['virtenv'], dest,repl['virtenv'])], env=os.environ, executable='/bin/bash', shell=True)
    print "Now type: workon %s" % repl['virtenv']

if __name__ == '__main__':
    main()