.. highlight:: shell

============
Installation
============


Stable release
--------------

To install taperable-helix, run this command in your terminal:

.. prompt:: bash

   pip install taperable-helix

This is the preferred method to install taperable-helix, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

Test release from testpypi
--------------------------

To install taperable-helix from testpypi, run this command in your terminal:

.. prompt:: bash

   pip install --index-url https://test.pypi.org/simple/ taperable-helix

From sources
------------

The sources for taperable_helix can be downloaded from the `Github repo`_.

  You can either clone the public repository:

.. prompt:: bash

   git clone git://github.com/winksaville/py-taperable-helix taperable-helix
   cd taperable-helix

Or download the tarball
  
.. prompt:: bash
   :substitutions:
  
   curl -OJL https://github.com/winksaville/py-taperable-helix/releases/v|ver|.tar.gz

Once you have a copy of the source, you can install it with:

.. prompt:: bash

   python setup.py install

Or if you want to install in editable mode for development:

.. prompt:: bash

   make install-dev

.. prompt:: bash

   pip install -e . -r dev-requirements.txt

Uninstall
---------

.. prompt:: bash

   pip uninstall taperable-helix


.. _Github repo: https://github.com/winksaville/taperable_helix
.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/
