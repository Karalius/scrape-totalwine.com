from setuptools import setup
from setuptools import find_packages


with open("README.md", "r") as description:
    long_description = description.read()

    
setup(
    name='totalwine-scraper',
    version='1.0.0',
    description='This package scrapes totalwine.com website for demanded count of listings and types for wine.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Kasparas Karalius',
    author_email='',
    url='https://github.com/Karalius/totalwine-scraper',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        "atomicwrites==1.4.0",
        "attrs==21.2.0",
        "certifi==2021.5.30",
        "charset-normalizer==2.0.3",
        "colorama==0.4.4",
        "idna==3.2",
        "iniconfig==1.1.1",
        "numpy==1.21.1",
        "packaging==21.0",
        "pandas==1.3.1",
        "pluggy==0.13.1",
        "py==1.10.0",
        "pyparsing==2.4.7",
        "pytest==6.2.4",
        "python-dateutil==2.8.2",
        "pytz==2021.1",
        "requests==2.26.0",
        "six==1.16.0",
        "toml==0.10.2",
        "urllib3==1.26.6"
    ],
)
