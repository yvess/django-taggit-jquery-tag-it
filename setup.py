# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
 
long_description = open('README.md').read()
 
setup(
    name='django-taggit-autocomplete',
    version='0.1',
    description='Autocompletion for django-taggit',
    long_description=long_description,
    author=u'Iván Raskovsky',
    author_email='raskovsky@gmail.com',
    url='https://github.com/rasca/django-taggit-jquery-tag-it',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    zip_safe=False,
) 
