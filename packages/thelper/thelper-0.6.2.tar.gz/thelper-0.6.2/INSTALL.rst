.. _install-guide:

============
Installation
============

Docker
======

Starting with v0.3.2, the latest stable version of the framework is pre-built and available from the
`docker hub <docker-hub_>`_. To get a copy, simply pull it via::

  $ docker pull plstcharles/thelper

You should then be able to launch sessions in containers as such::

  $ docker run -it plstcharles/thelper thelper <CLI_ARGS_HERE>

The image is built from ``nvidia/cuda``, meaning that it is compatible with ``nvidia-docker`` and
supports CUDA-enabled GPUs. To run a GPU-enabled container, install `the runtime using these
instructions <nvidia-docker_>`_, and add ``--runtime=nvidia`` to the arguments given to ``docker run``.

.. _docker-hub: https://hub.docker.com/r/plstcharles/thelper
.. _nvidia-docker: https://github.com/NVIDIA/nvidia-docker


Installing from source
======================

If you wish to modify the framework's source code or develop new modules within the framework itself,
follow the installation instructions below.

Linux
-----

You can use the provided Makefile to automatically create a conda environment on your system that will contain
the thelper framework and all its dependencies. In your terminal, simply enter::

  $ cd <THELPER_ROOT>
  $ make install

If you already have conda installed somewhere, you can force the Makefile to use it for the installation of the
new environment by setting the ``CONDA_HOME`` variable before calling make::

  $ export CONDA_HOME=/some/path/to/miniconda3
  $ cd <THELPER_ROOT>
  $ make install

The newly created conda environment will be called 'thelper', and can then be activated using::

  $ conda activate thelper

Or, assuming conda is not already in your path::

  $ source /some/path/to/miniconda3/bin/activate thelper


Other systems
-------------

If you cannot use the Makefile, you will have to install the dependencies yourself. These dependencies are
listed in the `requirements file <https://github.com/plstcharles/thelper/blob/master/requirements.txt>`_,
and can also be installed using the conda environment configuration file provided `here`__. For the latter
case, call the following from your terminal::

  $ conda env create --file <THELPER_ROOT>/conda-env.yml -n thelper

.. __: https://github.com/plstcharles/thelper/blob/master/conda-env.yml

Then, simply activate your environment and install the thelper package within it::

  $ conda activate thelper
  $ pip install -e <THELPER_ROOT> --no-deps

On the other hand, although it is *not* recommended since it tends to break PyTorch, you can install the dependencies
directly through pip::

  $ pip install -r <THELPER_ROOT>/requirements.txt
  $ pip install -e <THELPER_ROOT> --no-deps


Anaconda
========

Starting with v0.2.5, a stable version of the framework can be installed directly (with its dependencies)
via `Anaconda <https://docs.anaconda.com/anaconda/install/>`_. In a conda environment, simply enter::

  $ conda config --env --add channels plstcharles
  $ conda config --env --add channels conda-forge
  $ conda config --env --add channels pytorch
  $ conda install thelper

This should install a stable version of the framework on Windows and Linux for Python 3.6 or 3.7. You
can check the release notes `on GitHub <github-changelog_>`_, and pre-built packages `here <anaconda-hub_>`_.

Note that due to Travis build limitations (as of November 2019), conda package builds and deployments
have been stalling and have required manual uploads. This means that the conda packages are fairly likely
to be out-of-date compared to those on Docker Hub and PyPI. As such, we now recommend users to install the
framework through the "Install from source" method above.

.. _github-changelog: https://github.com/plstcharles/thelper/blob/master/CHANGELOG.rst
.. _anaconda-hub: https://anaconda.org/plstcharles/thelper


Testing the installation
========================

You should now be able to print the thelper package version number to see if the package is properly installed and
that all dependencies can be loaded at runtime::

  (conda-env:thelper) username@hostname:~/devel/thelper$ python
    Python X.Y.Z |Anaconda, Inc.| (default, YYY XX ZZZ, AA:BB:CC)
    [GCC X.Y.Z] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import thelper
    >>> print(thelper.__version__)
    x.y.z

You can now refer to the `[user guide]`__ for more information on how to use the framework.

.. __: https://thelper.readthedocs.io/en/latest/user-guide.html


Documentation
=============

The sphinx documentation is generated automatically via `readthedocs.io <https://readthedocs.org/projects/thelper/>`_,
but it might still be incomplete due to buggy apidoc usage/platform limitations. To build it yourself, use the makefile::

  $ cd <THELPER_ROOT>
  $ make docs

The HTML documentation should then be generated inside ``<THELPER_ROOT>/docs/build/html``. To browse it, simply open the
``index.html`` file there.
