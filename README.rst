===============
continuum-flask
===============
Small framework built on top of Flask to provide basic functionality common to
all of our internal projects.

.. note:: This is meant for internal use at `Continuum Analytics`_ and is
          released only in the hopes that others might find it useful.


------------
Installation
------------

Add the following to your ``environment.yml`` file you're using `conda-env`_:

.. code-block:: yaml

    channels:
      - continuumio
    dependencies:
      - continuum-flask

Otherwise, install it directly with ``conda`` like this:

.. code-block:: bash

    conda install -c continuumio continuum-flask


-----
Usage
-----
Replace the ``flask.Flask`` module with ``continuum_flask.Flask``.  This assumes
you have a ``settings`` module along side your application that will be
imported.  That can be overridden by providing an explicit ``settings`` kwarg
when instantiating ``Flask``.

The normal directory structure looks like this:

.. code-block:: text

    application/
      - __init__.py
      - settings.py

Your ``application/__init__.py`` should look something like this:


.. code-block:: python

    from continuum_flask import Flask


    def create_app():
        return Flask(__name__)

You can now run this in something like `gunicorn`_ from the command line with:

.. code-block:: bash

    gunicorn application:create_app


``kwargs``
----------

``settings``
    This is a string representing the module with your settings in it.  If this
    is not provided, it assumes it is in the same module as the server that's
    been initialized.

``blueprints``
    An array of strings to import when and register.  It assumes each of these
    modules has an attribute called ``blueprint`` that should be registered.
    This is registered inside the `app context`_, so you have access to any
    objects that are added to the application via ``current_app``.

    If the values added to ``blueprints`` are a string, they are registered at
    the via a simple ``register_blueprint(some_module)`` call.  However, you
    can specify both ``args`` and ``kwargs`` to register via this syntax:

    .. code-block:: python

        ('some_blueprint', ('arg1', 'arg2'), {'kwarg1': 'foo', 'kwarg2': 'bar'})
        ('some_other', ('arg1', 'arg2'))
        ('yet_another', {'kwarg1': 'foo', 'kwarg2': 'bar'})

    The first value is the name of the module that is imported inside the app
    context, the second argument is an optional iterable list of args and the
    third value is an optional dictionary of kwargs.  You can omit either the
    args or the kwargs.

.. _app context: http://flask.pocoo.org/docs/0.10/appcontext/
.. _conda-env: https://github.com/conda/conda-env/
.. _Continuum Analytics: http://continuum.io/
.. _gunicorn: http://gunicorn.org
