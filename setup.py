from setuptools import setup, find_packages
from displot.displot import displot_info


with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name=displot_info['appTitle'],
   version=displot_info['appVersion'],
   description='Structural dislocation detector.',
   long_description=long_description,
   license="GPLv3",
   author=displot_info['author'],
   author_email=displot_info['authorEmail'],
   packages=find_packages(),
   install_requires=[
    'numpy',
    'scipy',
    'scikit-image',
    'PyQt5'
    ],
)
