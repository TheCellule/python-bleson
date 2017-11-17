import platform
from setuptools import setup, find_packages

install_requires = []

system = platform.system()
print("Running on",system)

if system == 'Windows':
    install_requires.append('blesonwin')
elif system == 'Darwin':
    install_requires.append('pyobjc')



setup(
    name='bleson',
    version='0.0.4',
    packages= find_packages(),
    install_requires=install_requires,
    url='https://github.com/TheCellule/python-bleson',
    license='MIT',
    author='TheCellule',
    author_email='thecellule@gmail.com',
    description='Bluetooth LE Library'
)
