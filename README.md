# Displot

Structural dislocation detector.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 3
* Numpy + Scipy + Matplotlib
* Scikit-image
* PyQt5

### Installing

#### On Windows (no command line):

Download and use the newest self-contained binary provided [here](https://github.com/bjstarosta/displot/releases).

#### Non-OS specific (using python from command line):

First ensure that you have Python 3 installed on your PC. For Windows, you can get it from [here](https://www.python.org/downloads/windows/). For GNU/Linux based OS use your favourite package manager to download it.

After you downloaded Python, either download and extract the zip containing the source code from this page, or install git and clone the repository:

```
$ git clone https://github.com/bjstarosta/displot  
$ cd displot
```

Then install the package and download the dependencies using:

```
$ python setup.py install
```

Alternatively, to use the package from within the cloned directory:

```
$ python setup.py develop
```

Using the above commands should automatically download all the required dependencies for you, provided your python installation has pip and setuptools.

#### Troubleshooting

While on Windows Python comes with pip preinstalled, on GNU/Linux based OS you might need to download pip first. Most repositories should have it listed as a package however.

While using setup.py you may encounter an error related to some of the dependencies:
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1051) -- Some packages may not be found!
```
Running the following command fixes this issue:
```
$ python -m pip install certifi
```
After this you should run the setup.py script again, and this time the dependency installation should proceed without issues.

## Built With

* [Python 3](https://www.python.org/)
* [Qt 5](http://doc.qt.io/qt-5/qt5-intro.html) - Using the [PyQt5](https://pypi.org/project/PyQt5/) bindings
* [Qt Designer](http://doc.qt.io/qt-5/qtdesigner-manual.html) - Recommended for editing layouts
* [Feather open source icon pack](tps://github.com/feathericons/feather)

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Bohdan Starosta** - [bjstarosta](https://github.com/bjstarosta)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Simon Kraeusel for his original SADC work which inspired this piece of software
* Ben Hourahine for useful discussions and support
