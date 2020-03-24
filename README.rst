Kerberos authentication backend for Python Social Auth
======================================================

.. image:: https://github.com/kiwitcms/python-social-auth-kerberos/workflows/integration%20test/badge.svg
    :target: https://github.com/kiwitcms/python-social-auth-kerberos/actions

.. image:: https://coveralls.io/repos/github/kiwitcms/python-social-auth-kerberos/badge.svg?branch=master
   :target: https://coveralls.io/github/kiwitcms/python-social-auth-kerberos?branch=master

.. image:: https://tidelift.com/badges/package/pypi/social-auth-kerberos
    :target: https://tidelift.com/subscription/pkg/pypi-social-auth-kerberos?utm_source=pypi-social-auth-kerberos&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://opencollective.com/kiwitcms/tiers/sponsor/badge.svg?label=sponsors&color=brightgreen
   :target: https://opencollective.com/kiwitcms#contributors
   :alt: Become a sponsor

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter


This package provides Kerberos backend for Python Social Auth. It can be used to
enable passwordless authentication inside a Django app or any other application
that supports Python Social Auth. This is a pure Python implementation which doesn't
depend on Apache ``mod_auth_kerb``.

Installation
------------

To install::

    pip install social-auth-kerberos


Configuration
-------------

`Configure Python Social Auth <https://python-social-auth.readthedocs.io/en/latest/configuration/index.html>`_
and then make sure you have the following settings enabled::


    AUTHENTICATION_BACKENDS = [
        'social_auth_kerberos.backend.KerberosAuth',
        'django.contrib.auth.backends.ModelBackend',
    ]
    
    SOCIAL_AUTH_KRB5_KEYTAB = '/Kiwi/your-application.keytab'

**IMPORTANT:**

The principal name for your Kiwi TCMS web service must be
``HTTP/<fqdn.example.com>@REALM.EXAMPLE.COM`` where ``fqdn.example.com`` is
the domain name of the Kiwi TCMS server and ``REALM.EXAMPLE.COM`` is the
Kerberos realm that is used in your organization.

``/Kiwi/your-application.keytab`` is the keytab file for your
web app principal! If you install this inside a Docker container make sure
to ``chown 1001:root``!


Pipeline configuration
----------------------

Python Social Auth, and by extension this plugin, will create new user accounts
upon first access of the web interface. In Kiwi TCMS users need to either be
in the special group *Tester* or have sufficient permissions to add/edit/delete
objects.

You can automatically assign new accounts to the *Tester* group if
you append ``social_auth_kerberos.pipeline.initiate_defaults`` to the end
of the ``SOCIAL_AUTH_PIPELINE`` setting.

**WARNING:** this is not done for you automatically because some administrators
may want to employ different behaviour for newly registered accounts!


Kerberos configuration
----------------------

For more information about Kerberos see:

- `How to configure Firefox for kerberos <https://people.redhat.com/mikeb/negotiate/>`_
- `How to configure kerberos on Fedora <https://fedoraproject.org/wiki/Kerberos_KDC_Quickstart_Guide>`_
- `How to generate a keytab file
  <https://docs.tibco.com/pub/spotfire_server/7.6.1/doc/html/tsas_admin_help/GUID-27726F6E-569C-4704-8433-5CCC0232EC79.html>`_

or check out ``tests/Dockerfile.kerberos``.



Changelog
---------


v0.2.4 (24 Mar 2020)
~~~~~~~~~~~~~~~~~~~~

- Add ``social_auth_kerberos.pipeline`` with function to initialize
  default permissions for newly created accounts. See section
  *Pipeline configuration*
- Update README with more information how to configure this plugin
- Enable integration testing with Kerberos and coverage collection


v0.2.3 (22 Mar 2020)
~~~~~~~~~~~~~~~~~~~~

- Keep a reference to current user before checking anything else.
  Resolves a crash for clients which know that the server is
  Kerberos enabled and directly send the Authorization header
- Be more tolerant to authorization request headers which don't
  match RFC-4459, section 4.2


v0.2.2 (10 Nov 2019)
~~~~~~~~~~~~~~~~~~~~

- Pin license version to GPLv2 for Tidelift


v0.2.1 (10 Dec 2018)
~~~~~~~~~~~~~~~~~~~~

- Initial release
