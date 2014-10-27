from setuptools import setup
from setuptools import find_packages

setup(
    name='GeobricksMODIS',
    version='0.1.1',
    author='Simone Murzilli; Guido Barbaglia',
    author_email='geobrickspy@gmail.com',
    packages=find_packages(),
    license='LICENSE.txt',
    long_description=open('README.md').read(),
    install_requires=[
        'flask', 'BeautifulSoup'
    ],
    url='http://pypi.python.org/pypi/GeobricksMODIS/'
)