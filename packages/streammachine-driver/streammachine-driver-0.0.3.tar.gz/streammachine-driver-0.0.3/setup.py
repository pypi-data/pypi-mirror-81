#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    author="Stream Machine B.V.",
    author_email='apis@streammachine.io',
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
    ],
    description=" Common Schema for Stream Machine driver",
    install_requires=[
        "streammachine-schemas-common==0.0.1"
    ],
    long_description=readme,
    include_package_data=True,
    keywords='streammachine api client driver',
    name='streammachine-driver',
    packages=find_packages(),
    namespace_packages=["streammachine"],
    setup_requires=[],
    version='0.0.3',
    zip_safe=False,
)
