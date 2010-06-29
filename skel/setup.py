import os, sys
from setuptools import setup, find_packages

def read_file(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except:
        return ''

setup(
    name = "$$$$APP_NAME$$$$",
    version = __import__('$$$$APP_NAME$$$$').get_version().replace(' ', '-'),
    url = '',
    author = '$$$$AUTHOR$$$$',
    author_email = '',
    description = '',
    long_description = read_file('README'),
    packages = find_packages(),
    include_package_data = True,
    classifiers = [
    ],
)
