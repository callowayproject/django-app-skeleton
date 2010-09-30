import os
from setuptools import setup, find_packages

def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''

DESC = " ".join(__import__('alphafilter').__doc__.splitlines()).strip()

setup(
    name = "$$$$APP_NAME$$$$",
    version = __import__('$$$$APP_NAME$$$$').get_version().replace(' ', '-'),
    url = '',
    author = '$$$$AUTHOR$$$$',
    author_email = '',
    description = DESC,
    long_description = read_file('README'),
    packages = find_packages(),
    license = 'Apache 2.0',
    include_package_data = True,
    install_requires=read_file('requirements.txt'),
    classifiers = [
    ],
)
