Change log
================================================================================

0.6.0 - 8.10.2020
--------------------------------------------------------------------------------

**added**

#. new style reader and writer plugins. works with pyexcel-io v0.6.2

0.5.3 - 27.11.2018
--------------------------------------------------------------------------------

**added**

#. `pyexcel#57 <https://github.com/pyexcel/pyexcel/issues/57>`_, long type will
   not be written in ods. please use string type. And if the integer is equal or
   greater than 10 to the power of 16, it will not be written either in ods. In
   both situation, IntegerPrecisionLossError will be raised.

0.5.2 - 23.10.2017
--------------------------------------------------------------------------------

**updated**

#. pyexcel `pyexcel#105 <https://github.com/pyexcel/pyexcel/issues/105>`_,
   remove gease from setup_requires, introduced by 0.5.1.
#. remove python2.6 test support
#. update its dependecy on pyexcel-io to 0.5.3

0.5.1 - 20.10.2017
--------------------------------------------------------------------------------

**added**

#. `pyexcel#103 <https://github.com/pyexcel/pyexcel/issues/103>`_, include
   LICENSE file in MANIFEST.in, meaning LICENSE file will appear in the released
   tar ball.

0.5.0 - 30.08.2017
--------------------------------------------------------------------------------

**Updated**

#. put dependency on pyexcel-io 0.5.0, which uses cStringIO instead of StringIO.
   Hence, there will be performance boost in handling files in memory.

**Relocated**

#. All ods type conversion code lives in pyexcel_io.service module

0.4.1 - 17.08.2017
--------------------------------------------------------------------------------

**Updated**

#. update dependency to use pyexcel-ezodf v0.3.3 as ezodf 0.3.2 has `the bug
   <https://github.com/pyexcel/pyexcel-ezodf/issues/1>`_, cannot handle file
   alike objects and has not been updated for 2 years.

0.4.0 - 19.06.2017
--------------------------------------------------------------------------------

**Updated**

#. `pyexcel#14 <https://github.com/pyexcel/pyexcel/issues/14>`_, close file
   handle
#. pyexcel-io plugin interface now updated to use `lml
   <https://github.com/chfw/lml>`_.

0.3.2 - 13.04.2017
--------------------------------------------------------------------------------

**Updated**

#. issue `pyexcel#8 <https://github.com/pyexcel/pyexcel/issues/8>`_,
   PT288H00M00S is valid duration

0.3.1 - 02.02.2017
--------------------------------------------------------------------------------

**Added**

#. Recognize currency type

0.3.0 - 22.12.2016
--------------------------------------------------------------------------------

**Updated**

#. Code refactoring with pyexcel-io v 0.3.0

0.2.2 - 05.11.2016
--------------------------------------------------------------------------------

**Updated**

#. `pyexcel#11 <https://github.com/pyexcel/pyexcel/issues/11>`_, be able to
   consume a generator of two dimensional arrays.

0.2.1 - 31.08.2016
--------------------------------------------------------------------------------

**Added**

#. support pagination. two pairs: start_row, row_limit and start_column,
   column_limit help you deal with large files.

0.2.0 - 01.06.2016
--------------------------------------------------------------------------------

**Added**

#. By default, `float` will be converted to `int` where fits. `auto_detect_int`,
   a flag to switch off the autoatic conversion from `float` to `int`.
#. 'library=pyexcel-ods3' was added so as to inform pyexcel to use it instead of
   other libraries, in the situation where multiple plugins for the same file
   type are installed

**Updated**

#. support the auto-import feature of pyexcel-io 0.2.0
#. compatibility with pyexcel-io 0.1.0

0.1.0 - 17.01.2016
--------------------------------------------------------------------------------

**Updated**

#. support the auto-import feature of pyexcel-io 0.2.0
#. compatibility with pyexcel-io 0.1.0
