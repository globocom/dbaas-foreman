#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read()

with open('requirements_test.txt') as requirements_test_file:
    test_requirements = requirements_test_file.read()


setup(
    name='dbaas_foreman',
    version='0.1.1',
    description="DBaaS Foreman is a simple foreman api wrapper for DBaaS",
    long_description=readme + '\n\n' + history,
    author="Felippe da Motta Raposo",
    author_email='raposo.felippe@gmail.com',
    url='https://github.com/felippemr/dbaas_foreman',
    packages=[
        'dbaas_foreman',
    ],
    package_dir={'dbaas_foreman':
                 'dbaas_foreman'},
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='dbaas_foreman',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
