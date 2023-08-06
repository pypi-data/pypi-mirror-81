Flask-Boost
===========

.. image:: http://img.shields.io/pypi/v/flask-turbo-boost.svg
   :target: https://pypi.python.org/pypi/flask-turbo-boost
   :alt: Latest Version
.. image:: http://img.shields.io/pypi/dm/flask-turbo-boost.svg
   :target: https://pypi.python.org/pypi/flask-turbo-boost
   :alt: Downloads Per Month
.. image:: http://img.shields.io/pypi/pyversions/flask-turbo-boost.svg
   :target: https://pypi.python.org/pypi/flask-turbo-boost
   :alt: Python Versions
.. image:: http://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/hustlzp/Flask-Boost/blob/master/LICENSE
   :alt: The MIT License

Flask application generator for boosting your development.

Features
--------

* **Well Defined Project Structure**

  * Use factory pattern to generate Flask app.
  * Use Blueprints to organize controllers.
  * Split controllers, models, forms, utilities, assets, Jinja2 pages, Jinja2 macros into different directories.
  * Organize Jinja2 page assets (HTML, JavaScript, CSS) to the same directory.
  * Organize Jinja2 macro assets (HTML, JavaScript, CSS) to the same directory.
  * API-Only Project Structure

* **Batteries Included**

  * Use Flask-SQLAlchemy and Flask-Migrate as database tools.
  * Use Searchable-Mixin for search every Models [Optional]
  * Use ActiveRecord-Like-Mixin for search every Models [Optional]
  * Use JWTAuth for authentication [Optional]
  * Use JsonSchema for validate incoming requests [Optional]

  * Use Flask-WTF to validate forms.
  * Use Flask-Security for user management.
  * Use Flask-Dance for social user authentication (Sample with facebook and google).
  * Use Bulma as frontend framework.

  * Dockerfile – Sample dockerfile for development
  * docker-compose.yml – Sample docker-compose for deployment
  * Use Gunicorn to run Flask app and Supervisor to manage Gunicorn processes.
  * Use Fabric as deployment tool.
  * Use Sentry to log exceptions.
  * Use Nginx to serve static files.
  * Use sub script command to generate admin and form from a model.

* **Scaffold Commands**

  * Generate project files: ``turbo new <project>``
  * Generate API-only project files: ``turbo new --api <project>``
  * Generate controller files: ``turbo new controller <controller>``
  * Generate action files: ``turbo new action <controller> <action> [-t]``
  * Generate form files: ``turbo new form <form>``
  * Generate model files: ``turbo new model <model>``
  * Generate macro files: ``turbo new macro <category> <macro>`` or ``boost new macro <macro>``



Installation
------------

::

    pip install flask-turbo-boost



Development Guide
-----------------

Init project
~~~~~~~~~~~~

::

    turbo new <your_project_name>

Setup backend requirements
~~~~~~~~~~~~~~~~~~~~~~~~~~
 
::

    cd <your_project_dir>
    virtualenv venv
    . venv/bin/activate (venv\Scripts\activate in Windows)
    pip install -r requirements.txt

**Note**: if you failed in ``pip install -r requirements.txt`` in Windows, try to install package binaries directly:

* pycrpyto: try to follow this article compiling-pycrypto-on-win7-64_, or get the complied pycrypyto library directly: archive_pycrpyto_library_.

.. _compiling-pycrypto-on-win7-64: https://yorickdowne.wordpress.com/2010/12/22/compiling-pycrypto-on-win7-64/
.. _archive_pycrpyto_library: http://archive.warshaft.com/pycrypto-2.3.1.win7x64-py2.7x64.7z

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name`` and encoding ``utf8``.

Update ``SQLALCHEMY_DATABASE_URI`` in ``config/development.py`` as needed.

Then init tables::

    flask db upgrade

Run app
~~~~~~~

Run local server::

    flask run


Scaffold commands
~~~~~~~~~~~~~~~~~

::

    turbo new <project>
    turbo new --api <project>
    turbo new controller <controller>
    turbo new action <controller> <action> [-t]
    turbo new form <form>
    turbo new model <model>
    turbo new macro <category> <macro>
    turbo new macro <macro>
    turbo -v
    turbo -h


First Production Deploy
-----------------------

Config server
~~~~~~~~~~~~~

Install mysql-server, python-virtualenv, git, supervisor, nginx, g++, python-dev, libmysqlclient-dev, libxml2-dev, libxslt-dev on your server.

Install requirements
~~~~~~~~~~~~~~~~~~~~

::

    git clone **.git
    cd <your_project_dir>
    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt

Config app
~~~~~~~~~~

Save ``config/production_sample.py`` as ``config/production.py``, update configs in ``config/production.py`` as needed and transfer it to server.

**Note**: remember to update ``SECRET_KEY`` in ``config/production.py``! You can generate random secret key as follows::

>>> import os
>>> os.urandom(24)

Init database
~~~~~~~~~~~~~

Create database with name ``your_project_name`` and encoding ``utf8``.

And run::

    export MODE=PRODUCTION
    flask db upgrade

Copy config files
~~~~~~~~~~~~~~~~~

Update project root path as needed in ``deploy/nginx.conf`` and ``deploy/supervisor.conf``.

::

    cp deploy/flask_env.sh /etc/profile.d/
    cp deploy/nginx.conf /etc/nginx/conf.d/<your_project_name>.conf
    cp deploy/supervisor.conf /etc/supervisor/conf.d/<your_project_name>.conf

Start app
~~~~~~~~~

::

    service nginx restart
    service supervisor restart


Daily Production Deploy
-----------------------

Update ``HOST_STRING`` in config with the format ``user@ip``.

Commit your codes and run::

    git push && fab deploy

P.S. If you wanna to deploy flask with Apache2, see this_ post.

.. _this: https://www.digitalocean.com/community/tutorials/how-to-use-apache-http-server-as-reverse-proxy-using-mod_proxy-extension

License
-------

MIT
