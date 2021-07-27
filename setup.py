from setuptools import setup
from setuptools import find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()
    

setup(
    name='totalwine-scraper',
    version='1.0.0',
    description='This package scrapes totalwine.com website for demanded count of listings and types for wine.',
    long_description=readme,
    author='Kasparas Karalius',
    author_email='',
    url='https://github.com/Karalius/totalwine-scraper',
    license=license,
    packages=find_packages(exclude=('tests*')),
)