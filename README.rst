Kerberos authentication backend for Python Social Auth
======================================================

.. image:: https://travis-ci.org/kiwitcms/python-social-auth-kerberos.svg?branch=master
    :target: https://travis-ci.org/kiwitcms/python-social-auth-kerberos

.. image:: https://coveralls.io/repos/github/kiwitcms/python-social-auth-kerberos/badge.svg?branch=master
   :target: https://coveralls.io/github/kiwitcms/python-social-auth-kerberos?branch=master

Introduction
------------

This package provides Kerberos backend for Python Social Auth. It can be used to
enable passwordless authentication inside a Django app or any other application
that supports Python Social Auth. This is a pure Python implementation which doesn't
depend on Apache ``mod_auth_kerb``.

To install::

    pip install social-auth-kerberos


Then
`configure PSA <https://python-social-auth.readthedocs.io/en/latest/configuration/index.html>`_
and add the following settings::


    AUTHENTICATION_BACKENDS = [
        'social_auth_kerberos.backend.KerberosAuth',
        'django.contrib.auth.backends.ModelBackend',
    ]
    
    SOCIAL_AUTH_KRB5_KEYTAB = '/tmp/your-application.keytab'

For more information about Kerberos see:

- `How to configure Firefox for kerberos <https://people.redhat.com/mikeb/negotiate/>`_
- `How to configure kerberos on Fedora <https://fedoraproject.org/wiki/Kerberos_KDC_Quickstart_Guide>`_
- `How to generate a keytab file
  <https://docs.tibco.com/pub/spotfire_server/7.6.1/doc/html/tsas_admin_help/GUID-27726F6E-569C-4704-8433-5CCC0232EC79.html>`_

.. warning::

    USE AT YOUR OWN RISK!
    
    This module has been tested manually with Kiwi TCMS. Automated tests
    do not exist because we can't quite figure out how to use
    `gssapi-console <https://github.com/pythongssapi/gssapi-console>`_ as part of
    unit tests! If you do figure it out a pull request will be greatly appreciated!


Changelog
---------


v0.2.2 (10 Nov 2019)
~~~~~~~~~~~~~~~~~~~~

- Pin license version to GPLv2 for Tidelift


v0.2.1 (10 Dec 2018)
~~~~~~~~~~~~~~~~~~~~

- Initial release
