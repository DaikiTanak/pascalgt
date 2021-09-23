#!/usr/bin/env python
import datetime
from setuptools import setup, find_packages


def _requires_from_file(filename):
    return open(filename).read().splitlines()


readme = open('README.md').read()
VERSION = '0.0.2' + "_" + datetime.datetime.now().strftime('%Y%m%d%H%M')[2:]
setup(
    # Metadata
    name='pascalgt',
    version=VERSION,
    author='Daiki Tanaka',
    author_email='daiki.yosky@gmail.com',
    url='https://github.com/DaikiTanak/pascalgt',
    description='Tool for transform Pascal-VOC xml files and AWS Ground Truth manifest file.',
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    # Package info
    packages=find_packages(exclude=('*test*',)),
    install_requires=_requires_from_file('requirements.txt'),
    zip_safe=True,
    # Classifiers
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
