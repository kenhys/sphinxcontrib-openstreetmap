# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_desc = '''
This package contains the openstreetmap Sphinx extension.

.. add description here ..
'''

requires = ['Sphinx>=0.6']

setup(
    name='sphinxcontrib-openstreetmap',
    version='0.4.0',
    url='https://github.com/kenhys/sphinxcontrib-openstreetmap',
    download_url='http://pypi.python.org/pypi/sphinxcontrib-openstreetmap',
    license='BSD',
    author='HAYASHI Kentaro',
    author_email='kenhys@gmail.com',
    description='Sphinx "OpenStreetMap" extension',
    long_description=long_desc,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Sphinx :: Extension',
        #'Framework :: Sphinx :: Theme',
        'Topic :: Documentation',
        'Topic :: Utilities',
    ],
    platforms='any',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    namespace_packages=['sphinxcontrib'],
)
