"""@package PySideWidgetCollection.utility
@brief Useful qt utility functions
@date 2014/11/20
@version 1.0
@author Paul Schweizer
@email paulschweizer@gmx.net
"""
import os
import urllib
from maya import OpenMayaUI
from PySide import QtCore, QtGui


def load_ui_type(ui_file):
    """Load a ui file for PySide.

    PySide lacks the "load_ui_type" command, so we have to convert
    the UI file to python code in-memory first and then execute it in a
    special frame to retrieve the form_class.
    """
    import xml.etree.ElementTree as xml
    from cStringIO import StringIO
    import pysideuic
    parsed = xml.parse(ui_file)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text
    with open(ui_file, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form_class based on their type
        # in the xml from designer
        base_class = eval('QtGui.%s' % widget_class)
        form_class = frame['Ui_%s' % form_class]
        return base_class, form_class
    # end reading the ui file
# end def load_ui_type


def wrapinstance(ptr, base=None):
    """Utility to convert a pointer to a Qt class instance.

    @param ptr long or Swig instance, Pointer to QObject in memory
    @param base QtGui.QWidget, (Optional) Base class to wrap with
                 (Defaults to QObject, which should handle anything)
    @return QWidget or subclass instance
    """
    import shiboken
    if ptr is None:
        return None
    # end if
    ptr = long(ptr)
    if base is None:
        qObj = shiboken.wrapInstance(long(ptr), QtCore.QObject)
        metaObj = qObj.metaObject()
        cls = metaObj.className()
        superCls = metaObj.superClass().className()
        if hasattr(QtGui, cls):
            base = getattr(QtGui, cls)
        elif hasattr(QtGui, superCls):
            base = getattr(QtGui, superCls)
        else:
            base = QtGui.QWidget
        # end if
    # end if
    return shiboken.wrapInstance(long(ptr), base)
# end def wrapinstance


def get_cpp_pointer(widget):
    """Convert the cpp pointer of the given widget.

    @param widget the widget
    @return the cpp pointer
    """
    import shiboken
    return long(shiboken.getCppPointer(widget)[0])
# end def get_cpp_pointer


def get_ui_file_path(widget_file, widget_name):
    """Retrieve the ui file for the given widget.

    It is assumed that it is set up inside the standardized
    resource folder.
    @param widget_file the file of the widget
    @param widget_name the name of the widget
    @return the file path for the ui file
    """
    return os.path.join(os.path.dirname(widget_file),
                        'resource', '%s.ui' % widget_name)
# end def get_ui_file_path


def load_ui_bases(widget_file, widget_name):
    """Load the ui base classes.

    @param widget_file the file of the widget
    @param widget_name the name of the widget
    @return the base classes for the ui
    """
    return load_ui_type(get_ui_file_path(widget_file, widget_name))
# end def load_ui_bases
