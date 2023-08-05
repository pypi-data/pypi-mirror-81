'''
Kids without umbrellas have to run !

====================================

Join ISCLUB TEAM:

Github: https://github.com/isclub
Email: 2731510961@gmail.com
QQ: 2731510961

====================================
'''

from setuptools import setup
from setuptools import find_packages
import os
import io

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
BASE_DIR = os.path.join(os.path.dirname(__file__))

with io.open(os.path.join(BASE_DIR, 'requirements.txt'), encoding='utf-8') as fh:
    REQUIREMENTS = fh.read()

setup(
    name="isclub-forum",
    version="0.0.1",
    author='snbck',
    author_email='snbckcode@gmail.com',
    packages=find_packages(),
    long_description=open('README.md', 'r', encoding="utf-8").read(),
    install_requires=REQUIREMENTS,
    include_package_data=True,
    long_description_content_type="text/markdown",
)

