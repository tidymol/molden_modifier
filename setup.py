#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

# Standard Library
import io
import re
from glob import glob
from os.path import basename, dirname, join, splitext

# Third Party Libraries
from setuptools import find_packages, setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


def requires(filename):
    """Returns a list of all pip requirements

    :param filename: the Pip requirement file (usually 'requirements.txt')
    :return: list of modules
    :rtype: list
    """
    modules = []
    with open(filename, 'r') as pipreq:
        for line in pipreq:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            modules.append(line)
    return modules


# ------------------------------------------------------
setup(
    name='molden-modifier',
    version='0.1.0',
    license='MIT',
    description='Helps to modify molden files',
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', read('README.rst')),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', read('CHANGELOG.rst'))
    ),
    author='Jürgen Löhel, Alba Vargas-Caamal',
    author_email='Jürgen Löhel <juergen@loehel.de>',
    url='https://bitbucket.com/jloehel/molden_modifier',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS',
        'Environment :: Console',
	'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
        'Topic :: Scientific/Engineering :: Chemistry',
    ],
    keywords=[
        'molden', 'chemistry', 'modify', 'helper',
    ],

    install_requires=requires('requirements.txt'),

    # Required packages for using "setup.py test"
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-catchlog'],

    entry_points={
        'console_scripts': [
            'molden_modifier = molden_modifier.cli:main',
        ]
    },
)
