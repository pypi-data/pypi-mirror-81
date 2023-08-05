**qprof**
=========

**qprof** is a quantum profiler largely inspired by `gprof\
<https://ftp.gnu.org/old-gnu/Manuals/gprof-2.9.1/html_chapter/gprof_1.html#SEC1>`_.
It is a Python module distributed under the open-source (non-OSI but BSD compatible)
`CeCILL-B licence <https://cecill.info/licences/Licence_CeCILL-B_V1-en.html>`_.

*qprof* has been designed to output exactly the same text format as gprof in order to
be able to use the already existing tools designed for gprof.

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

The code has not been published on PyPi yet.


Usage
-----

Plugin organisation
~~~~~~~~~~~~~~~~~~~

The ``qprof`` library is organised as follow:

#. A main ``qprof`` library containing all the code related to computing routine
   execution time, the call graph, etc.
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

.. code:: python3

    # Import the qprof tools
    from qprof import profile
    from qprof.hardware.melbourne.gate_times import gate_times

    # Import the framework tools to generate a quantum routine
    from qat.lang.AQASM.routines import QRoutine
    from qat.lang.AQASM.gates import X, CNOT
    from qat.lang.AQASM.qftarith import add_const
    from qat.lang.AQASM.misc import build_gate

    # Generate the routine to benchmark.
    @build_gate("my_test_routine", [], arity=2)
    def my_test_routine() -> QRoutine:
        rout = QRoutine(arity=2)
        rout.apply(X, 1)
        rout.apply(CNOT, 1, 0)
        rout.apply(CNOT, 0, 1)
        rout.apply(CNOT, 1, 0)
        rout.apply(add_const(2, 1), [0, 1])
        return rout

    # Profile the resulting quantum routine
    qprof_out = profile(rout, gate_times, second_scale=10 ** 6)

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

If the problem is still present, open an issue. It may be an internal-routine that
is missing in the framework internal-routines adaption function or that is not wrapped
correctly.

``qprof2dot`` produce a call graph with all the routines taking 100% of the time
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This issue is usually caused by a non-adapted value for the optional parameter
``second_scale`` of the ``profile`` function. For small circuits, the self-time and
subroutine-time values are likely to be very small (of the order of the µs) but the
``gprof`` output format only has a precision of 10ms. This means that a routine taking less
than 5ms to execute will have a reported time of 0. If all the routines take less than
this threshold of 5ms, then ``gprof2dot`` will have no data to analyse (as all the
routines will have a written execution time of 0.00s) and will output a bad graph.

The solution is to set the parameter ``second_scale`` such that routines that takes
more than 5% of the total time have a written execution time of at least 1s.
Greater values of ``second_scale`` will improve the precision by avoiding round-offs.
