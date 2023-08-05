""" The main initialization of our PySide2/PyQt5 Package.

    Warning:
        This module tries to import PySide2 if available,
        otherwise defaults to PyQt5 for the GUI.

    :Author:
        - 2009-2011 Nicola Creati
        - 2009-2020 Roberto Vidmar

    :Copyright: 2011-2020
              Nicola Creati <ncreati@inogs.it>
              Roberto Vidmar <rvidmar@inogs.it>

    :License: MIT/X11 License (see :download:`license.txt
                               <../../license.txt>`)
"""
import os

PREFER_PYQT5 = os.environ.get('PREFER_PYQT5')
if PREFER_PYQT5:
    try:
        import PyQt5.QtCore as _QtCore
        import PyQt5.QtGui as _QtGui
        import PyQt5.QtWidgets as _QtWidgets
    except ImportError:
        LIB = None
    else:
        LIB = "PyQt5"
else:
    try:
        import PySide2.QtCore as _QtCore
        import PySide2.QtGui as _QtGui
        import PySide2.QtWidgets as _QtWidgets
    except ImportError:
        LIB = None
    else:
        LIB = "PySide2"

if LIB is None:
    if PREFER_PYQT5:
        raise SystemExit("\nERROR! Preferred PyQt5 library not available!\n"
                "Please install it before retrying.")
    else:
        raise SystemExit("\nERROR! Neither PySide2 nor PyQt5 libraries"
                " available!\n"
                "Please install one of them before retrying.")

QtWidgets = _QtWidgets
QtCore = _QtCore
QtGui = _QtGui

if LIB == "PySide2":
    Signal = QtCore.Signal
    Slot = QtCore.Slot
    Property = QtCore.Property

    def getOpenFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileName(*args,
                **kargs)
        return pn

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getOpenFileNames
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getOpenFileNames(*args,
                **kargs)
        return pn

    def getSaveFileName(*args, **kargs):
        """ Wrap to PySide QtWidgets.QFileDialog.getSaveFileName
        """
        pn, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(*args,
                **kargs)
        return pn
else:
    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    Property = QtCore.pyqtProperty

    def getOpenFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileName
        """
        return QtWidgets.QFileDialog.getOpenFileName(*args, **kargs)

    def getOpenFileNames(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getOpenFileNames
        """
        return QtWidgets.QFileDialog.getOpenFileNames(*args, **kargs)

    def getSaveFileName(*args, **kargs):
        """ Wrap to PyQt4 QtWidgets.QFileDialog.getSaveFileName
        """
        return QtWidgets.QFileDialog.getSaveFileName(*args, **kargs)

    QtCore.pyqtRemoveInputHook()

Qt = QtCore.Qt
