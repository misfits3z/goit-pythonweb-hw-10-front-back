REST API ContacTs Documentation
===============================

This is the main documentation for the Contacts REST API project.

Add your content using ``reStructuredText`` syntax. See the
`reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
documentation for details.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

API Layer
=========

API Auth
--------
.. automodule:: src.api.auth_router
   :members:
   :show-inheritance:

API Contacts
------------
.. automodule:: src.api.contacts
   :members:
   :show-inheritance:

API Admin
---------
.. automodule:: src.api.create_admin
   :members:
   :show-inheritance:

API Users
---------
.. automodule:: src.api.users
   :members:
   :show-inheritance:

API Utils
---------
.. automodule:: src.api.utils
   :members:
   :show-inheritance:

Main Application
================
.. automodule:: main
   :members:
   :undoc-members:
   :show-inheritance:

Config Layer
============

Config
------
.. automodule:: src.conf.config
   :members:
   :show-inheritance:

Core Layer
==========

Core Redis Client
-----------------
.. automodule:: src.core.redis_client
   :members:
   :show-inheritance:

Database Layer
==============

Database Models
---------------
.. automodule:: src.database.models
   :members:
   :show-inheritance:

Database Session Manager
------------------------
.. automodule:: src.database.db
   :members:
   :show-inheritance:

Database Seeder
---------------
.. automodule:: src.database.seed_contacts
   :members:
   :show-inheritance:

Repository Layer
================

Repository Contacts
-------------------
.. automodule:: src.repository.contacts
   :members:
   :undoc-members:
   :show-inheritance:

Repository Users
----------------
.. automodule:: src.repository.users
   :members:
   :undoc-members:
   :show-inheritance:

Services Layer
==============

Auth Service
------------
.. automodule:: src.services.auth
   :members:
   :show-inheritance:

Contacts Service
----------------
.. automodule:: src.services.contacts
   :members:
   :show-inheritance:

Users Service
-------------
.. automodule:: src.services.users
   :members:
   :show-inheritance:

Utils Layer
===========

Token Utilities
---------------
.. automodule:: src.utils.tokens
   :members:
   :show-inheritance:

Pydantic Schemas
================

Schemas
-------
.. automodule:: src.schemas
   :members:
   :show-inheritance:

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`