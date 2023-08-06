#!/usr/bin/env python3
from setuptools import setup


from djangocms_socialshare import __version__


setup(
    name='djangocms-socialshare',
    version=__version__,
    url='https://gitlab.com/what-digital/djangocms-socialshare',
    author='Victor Yunenko',
    packages=[
        'djangocms_socialshare',
    ],
    include_package_data=True,
    install_requires=[
        'django >= 2.2, < 4',
        'django-cms >= 3.7.2, < 4',
    ],
)
