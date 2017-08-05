# Movie Trailer Website Project Submission
This directory contains the submission of Movie Trailer Website project from FSND.

## Environment
You need Python 2.7.

## How to install python
There are various ways to install python.
I show you 2 options in this README.

### Use Homebrew
[Homebrew](https://brew.sh/) is a package management system for Mac.

First, install Homebrew by the following command:

```sh
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then, install python:

```sh
$ brew install python
```

### Use Anaconda/Miniconda
[Anaconda](https://www.continuum.io/downloads) is a data science platform.
It is quite useful when we want to construct multiple environments for python:
e.g. If you install and use python 2.7 and 3.6 on the same computer, Anaconda is a good choice.

[Miniconda](https://conda.io/miniconda.html) is a subset of Anaconda, which includes python and basic libraries.

Anaconda/Miniconda works on Windoows, Mac and Linux.

Here, I show you how to install Miniconda on Mac. For other OSs, see [the official guide](https://conda.io/docs/install/quick.html).

1. Install Miniconda installer for Mac from [here](https://conda.io/miniconda.html)
2. Execute installer: `$ bash Miniconda3-latest-MacOSX-x86_64.sh`

## Generate the web page
The following command generates and open a html file `fresh_tomatoes.html`.

```sh
$ python entertainment_center.py
```

## Check the coding style
The coding style of python files are checked by pep8 lint.  
You can install pep8 by the following command:

```sh
$ pip install pep8
```

Then check the style by the following command:

```sh
$ pep8 foo.py
```
