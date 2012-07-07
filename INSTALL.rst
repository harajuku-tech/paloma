========================================================================
**paloma** Installation Instructions
========================================================================

This section contains information about 
how to download and install **paloma** in your system. 
It also contains brief instructions about how
to build the included documentation.

Requirements
============

Detailed information about the minimum supported Django version and 
other Python modules that may be required in order to run this software is shown below:

.. literalinclude:: ../requirements.txt

This information exists in the ``requirements.txt`` file 
inside the ** paloma ** distribution package. 
If ``pip`` is used to install this software,
then all these dependencies will also be installed, 
if they are not already installed in your system.


Soruce
========

Clone from Github.

URL is https://github.com/harajuku-tech/paloma


Install
=======

To install **paloma** from soruce code, use the provided installation script::

    python setup.py install


Or it is also possible to install this application directly from
the `source code repository`_ using ``pip``::

    pip install -e git+https://github.org/harajuku-tech/paloma#egg=paloma

The above command will install the latest development release of **paloma**.


How to build the documentation
==============================

This project's documentation is located in source form under the ``docs``
directory. In order to convert the documentation to a format that is
easy to read and navigate you need the ``sphinx`` package.

You can install ``sphinx`` using ``pip``::

    pip install sphinx

Or ``easy_install``::

    easy_install sphinx

Once ``sphinx`` is installed, change to the ``docs`` directory, open a shell
and run the following command::

    make html

This will build a HTML version of the documentation. You can read the
documentation by opening the following file in any web browser::

    docs/_build/html/index.html
