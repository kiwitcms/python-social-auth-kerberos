Kerberos authentication backend for Kiwi TCMS
=============================================

.. image:: https://travis-ci.org/kiwitcms/kiwitcms-auth-kerberos.svg?branch=master
    :target: https://travis-ci.org/kiwitcms/kiwitcms-auth-kerberos

.. image:: https://coveralls.io/repos/github/kiwitcms/kiwitcms-auth-kerberos/badge.svg?branch=master
   :target: https://coveralls.io/github/kiwitcms/kiwitcms-auth-kerberos?branch=master

Introduction
------------

TODO:

- package this backend and publish to PyPI
- enable testing
- why there are 2 classes for kerberos backend? which one if the real deal
  maybe 'tcms.auth.kerberos.ModAuthKerbBackend' ????
- check-out https://github.com/kiwitcms/Kiwi/issues/240


This package provides passwordless authentication for Kiwi TCMS via Kerberos.
This is turned off by default because most organizations do not use it. To enable
configure the following settings::

    MIDDLEWARE += [
        'django.contrib.auth.middleware.RemoteUserMiddleware',
    ]

    AUTHENTICATION_BACKENDS += [
        'tcms.auth.kerberos.ModAuthKerbBackend',
    ]

    KRB5_REALM='YOUR-DOMAIN.COM'


Also modify Kiwi TCMS ``Dockerfile`` to include the following lines::

    RUN yum -y install krb5-devel mod_auth_kerb
    RUN pip install kerberos
    COPY ./auth_kerb.conf /etc/httpd/conf.d/

Where ``auth_kerb.conf`` is your Kerberos configuration file for Apache!
More information about it can be found
`here <https://access.redhat.com/documentation/en-US/Red_Hat_JBoss_Web_Server/2/html/HTTP_Connectors_Load_Balancing_Guide/ch10s02s03.html>`_.

.. warning::

    Unless Kerberos authentication is configured and fully-operational the
    XML-RPC method `Auth.login_krbv()` will not work!
