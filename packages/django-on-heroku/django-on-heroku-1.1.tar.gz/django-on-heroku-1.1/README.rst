django-on-heroku (Python Library)
=================================

This has been forked from `django-heroku <https://github.com/heroku/django-heroku>`_ because it was abandoned and then renamed to **django-on-heroku** because old project has been archived.

Current updates:

- renamed package from ``django-heroku`` to ``django-on-heroku``
- changed ``psycopg2`` to ``psycopg2-binary`` so it works and is installable
- added installation instructions
- fixed wipe'ing tables in Postgres
- ``whitenoise.middleware.WhiteNoiseMiddleware`` is injected after ``django.middleware.security.SecurityMiddleware``

--------------

This is a Django library for Heroku applications that ensures a seamless deployment and development experience.

This library provides:

-  Settings configuration (Static files / WhiteNoise).
-  Logging configuration.
-  Test runner (important for `Heroku CI <https://www.heroku.com/continuous-integration>`_).

--------------

Django 2.0 is targeted, but older versions of Django should be compatible. Only Python 3 is supported.

Installation
------------

    pip install django-on-heroku

Usage of Django-Heroku
----------------------

In ``settings.py``, at the very bottom::

    # Configure Django App for Heroku.
    import django_on_heroku
    django_on_heroku.settings(locals())

This will automatically configure ``DATABASE_URL``, ``ALLOWED_HOSTS``, WhiteNoise (for static assets), Logging, and Heroku CI for your application.

**Bonus points!**

If you set the ``SECRET_KEY`` environment variable, it will automatically be used in your Django settings, too!

If you set the ``CONN_MAX_AGE`` environment variable, it will automatically be used in your database settings, too!

Disabling Functionality
///////////////////////

``settings()`` also accepts keyword arguments that can be passed ``False`` as a value, which will disable automatic configuration for their specific areas of responsibility:

- ``databases``
- ``test_runner``
- ``staticfiles``
- ``allowed_hosts``
- ``logging``
- ``secret_key``
- ``geodjango``
- ``db_ssl_required``

-----------------------


Geodjango support
///////////////////////
To enable the Geodjango support pass the ``geodjango`` flag as ``True`` when calling ``settings()``::

    django_heroku.settings(locals(), geodjango=True)

-----------------------

You can also just use this library to provide a test runner for your Django application, for use on Heroku CI::

    import django_on_heroku
    TEST_RUNNER = 'django_on_heroku.HerokuDiscoverRunner'
