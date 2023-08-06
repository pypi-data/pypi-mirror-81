===============
 zope.app.i18n
===============

.. image:: https://img.shields.io/pypi/v/zope.app.i18n.svg
        :target: https://pypi.org/project/zope.app.i18n/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.app.i18n.svg
        :target: https://pypi.org/project/zope.app.i18n/
        :alt: Supported Python versions

.. image:: https://travis-ci.org/zopefoundation/zope.app.i18n.svg?branch=master
        :target: https://travis-ci.org/zopefoundation/zope.app.i18n

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.app.i18n/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.app.i18n?branch=master

Summary
=======

This package provides placeful persistent translation domains and
message catalogs along with ZMI views for managing them.

Caveats
=======

Currently this integration does not support the feature of plural messages
which is supported by the underlying ``zope.i18n`` library. In case you need
this feature, please discuss this in the issue tracker in the repository.
