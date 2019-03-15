#!/usr/bin/env python3

# setuptools
from setuptools import setup

# Globe Indexer
from globe_indexer import __version__

with open('README.md') as fin:
    long_description = fin.read()

setup(
    name="globe_indexer",
    version=__version__,
    description='Get information regarding cities around the world',
    long_description=long_description,
    packages=['globe_indexer'],
    install_requires=[
        'Flask>=1.0.2',
        'Flask-SQLAlchemy>=2.3.2',
        'Flask-WTF>=0.14.2',
        'pycountry>=18.12.8',
        'requests>=2.21.0',
        'SQLAlchemy>=1.3.0',
        'WTForms>=2.2.1',
    ],
    tests_require=[
        'Flask-Testing>=0.7.1',
        'coverage>=4.5.2',
        'pytest>=4.3.0',
        'pytest-cov>=2.6.1',
    ],
    author='Alex Hartoto',
    author_email='ahartoto.dev@gmail.com',
    url='https://github.com/ahartoto/globe-indexer',
    keywords=['globe', 'indexer', 'globe-indexer', 'rest', 'api', 'flask'],
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
