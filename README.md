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

#### On Windows/Linux (using python from command line):

First clone the repository to a folder on your PC:

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

## Built With

* [Python 3](https://www.python.org/)
* [Qt 5](http://doc.qt.io/qt-5/qt5-intro.html) - Using the [PyQt5](https://pypi.org/project/PyQt5/) bindings
* [Qt Designer](http://doc.qt.io/qt-5/qtdesigner-manual.html) - Recommended for editing layouts

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags).

## Authors

* **Bohdan Starosta** - [bjstarosta](https://github.com/bjstarosta)

## License

This project is licensed under the GNU GPLv3 License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

* Simon Kraeusel for his original SADC work which inspired this piece of software
* Ben Hourahine for useful discussions and support
