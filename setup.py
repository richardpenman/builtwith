import os
from distutils.core import setup

def read(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='reverse_engineer', 
    version='1.1',
    packages=['reverse_engineer'],
    package_dir={'reverse_engineer' : '.'}, # look for package contents in current directory
    author='Richard Penman',
    author_email='richard@webscraping.com',
    description='Detect the technology used by a website, such as Apache, JQuery, and Wordpress.',
    long_description=read('README.rst'),
    url='https://bitbucket.org/richardpenman/reverse_engineer',
    license='lgpl'
)
