# Ultralytics YOLO 🚀, GPL-3.0 license

import re
from pathlib import Path

import pkg_resources as pkg
from setuptools import find_packages, setup

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
# README = (PARENT / 'README.md').read_text(encoding='utf-8')
REQUIREMENTS = [f'{x.name}{x.specifier}' for x in pkg.parse_requirements((PARENT / 'requirements.txt').read_text())]


def get_version():
    return '0.0.1'


setup(
    name='bridge',
    version=get_version(),
    python_requires='>=3.7',
    license='GPL-3.0',
    description='',
    #long_description=README,
    install_requires=REQUIREMENTS,
    long_description_content_type='text/markdown',
    author='Ayush',
    author_email='ayush.chaurarsia@gmail.com',
    packages=find_packages(),  # required
    include_package_data=True,
)

