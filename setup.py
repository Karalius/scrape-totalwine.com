from setuptools import setup
from setuptools import find_packages


setup(
    name='totalwine-scraper',
    version='1.0.0',
    package_dir={'': 'totalwine_scraper'},
    description='This package scrapes totalwine.com website for demanded count of listings and types for wine.',
    author='Kasparas Karalius',
    author_email='',
    url='https://github.com/Karalius/totalwine-scraper',
    license='MIT',
    packages=find_packages(exclude=('tests*')),
)
