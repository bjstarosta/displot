from setuptools import setup, find_packages
from displot.displot import DISPLOT_INFO


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name=DISPLOT_INFO['appTitle'],
   version=DISPLOT_INFO['appVersion'],
   description='Structural dislocation detector.',
   long_description=long_description,
   license="GPLv3",
   author=DISPLOT_INFO['author'],
   author_email=DISPLOT_INFO['authorEmail'],
   packages=find_packages(),
   install_requires=[
    'numpy',
    'scipy',
    'scikit-image',
    'PyQt5'
    ],
)
