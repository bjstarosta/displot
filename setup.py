import subprocess
import sys

from setuptools import setup, find_packages
from setuptools.command import install, develop
from displot.config import DISPLOT_INFO


def pip_install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

class displotDevelop(develop.develop):
    def run(self):
        print('Installing PyQt5 using pip')
        pip_install('PyQt5')
        develop.develop.run(self)

class displotInstall(install.install):
    def run(self):
        print('Installing PyQt5 using pip')
        pip_install('PyQt5')
        install.install.run(self)


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
        'opencv-python',
        'PyWavelets'
    ],
    cmdclass={
        'install': displotInstall,
        'develop': displotDevelop
    },
)
