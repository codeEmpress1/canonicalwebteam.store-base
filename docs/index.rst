.. :relatedlinks: [Diátaxis](https://diataxis.fr/)

.. _home:

Store Base
============

This is the base application that serves as a building block for all stores. It is available as a module on PyPI, and is installed in the virtual environment of each store.

Store-base is a flask application that allows common configurations, dependencies, logic and  endpoints to be shared across all webteam's stores. It provides a common structure for all stores which enhances uniformity, scalabilty and maintainability of stores. It also allows easy creation of new stores and faster update of existing stores. Each store is a separate Flask app that inherits from this base app. 

Individual stores are registered as blueprints  after initialization of the base app. After which store-specific configurations are defined. 

---------

In this documentation
---------------------

..  grid:: 1 1 2 2

   
   ..  grid-item:: :doc:`Development <development/index>`

      **Step-by-step guides** covering key operations and common tasks

   ..  grid-item:: :doc:`Tutorial <tutorial/index>`

       An introduction to Store-base


---------

Project and community
---------------------

Store base is a developed and maintained by Canonical webteam. It’s an open source project that warmly welcomes community projects, contributions, suggestions, fixes and constructive feedback.

.. * :ref:`Code of conduct <home>`
.. * :ref:`Get support <home>`
.. * :ref:`Join our online chat <home>`
.. * :ref:`Contribute <home>`
.. * :ref:`Roadmap <home>`
.. * :ref:`Thinking about using Example Product for your next project? Get in touch! <home>`


.. toctree::
   :hidden:
   :maxdepth: 2

   development/index
   tutorial/index
