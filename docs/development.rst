Development
===========

The main GitHub repository for the project can be found at:

    https://github.com/TheCellule/python-bleson

It's strongly recommended to update your tools:

.. code-block:: console

    pip3 install --upgrade pip setuptools wheel twine



Building the docs
-----------------

Build the documentation:

.. code-block:: console

    python3 setup.py doc


Build the documentation and run the doctests:

.. code-block:: console

    python3 setup.py doctest


Test suite
----------

.. code-block:: console

    python3 setup.py test


Release to PyPi
---------------

A CI integration takes care of testing and then publishing to PyPi, all you need todo is

+ merge the changes into master,
+ bump `bleson/VERSION`,
+ `git add`
+ `git commit`
+ run:

.. code-block:: console

    python3 setup.py tag
