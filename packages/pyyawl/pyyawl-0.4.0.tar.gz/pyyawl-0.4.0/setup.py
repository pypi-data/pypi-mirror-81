#!/usr/bin/env python
"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().split('\n')

with open('requirements_dev.txt', 'r') as fh:
    test_requirements = fh.read().split('\n')

setup_requirements = [
    'pytest-runner',
]

setup(
    author="Fabio Fumarola",
    author_email='fabiofumarola@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Yet another simple workflow language for python",
    entry_points={
        'console_scripts': ['yawl=pyyawl.cli:main',],
    },
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pyyawl',
    name='pyyawl',
    packages=find_packages(include=['pyyawl', 'pyyawl.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/fabiofumarola/pyyawl',
    version='0.4.0',
    zip_safe=False,
)
