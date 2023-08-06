Changelog
=========

1.1.1rc5 (2020-09-30)
---------------------
- Drop support for Python 3.5.

1.1.1rc2 (2020-09-22)
---------------------
- Setup general update and cleanup.
- Setup: fix an improper dependencies versions.

1.1.0rc9 (2019-11-13)
---------------------
- | Requirements upgrade:
  | PySide2 to at least 5.13.2
  | PyQt5   to at least 5.13.2
- Setup updates and cleanup.

1.1.0rc7 (2019-10-29)
---------------------
- | Requirements upgrade:
  | PySide2 to at least 5.13.1
  | PyQt5   to at least 5.13.1
- Adding of (for now fake/empty) test case.
- Setup updates and cleanup.

1.1.0rc2 (2019-08-02)
---------------------
- StreamEmitter class added.

1.1.0rc1 (2019-07-23)
---------------------
- | Requirements upgrade:
  | QtPy    to at least 1.9.0
  | PySide2 to at least 5.13.0
  | PyQt5   to at least 5.13.0
  | This allows to have applications that import PySide2 and PyQt5 at the same time
  | (which is possible if both bindings are compiled for the same Qt version).

1.0.0b5 (2019-06-10)
--------------------
- Adding setup extras PySide and PyQt for installing PySide2 or PyQt5 backends.

1.0.0b4 (2019-06-06)
--------------------
- Fix a bug for PySide2 as backend.

1.0.0b3 (2019-06-04)
--------------------
- Adding a monkey-patch for vtk.qt (vtk==8.1.x).

1.0.0b2 (2019-05-22)
--------------------
- Fixes and cleanup of setup.

1.0.0b1 (2019-05-22)
--------------------
- First public release.

0.0.1a1 (2012-03-9)
-------------------
- Initial version.
