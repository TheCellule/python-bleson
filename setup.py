import sys, os
import unittest
from setuptools import setup, find_packages

from distutils.command.clean import clean
from distutils.core import Command
from distutils.dir_util import remove_tree

# bleson/VERSION file must follow: https://www.python.org/dev/peps/pep-0440/

version_file = open(os.path.join('bleson', 'VERSION'))
version = version_file.read().strip()

# support overriding version from env
version=os.getenv('MODULE_VERSION', version)

if not version:
    raise ValueError("Version not set")

print("Version={}".format(version))

class SimpleCommand(Command):
    # default some Command abstract class boilerplate for subclasses
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


class SuperClean(clean):

    def run(self):
        self.all = True
        super().run()
        # remove_tree doesn't ignore errors. liek it says it should..
        if os.path.exists('sdist'):
            remove_tree('sdist')
        if os.path.exists('dist'):
            remove_tree('dist')


class Tag(SimpleCommand):

    def run(self):
        rc = os.system("git tag -a %s -m 'version %s'" % (version, version))
        if rc:
            sys.exit(rc)
        rc = os.system("git push --tags")
        sys.exit(rc)


class Publish(SimpleCommand):

    def run(self):
        pypi_repo_name = os.getenv('PYPI_REPO_NAME', 'pypitest')

        # TODO: use a Pythonic method
        upload_cmd = "twine upload --repository {} dist/*".format(pypi_repo_name)
        print(upload_cmd)
        rc = os.system(upload_cmd)
        sys.exit(rc)

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
    test_suite='tests',
    cmdclass={
        'clean': SuperClean,
        'publish': Publish,
        'tag': Tag,
    },
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
