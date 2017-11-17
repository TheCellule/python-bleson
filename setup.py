import platform
from setuptools import setup, find_packages

install_requires = []

system = platform.system()
print("Running on",system)

if system == 'Windows':
    # Wheels are not yet supported by setuptools.
    install_requires.append('blesonwin')
    #import pip
    #pip.main(['install', 'blesonwin'])
elif system == 'Darwin':
    # Wheels are not yet supported by setuptools.
    install_requires.append('pyobjc')
    #import pip
    #pip.main(['install', 'pyobjc'])



setup(
    name='bleson',
    version='0.0.6',
    packages= find_packages(),
    install_requires=install_requires,
    url='https://github.com/TheCellule/python-bleson',
    license='MIT',
    author='TheCellule',
    author_email='thecellule@gmail.com',
    description='Bluetooth LE Library'
)
