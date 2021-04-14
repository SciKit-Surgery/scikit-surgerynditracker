# coding=utf-8
"""
Setup for scikit-surgerynditracker
"""

from setuptools import setup, find_packages
import versioneer

# Get the long description
with open('README.rst') as f:
    long_description = f.read()

setup(
    name='scikit-surgerynditracker',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description='Interface for Northern Digital (NDI) Trackers with data to NumPy arrays',
    long_description=long_description,
    url='https://weisslab.cs.ucl.ac.uk/WEISS/SoftwareRepositories/SNAPPY/scikit-surgerynditracker',
    author='Stephen Thompson',
    author_email='s.thompson@ucl.ac.uk',
    license='BSD-3 license',
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',

        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: System :: Hardware',
    ],

    keywords='medical imaging',

    packages=find_packages(
        exclude=[
            'docs',
            'tests',
        ]
    ),

    install_requires=[
        'six>=1.10',
        'numpy>=1.11',
        'ndicapi>=3.2.6',
        'scikit-surgerycore>=0.6.9'
    ],
)
