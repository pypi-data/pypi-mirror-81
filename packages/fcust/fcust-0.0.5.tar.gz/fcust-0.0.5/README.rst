================
Folder Custodian
================


.. image:: https://img.shields.io/pypi/v/fcust.svg
        :target: https://pypi.python.org/pypi/fcust

.. image:: https://img.shields.io/travis/Iolaum/fcust.svg
        :target: https://travis-ci.com/Iolaum/fcust

.. image:: https://readthedocs.org/projects/fcust/badge/?version=latest
        :target: https://fcust.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/Iolaum/fcust/shield.svg
     :target: https://pyup.io/repos/github/Iolaum/fcust/
     :alt: Updates



Linux Common Folder Custodian


* Free software: GNU General Public License v3
* Documentation: https://fcust.readthedocs.io.



Features
--------

This package is intended to perform maintenance over a folder shared across many users in a Fedora Workstation.
The folder belongs to a group for which all users are members.

* Go through a folder's content and enforce common group ownership.
* Go through a folder's content and enforce common group read and write permissions as
  well as set groupid sticky bit.
* Provide a command line command with sane defaults for enforcing common folder group ownership
  and permissions.
* (TODO) Write logs to ``/tmp/fcust``.
* (TODO) Provide user systemd service to periodically enforce common folder group ownership
  and permissions.

The key problem this package intends to solve is that files moved from one location to another do not inherit
proper permissions in the commonly used folder and therefore when another user tries to access them they encounter
problems.

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
