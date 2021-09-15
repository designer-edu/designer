-----------------------
How to Install Designer
-----------------------

======
Thonny
======

Designer can be installed through the Integrated Development Environment (IDE) Thonny_ in two ways:

1. Through the `Thonny package manager`_
    - Open the package manager through *Tools* -> *Manage packages*
    - Type in the search bar for "designer"
    - Press "Find packages from PyPI"
    - Designer should be loaded from the search. Press "Install".

**OR:**

2. Through the `Thonny system shell`_
    - Open the Thonny system shell through *Tools* -> *Open system shell*
    - Type ``pip install designer``

To make sure that Designer has been successfully installed, open a new Python (.py) file.

Type ``from designer import *``.

If this line of code runs without error, Designer has been successfully installed!

**Next:**

Check out Designer quick start :ref:`quickstart`.

============
Command Line
============
Designer can also be installed straight from the command line through ``pip install designer``.

It can also be installed on a `Python virtual environment`_.

**Next:**

Check out Designer quick start :ref:`quickstart`.

.. _Thonny: https://thonny.org/
.. _Thonny system shell: https://thonny.org/#:~:text=Beginner%20friendly%20system%20shell.%20Select%20Tools%20%E2%86%92%20Open%20system%20shell%20to%20install%20extra%20packages%20or%20learn%20handling%20Python%20on%20command%20line.%20PATH%20and%20conflicts%20with%20other%20Python%20interpreters%20are%20taken%20care%20of%20by%20Thonny.
.. _Thonny package manager: https://thonny.org/#:~:text=Simple%20and%20clean%20pip%20GUI.%20Select%20Tools%20%E2%86%92%20Manage%20packages%20for%20even%20easier%20installation%20of%203rd%20party%20packages.
.. _Python virtual environment: https://realpython.com/python-virtual-environments-a-primer/
