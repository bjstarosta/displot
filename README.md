# displot

Displot is a pre-trained machine learning driven semiconductor surface analysis
program. It allows for automated detection of threading dislocations on images
of surfaces obtained using ECCI. The underlying neural network is based on the
[FusionNet][fusionnet] architecture.

## Install

This program is built using [Python 3.7][python]. If you are going to run it
from a GNU/Linux based OS, you will likely already have it installed. If you
are going to run it from a Windows based machine, you might need to download
the relevant Python distribution first.

First clone the repository using git:

    $ git clone https://github.com/bjstarosta/displot

Or manually download and unpack the source code into a directory within
Python's PATH.

The required environment can be reproduced using
[Anaconda][anaconda]/[Miniconda][miniconda]:

    $ conda create --name displot --file condaenv.txt

Alternatively, pip can be used:

    $ pip install -r requirements.txt

Be aware that if using pip it may also be necessary to install Qt5 binaries,
on which this software depends.

Finally, due to GitHub filesize limits, you will need to separately download
the latest neural network model (about 225MB) and place it in the
displot/weights directory. <!-- You will be given an option to do this
automatically upon program launch. -->

## Usage

The user interface can be started by running the following command from the
software directory:

    $ python -m displot

## License

Distributed under the GNU GPLv3 License. See `LICENSE` for more information.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available,
see the tags on this repository.

## Acknowledgments

* [Feather open source icon pack](tps://github.com/feathericons/feather)

## Contact

- E-mail: bohdan.starosta@strath.ac.uk

[fusionnet]: https://arxiv.org/abs/1612.05360
[python]: https://www.python.org/downloads/release/python-379/
[anaconda]: https://www.anaconda.com/
[miniconda]: https://docs.conda.io/en/latest/miniconda.html
