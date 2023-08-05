=============================
django-airports-legacy
=============================

Quickstart
----------
Requirements (Ubuntu 16.04)::

    sudo apt-get install -y libsqlite3-mod-spatialite binutils libproj-dev gdal-bin

Install django-airports-legacy::

    pip install django-airports-legacy

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'cities',
        'airports',
        'django.contrib.gis',
        ...
    )


Features
--------

The ```airports``` manage command has options, see ```airports --help``` output.
Second run will update the DB with the latest data from the source csv file.

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox




History
-------

0.2.2 (2020-10-01)
++++++++++++++++++

* upstream django-cities==0.6 requirement
* better doc on installation


0.2.1 (2019-12-17)
++++++++++++++++++

* compatibility with Django 3.0


0.2 (2019-09-15)
++++++++++++++++

* renaming and uploading to Pypi



0.1.5 (2018-03-08)
++++++++++++++++++

* creation of the HISTORY.rst file;


