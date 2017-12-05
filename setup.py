import sys, os
import unittest
from setuptools import setup, find_packages

from distutils.command.clean import clean
from distutils.core import Command
from distutils.dir_util import remove_tree

HAS_SPHINX=False
try:
    from sphinx.setup_command import BuildDoc
    HAS_SPHINX=True


    class Doctest(Command):
        description = 'Run doctests with Sphinx'
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            from sphinx.application import Sphinx
            sph = Sphinx('./docs',  # source directory
                         './docs', # directory containing conf.py
                         './docs/_build',  # output directory
                         './docs/_build/doctrees',  # doctree directory
                         'doctest')  # finally, specify the doctest builder
            sph.build()
except ImportError:
    pass

# bleson/VERSION file must follow: https://www.python.org/dev/peps/pep-0440/

version_file = open(os.path.join('bleson', 'VERSION'))
version = version_file.read().strip()

# support overriding version from env
version=os.getenv('MODULE_VERSION', version)

if not version:
    raise ValueError("Version not set")

print("Version={}".format(version))

def _os_run_chk(cmd):
    print("CMD={}".format(cmd))
    rc = os.system(cmd)
    print("RC ={}".format(rc))
    if rc != 0:
        sys.exit(1)

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
        _os_run_chk("git tag -a RELEASE_%s -m 'Release version %s'" % (version, version))
        _os_run_chk("git push --tags")


class Publish(SimpleCommand):

    def run(self):
        # TODO: use a Pythonic method
        _os_run_chk("twine upload dist/*")


cmdclass={
        'clean': SuperClean,
        'publish': Publish,
        'tag': Tag,
    }


if HAS_SPHINX:
    cmdclass['doc'] = BuildDoc
    cmdclass['doctest'] = Doctest

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
    cmdclass=cmdclass,
    command_options={
        'doc': {
            'build_dir': ('setup.py', 'docs/_build'),
        },
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
