# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Compatibility layer for Qt bindings, so it is easier to switch from PyQt4 to PyQt5 and
vice-versa. It is possible to add PySide if needed.
For PyQt4 and PyQt5 differences please see http://pyqt.sourceforge.net/Docs/PyQt5/pyqt4_differences.html
"""

# based on https://gist.github.com/remram44/5985681 and
# https://github.com/pyQode/pyqode.qt/blob/master/pyqode/qt/QtWidgets.py (MIT license)


import sys
import sip
import os

import logging
log = logging.getLogger(__name__)


if os.environ.get('GNS3_QT4', None) is not None:
    DEFAULT_BINDING = 'PyQt4'
    print("WARNING: PyQt4 is no longer supported, please upgrade to PyQt5")
else:
    try:
        import PyQt5
        DEFAULT_BINDING = 'PyQt5'
    except ImportError:
        DEFAULT_BINDING = 'PyQt4'
        print("WARNING: PyQt4 is no longer supported, please upgrade to PyQt5")

if DEFAULT_BINDING == 'PyQt5':

    from PyQt5 import QtCore, QtGui, QtNetwork, QtWidgets, Qt
    sys.modules[__name__ + '.QtCore'] = QtCore
    sys.modules[__name__ + '.QtGui'] = QtGui
    sys.modules[__name__ + '.QtNetwork'] = QtNetwork
    sys.modules[__name__ + '.QtWidgets'] = QtWidgets

    try:
        from PyQt5 import QtSvg
        sys.modules[__name__ + '.QtSvg'] = QtSvg
    except ImportError:
        raise SystemExit("Please install the PyQt5.QtSvg module")

    try:
        from PyQt5 import QtWebKit
        from PyQt5 import QtWebKitWidgets
        sys.modules[__name__ + '.QtWebKit'] = QtWebKit
        sys.modules[__name__ + '.QtWebKitWidgets'] = QtWebKitWidgets
    except ImportError:
        pass

    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.Property = QtCore.pyqtProperty
    QtCore.BINDING_VERSION_STR = QtCore.PYQT_VERSION_STR

    from PyQt5.QtWidgets import QFileDialog as OldFileDialog

    class QFileDialog(OldFileDialog):

        @staticmethod
        def getExistingDirectory(parent=None, caption='', dir='', options=OldFileDialog.ShowDirsOnly):
            path = OldFileDialog.getExistingDirectory(parent, caption, dir, options)
            if path:
                path = os.path.normpath(path)
            return path

        @staticmethod
        def getOpenFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getOpenFileName(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

        @staticmethod
        def getOpenFileNames(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getOpenFileNames(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

        @staticmethod
        def getSaveFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getSaveFileName(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

    QtWidgets.QFileDialog = QFileDialog

    def translate(*args):
        return QtCore.QCoreApplication.translate(*args)

elif DEFAULT_BINDING == 'PyQt4':

    sip.setapi('QDate', 2)
    sip.setapi('QDateTime', 2)
    sip.setapi('QString', 2)
    sip.setapi('QTextStream', 2)
    sip.setapi('QTime', 2)
    sip.setapi('QUrl', 2)
    sip.setapi('QVariant', 2)

    from PyQt4 import QtCore, QtGui, QtNetwork, QtSvg, Qt
    sys.modules[__name__ + '.QtCore'] = QtCore
    sys.modules[__name__ + '.QtGui'] = QtGui
    sys.modules[__name__ + '.QtNetwork'] = QtNetwork
    sys.modules[__name__ + '.QtSvg'] = QtSvg

    try:
        from PyQt4 import QtWebKit
        sys.modules[__name__ + '.QtWebKit'] = QtWebKit
        # Qt5 name compatibility
        QtWebKitWidgets = QtWebKit
    except ImportError:
        pass

    QtCore.Signal = QtCore.pyqtSignal
    QtCore.Slot = QtCore.pyqtSlot
    QtCore.Property = QtCore.pyqtProperty
    QtCore.BINDING_VERSION_STR = QtCore.PYQT_VERSION_STR

    # Qt5 name compatibility
    QtWidgets = QtGui

    from PyQt4.QtGui import QFileDialog as OldFileDialog

    class QFileDialog(OldFileDialog):

        @staticmethod
        def getExistingDirectory(parent=None, caption='', dir='', options=OldFileDialog.ShowDirsOnly):
            path = OldFileDialog.getExistingDirectory(parent, caption, dir, options)
            if path:
                path = os.path.normpath(path)
            return path

        @staticmethod
        def getOpenFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getOpenFileNameAndFilter(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

        @staticmethod
        def getOpenFileNames(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getOpenFileNamesAndFilter(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

        @staticmethod
        def getSaveFileName(parent=None, caption='', directory='', filter='', selectedFilter='', options=OldFileDialog.Options()):
            path, _ = OldFileDialog.getSaveFileNameAndFilter(parent, caption, directory, filter, selectedFilter, options)
            if path:
                path = os.path.normpath(path)
            return path, _

    QtWidgets.QFileDialog = QFileDialog

    # QStandardPaths replace QDesktopServices in QT5
    class QStandardPaths:
        DocumentsLocation = QtGui.QDesktopServices.DocumentsLocation
        PicturesLocation = QtGui.QDesktopServices.PicturesLocation

        def writableLocation(path_type):
            return QtGui.QDesktopServices.storageLocation(path_type)

    QtCore.QStandardPaths = QStandardPaths

    # Translate not working well when reading a PyQT5 ui file (unicode issues)
    # we turn off translation for PyQT4
    def translate(*args):
        return ''.join(args[-1:])


# If we run from a test we replace the signal by a synchronous version
if hasattr(sys, '_called_from_test'):
    class FakeQtSignal:
        _instances = set()

        def __init__(self, *args):
            self._callbacks = set()
            self._instances.add(self)

        def connect(self, func):
            log.debug("{caller} connect to signal".format(caller=sys._getframe(1).f_code.co_name))
            self._callbacks.add(func)

        def disconnect(self, func):
            self._callbacks.remove(func)

        def emit(self, *args):
            log.debug("{caller} emit signal".format(caller=sys._getframe(1).f_code.co_name))
            for callback in list(self._callbacks):
                callback(*args)

        @classmethod
        def reset(cls):
            """Use to clean the listening signals between tests"""
            for instance in cls._instances:
                instance._callbacks = set()

    QtCore.Signal = FakeQtSignal
    QtCore.pyqtSignal = FakeQtSignal
