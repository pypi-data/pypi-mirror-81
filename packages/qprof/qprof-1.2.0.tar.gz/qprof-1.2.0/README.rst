**qprof**
=========

**qprof** stands for **q**\ uantum **prof**\ iler and aims at providing a
unique tool to profile quantum circuits.

Installation
------------

*qprof* being a Python module, it is installable with ``pip``.

From Gitlab
~~~~~~~~~~~

.. code:: bash

   git clone https://gitlab.com/qcomputing/qprof/qprof.git
   pip install qprof/

From PyPi
~~~~~~~~~

*qprof* is now available on PyPi! To download and install the last version, just
type

.. code:: bash

   pip install qprof

Plugins for library support are not installed by default in order to avoid pulling
silently huge dependencies like qiskit in your project. In order to install the plugins
you can either do it afterwards with pip:

.. code:: bash

   pip install qprof_qiskit  # replace "qiskit" by your library

or use the appropriate target when installing qprof:

.. code:: bash

   pip install qprof[qiskit]
   pip install qprof[myqlm]
   pip install qprof[all_plugin]

For developers
~~~~~~~~~~~~~~

Developers might want to install *qprof* as an editable project.
To do so you need to clone the git repository and install the library in
editable mode with the `-e` option:

.. code:: bash

   git clone https://gitlab.com/qcomputing/qprof/qprof.git
   pip install -e qprof/

Note that the dependencies will **not** be installed in editable mode. If you want
all the *qprof* stack in editable mode, you need to clone and install everything
"by hand":

.. code:: bash

   git clone https://gitlab.com/qcomputing/qprof/qprof.git
   git clone https://gitlab.com/qcomputing/qprof/qprof_interfaces.git
   # Plugins?
   # git clone https://gitlab.com/qcomputing/qprof/qprof_qiskit.git
   pip install -e qprof_interfaces/
   pip install -e qprof/
   # Plugins?
   # pip install -e qprof_qiskit/

Usage
-----

Plugin organisation
~~~~~~~~~~~~~~~~~~~

The ``qprof`` library is organised as follow:

#. A main ``qprof`` library containing all the code related to computing routine
   execution time, call graph, exporting, ...
#. A ``qprof_interfaces`` plugin providing interfaces for the data structures used
   by ``qprof`` to communicate with the plugins.
#. Several ``qprof_XXX`` libraries that are used to adapt a library ``XXX`` to
   ``qprof`` by implementing the interfaces of ``qprof_interfaces``.

Plugins are automatically discovered the first time ``qprof.frameworks`` is imported
and are arranged in a dictionary-like data-structure with the following structure:

.. code:: python

    frameworks = {
        "interfaces": <module 'qprof_interfaces' from '[path]'>, # always present
        "plugin1": <module 'qprof_plugin1' from '[path]'>,
        # ...
        "pluginN": <module 'qprof_pluginN' from '[path]'>,
    }

Plugins are lazy-imported, meaning that the plugin module is imported at the
first access to the dictionary key.

Profiling
~~~~~~~~~

The profiling is performed with the ``qprof.profile`` function.

The ``qprof.profile`` function needs a quantum routine implemented with one of the
supported frameworks along with the "base" gate times provided as a dictionary.

Example of profiling:

.. code:: python

    # Import the qprof tools
    from qprof import profile

    # Import the framework tools to generate a quantum routine
    from qiskit.aqua.algorithms import Grover
    from qiskit.aqua.components.oracles import LogicalExpressionOracle


    # Generate the routine to benchmark.
    input_3sat = """
    c example DIMACS-CNF 3-SAT
    p cnf 3 5
    -1 -2 -3 0
    1 -2 3 0
    1 2 -3 0
    1 -2 -3 0
    -1 2 3 0
    """

    oracle = LogicalExpressionOracle(input_3sat)
    grover = Grover(oracle)

    # Hard-coded gate times retrieved by hand
    gate_times = {"U1": 0, "U2": 89, "U3": 178, "CX": 930, "BARRIER": 0}

    # Profile the resulting quantum routine and use the "gprof" exporter
    qprof_out = profile(rout, gate_times, "gprof")

    # Print to stdout the analysis report
    print(qprof_out)

Full profiling example
----------------------

Requirements for the example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You should have the ``dot`` tool installed on your machine, along with the
`gprof2dot <https://github.com/jrfonseca/gprof2dot>`_ tool that can be installed
with ``pip install gprof2dot``.

Profile the code
~~~~~~~~~~~~~~~~

Let save the code of the previous section in a file `profile.py`.

You can generate the following graph with the command

.. code:: bash

    python3 profile.py | gprof2dot | dot -Tpng -o profiling_result.png

.. image:: docs/images/profile_result.png


Limitations
-----------

* *qprof* is not able to analyse recursive routine calls yet. If your quantum circuit
  contains calls to recursive routines, expect the unexpected.

Troubleshooting
---------------

"Unknown" routines shows up in reports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If "Unknown" routines are showing up in the reports, check that you named
correctly all the routines you defined.

If the problem is still present, open an issue.
