"""@package PySideWidgetCollection.notifier.notifier
@brief Notifier Widget, that hides itself in the tray bar
@date 2014/08/20
@version 1.0
@author Paul Schweizer
@email pschweizer@gmx.net
"""
import os

from PySide import QtCore, QtGui

from PySideWidgetCollection import utility
__all__ = ['NotifierTrayIcon', 'Notifier']


class NotifierTrayIcon(QtGui.QSystemTrayIcon):

    """The Icon for the Notifier."""

    def __init__(self, icon, parent=None):
        """Add an exit button to the menu."""
        super(NotifierTrayIcon, self).__init__(icon, parent)
        menu = QtGui.QMenu(parent)
        self.exit_action = menu.addAction('Exit')
        self.setContextMenu(menu)
    # end def __init__
# end class NotifierTrayIcon


form_class, base_class = utility.load_ui_bases(__file__, 'Notifier')


class Notifier(base_class, form_class):

    """A Widget blueprint for pop-up tray notifications.

    It collapses to a tray icon and pops up at a position near
    the tray icon.
    """

    def __init__(self):
        """Setup the tray icon and signals."""
        super(Notifier, self).__init__()
        self.setupUi(self)
        self.width = 150
        self.height = 100
        self._init_tray_icon()
        self._close_action = False
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
    # end def __init__

    def _init_tray_icon(self):
        """Initialize the tray icon."""
        icon = os.path.join(os.path.dirname(__file__),
                            'resource', 'Notifier.png')
        icon = QtGui.QIcon(QtGui.QPixmap(icon))
        self.system_tray_icon = NotifierTrayIcon(icon, self)
        self.system_tray_icon.setVisible(True)
        self.system_tray_icon.setToolTip('Notifier')
        self.system_tray_icon.activated.connect(self._tray_icon_activated)
        self.system_tray_icon.exit_action.triggered.connect(self._exit)
    # end def _tray_icon

    def _tray_icon_activated(self, reason):
        """Show/hide the Widget when the icon is double clicked.

        @param reason The reason for the activation
        """
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()
            # end if
        # end if
    # end def _tray_icon_activated

    def _exit(self):
        """Close the Notifier."""
        self._close_action = True
        self.close()
    # end def _exit

    def show(self):
        """Show the Notifier."""
        # Calculate the position
        trayicon_geo = self.system_tray_icon.geometry()
        avaibable_geo = (QtGui.QApplication.instance().desktop()
                         .availableGeometry())
        x = (trayicon_geo.x() +
             avaibable_geo.x() +
             trayicon_geo.width() -
             self.width)
        y = avaibable_geo.height() - self.height - 30
        self.setGeometry(x, y, self.width, self.height)
        QtGui.QWidget.show(self)
    # end def show

    def closeEvent(self, event):
        """Minimize the Notifier instead of closing it.

        If the close action has been triggered, the Notifier is
        actually closed.
        @param event The event
        """
        if self._close_action:
            event.accept()
            return QtGui.QWidget.closeEvent(self, event)
        # end if
        event.ignore()
        self.hide()
        self.system_tray_icon.showMessage('Notifier minimized',
                                          'Still running in the background')
    # end def closeEvent
# end class Notifier
