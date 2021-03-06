# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from provy import __version__

setup(
    name='provy',
    version=__version__,
    description="provy is an easy-to-use server provisioning tool.",
    long_description="provy is an easy-to-use server provisioning tool.",
    keywords='provisioning devops infrastructure server',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='https://provy.readthedocs.org',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Topic :: System :: Installation/Setup'
    ],
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    package_data={
        '': ['*.template'],
    },

    install_requires=[
        "fabric",
        "jinja2",
        "configobj",
    ],

    entry_points={
        'console_scripts': [
            'provy = provy.console:main',
        ],
    },

)
