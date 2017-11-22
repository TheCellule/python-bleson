import sys, os
import unittest
from setuptools import setup, find_packages

version='0.0.10'

#pip setuptools wheel twine

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

if sys.argv[-1] == 'publish':
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()


def test_suite():
    # print native diagnostic information on an abort (e.g. for faultfinding blesonwin native errors)
    # alternatively add to python parameters:  -X faulthandler
    #import faulthandler
    #faulthandler.enable()
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    return test_suite

setup(
    name='bleson',
    version=version,
    packages= find_packages(),
    url='https://github.com/TheCellule/python-bleson',
    license='MIT',
    author='TheCellule',
    author_email='thecellule@gmail.com',
    description='Bluetooth LE Library',
    extras_require = {
        ':platform_system=="Windows"': [
            'blesonwin'
        ],
        ':platform_system=="Darwin"': [
            'pyobjc'
        ]
    },
    test_suite='setup.test_suite',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
