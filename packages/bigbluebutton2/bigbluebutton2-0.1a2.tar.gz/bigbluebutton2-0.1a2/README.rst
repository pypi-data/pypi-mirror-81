BigBlueButton™ API implementation for Python
============================================

Synopsis
--------

bigbluebutton2 is a sophisticated Python client library for BigBlueButton™
with Django integration.

This package implements tools for using the API of the
`BigBlueButton`_ web conferencing and online teaching software. In order to
broadly support the software in widespread python-based ecosystems, it
contains:

* an object-oriented library wrapping the `XML-RPC API`_
* a multi-server capable container that transparently wraps BigBlueButton
  server clusters, including load-balancing
* a command-line interface (CLI) tool to manage BigBlueButton (including
  clusters)
* an integration app for the `Django`_ web framework, including an
  API proxy view with multi-tenant/scoping support

The project serves as the core for `InfraBlue`_, the django-based material
design BigBlueButton frontend, and the conferencing integration in the
`AlekSIS`_ school information system.


Documentation
-------------

For an overview of all features of the different parts of
python-bigbluebutton2, as well as a complete API reference, please refer to
the `full documentation`_.


License
-------

This library is free and open software, licensed under the terms of the MIT
license. See the LICENSE file for details.


.. _BigBlueButton: https://bigbluebutton.org/
.. _XML-RPC API: https://docs.bigbluebutton.org/dev/api.html
.. _Django: https://www.djangoproject.com/
.. _InfraBlue: https://edugit.org/infrablue/infrablue
.. _AlekSIS: https://aleksis.org/
.. _full documentation: https://infrablue.edugit.io/python-bigbluebutton2/docs/html/
