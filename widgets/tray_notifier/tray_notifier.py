"""Notifier Widget, that hides itself in the tray bar."""
import os

from Qt import QtCore, QtWidgets

from widgets import utility
__all__ = ['NotifierTrayIcon', 'TrayNotifier']


class NotifierTrayIcon(QtWidgets.QSystemTrayIcon):
    """The Icon for the TrayNotifier."""

    def __init__(self, icon, parent=None):
        """Add an exit button to the menu."""
        super(NotifierTrayIcon, self).__init__(icon, parent)
        menu = QtWidgets.QMenu(parent)
        self.exit_action = menu.addAction('Exit')
        self.setContextMenu(menu)
    # end def __init__
# end class NotifierTrayIcon


class TrayNotifier(utility.ui_class(__file__, 'TrayNotifier')):
    """A Widget blueprint for pop-up tray notifications.

    It collapses to a tray icon and pops up at a position near
    the tray icon.
    """

    def __init__(self):
        """Setup the tray icon and signals."""
        super(TrayNotifier, self).__init__()
        self.setupUi(self)
        self.width = 150
        self.height = 100
        self._init_tray_icon()
        self._close_action = False
        self.setWindowFlags(QtCore.Qt.Widget |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)
    # end def __init__

    def _init_tray_icon(self):
        """Initialize the tray icon."""
        icon = os.path.join(os.path.dirname(__file__),
                            'resource', 'TrayNotifier.png')
        icon = QtWidgets.QIcon(QtWidgets.QPixmap(icon))
        self.system_tray_icon = NotifierTrayIcon(icon, self)
        self.system_tray_icon.setVisible(True)
        self.system_tray_icon.setToolTip('TrayNotifier')
        self.system_tray_icon.activated.connect(self._tray_icon_activated)
        self.system_tray_icon.exit_action.triggered.connect(self._exit)
    # end def _tray_icon

    def _tray_icon_activated(self, reason):
        """Show/hide the Widget when the icon is double clicked.

        @param reason The reason for the activation
        """
        if reason == QtWidgets.QSystemTrayIcon.DoubleClick:
            if self.isHidden():
                self.show()
            else:
                self.hide()
            # end if
        # end if
    # end def _tray_icon_activated

    def _exit(self):
        """Close the TrayNotifier."""
        self._close_action = True
        self.close()
    # end def _exit

    def show(self):
        """Show the TrayNotifier."""
        trayicon_geo = self.system_tray_icon.geometry()
        avaibable_geo = (QtWidgets.QApplication.instance().desktop()
                         .availableGeometry())
        x = (trayicon_geo.x() +
             avaibable_geo.x() +
             trayicon_geo.width() -
             self.width)
        y = avaibable_geo.height() - self.height - 30
        self.setGeometry(x, y, self.width, self.height)
        QtWidgets.QWidget.show(self)
    # end def show

    def closeEvent(self, event):
        """Minimize the TrayNotifier instead of closing it.

        If the close action has been triggered, the TrayNotifier is
        actually closed.
        @param event The event
        """
        if self._close_action:
            event.accept()
            return QtWidgets.QWidget.closeEvent(self, event)
        # end if
        event.ignore()
        self.hide()
        self.system_tray_icon.showMessage('TrayNotifier minimized')
    # end def closeEvent
# end class TrayNotifier


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = TrayNotifier()
    dialog.show()
    sys.exit(app.exec_())
