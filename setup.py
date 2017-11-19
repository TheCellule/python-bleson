from setuptools import setup, find_packages

setup(
    name='bleson',
    version='0.0.9',
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
    }
)
