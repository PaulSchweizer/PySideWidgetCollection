"""@package PySideWidgetCollection.framelesswidget.framelesswidget
@brief A scale button for the bottom right corner
@date 2014/11/20
@version 1.0
@author Paul Schweizer
@email paulschweizer@gmx.net
"""
from os import path
import webbrowser

from PySide import QtCore, QtGui

from PySideWidgetCollection import utility
__all__ = ['TitleBar', 'FramelessResizeWidget', 'ResizeButton']


class ResizeButton(QtGui.QPushButton):

    """A button to resize the frameless widget."""

    def __init__(self, parent=None):
        """Initialize internal attributes."""
        super(ResizeButton, self).__init__(parent=parent)
        self._mouse_pressed = False
        self._start_geo = None
        self._ui = self.parent().parent()
        self.setIcon(QtGui.QIcon(QtGui.QPixmap(path.join(path.dirname(__file__),
                                               'resource',
                                               'resize.png'))))
    # end def __init__

    def mousePressEvent(self, event):
        """Register mouse press and store the start geometry."""
        self._mouse_pressed = True
        self._start_geo = self._ui.geometry()
    # end def dragMoveEvent

    def mouseMoveEvent(self, event):
        """Resize the widget according to the mouse position."""
        if self._mouse_pressed:
            self._ui.setGeometry(self._start_geo.x(),
                                 self._start_geo.y(),
                                 event.globalPos().x() - self._start_geo.x(),
                                 event.globalPos().y() - self._start_geo.y())
        # end if
    # end def dragMoveEvent

    def mouseReleaseEvent(self, event):
        """De-register the mouse press."""
        self._mouse_pressed = False
    # end def mouseReleaseEvent
# end class ResizeButton


tb_base_class, tb_form_class = utility.load_ui_bases(__file__, 'TitleBar')


class TitleBar(tb_base_class, tb_form_class):

    """The title bar reproduces the behavior of a normal title bar.

    It is specifically designed for frame less widgets.
    """

    def __init__(self, parent=None, title='', help_url=''):
        """Initialize the title bar widget.

        @param parent The parent widget
        @param title The title
        @param help_url An optional url to a help page.
        """
        super(TitleBar, self).__init__(parent=parent)
        self.setupUi(self)
        self.help_url = help_url
        self.mouse_press_position = QtCore.QPoint()
        self.title_lbl.setText(title)
        self._collapsed = False
        self._stored_sizes = list()
    # end def __init__

    def mousePressEvent(self, event):
        """The mouse press event

        Captures the position of the press event, so the window can be
        moved relative to the cursor position.
        @param event the move event
        @return a standard mousePressEvent
        """
        self.mouse_press_position = event.pos()
        self.top_line_lbl.setStyleSheet('background-color:#4ca64f;')
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
        return QtGui.QWidget.mousePressEvent(self, event)
    # end def mousePressEvent

    def mouseMoveEvent(self, event):
        """Move the widget to the given location on the screen.

        @param event the move event
        @return a standard mouseMoveEvent
        """
        margins = self.parent().layout().contentsMargins()
        self.parent().move((event.globalPos().x()
                            - self.mouse_press_position.x()
                            - margins.left()),
                           (event.globalPos().y() + 6
                            - self.mouse_press_position.y()
                            - margins.right()))
        return QtGui.QWidget.mouseMoveEvent(self, event)
    # end def mousePressEvent

    def mouseReleaseEvent(self, event):
        """Reset the color of the top line on release."""
        self.top_line_lbl.setStyleSheet('background-color:#316b33;')
        QtGui.QApplication.restoreOverrideCursor()
        return QtGui.QWidget.mouseReleaseEvent(self, event)
    # end def mouseReleaseEvent

    def enterEvent(self, event):
        """Set the top line active."""
        self.top_line_lbl.setStyleSheet('background-color:#316b33;')
    # end def enterEvent

    def leaveEvent(self, event):
        """Set the top line inactive."""
        self.top_line_lbl.setStyleSheet('background-color:#656565;')
    # end def enterEvent

    def _show_help(self):
        """Show the help for this tool in the browser."""
        if self.help_url != '':
            webbrowser.open(self.help_url)
        # end if
    # end def _show_help

    def _minimize_parent_widget(self):
        """Minimize the parent widget."""
        self.parent().showMinimized()
    # end def _minimize_parent_widget

    def _close_parent_widget(self):
        """Close the parent widget."""
        self.parent().close()
    # end def _close_parent_widget
# end class TitleBar


frw_base_class, frw_form_class = utility.load_ui_bases(__file__,
                                                       'FramelessResizeWidget')


class FramelessResizeWidget(frw_base_class, frw_form_class):

    """A resize button on the bottom right corner of a frameless widget."""

    def __init__(self, parent=None, title=''):
        """Initialize the widget.

        @param parent the parent widget
        @param title the title
        """
        super(FramelessResizeWidget, self).__init__(parent=parent)
        self.setupUi(self)
    # end def __init__
# end class FramelessResizeWidget


def make_frameless(widget, help_url=''):
    """Convert the given widget into a frame less widget.

    Removes the window borders and adds the custom title bar widget
    to it.
    @param widget The widget
    @param help_url A url for the help button
    """
    widget.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
    widget.layout().insertWidget(0, TitleBar(widget,
                                             widget.windowTitle(),
                                             help_url))
    widget.layout().setContentsMargins(widget.layout().contentsMargins().left(),
                                       0,
                                       widget.layout().contentsMargins().right(),
                                       widget.layout().contentsMargins().bottom())
    widget.layout().addWidget(FramelessResizeWidget(widget,
                                                    widget.windowTitle()))
# end def make_frameless
