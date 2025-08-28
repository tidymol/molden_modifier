Using molden-modifier
=====================

Extract basic information about the molden file
-----------------------------------------------
::

    molden-modifier info data.molden

Applying filters on a molden file
---------------------------------
::

    molden-modifier filter -f ???  test.molden



Sort the molecules in a molden file
-----------------------------------
::

    molden-modifier sort test.molden


Creating mirrors of molecules
-----------------------------
::

    molden-modifier mirror test.molden


Find the shortest distance between selected pairs of atoms
----------------------------------------------------------
::

    molden-modifier shortest_distance test.molden
