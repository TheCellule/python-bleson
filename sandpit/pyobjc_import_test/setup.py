import unittest
from setuptools import setup, find_packages

def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests')
    return test_suite

setup(
    name='testpkg',
    version='0.0.1',
    packages= [],
    test_suite='setup.test_suite')