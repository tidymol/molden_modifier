Installing the molden modifier
==============================

.. note::
   This is a python3 only package.


Pip
---

For Python 3:

.. code-block:: bash

    pip3 install molden-modifier


Linux Distributions
-------------------

Fedora
^^^^^^

.. code-block:: bash

    $ dnf install python3-molden-modifier


openSUSE
^^^^^^^^

1. Enable the ``jloehel:python`` repository of the Open Build Service::

    $ sudo zypper addrepo --refresh obs://jloehel:python jloehel_python

2. Install the package::

    $ sudo zypper install --repo jloehel_python molden_modifier
