# pylint: disable=missing-docstring
from setuptools import setup


def get_long_description():
    with open("README.rst", "r") as file:
        return file.read()


setup(
    name="social-auth-kerberos",
    version="0.3.2",
    description="Kerberos authentication backend for Python Social Auth",
    long_description=get_long_description(),
    author="Kiwi TCMS",
    author_email="info@kiwitcms.org",
    url="https://github.com/kiwitcms/python-social-auth-kerberos/",
    keywords="social auth, kerberos",
    install_requires=["social-auth-core", "gssapi"],
    packages=["social_auth_kerberos"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Internet",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)
