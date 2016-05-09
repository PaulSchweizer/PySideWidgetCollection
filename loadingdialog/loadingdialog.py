"""@package PySideWidgetCollection.loadingdialog.loadingdialog
@brief A loading screen for time consuming processes.
@date 2016/02/05
@version 2.0
@author Paul Schweizer
@email paulschweizer@gmx.net
"""
import os
import logging

from PySide import QtCore, QtGui

from PySideWidgetCollection import utility
__all__ = ['LoadingDialog']


base_class, form_class = utility.load_ui_bases(__file__, 'LoadingDialog')


class LoadingDialog(base_class, form_class):

    """Show a screen while running a background process.

    The dialog will be shown until the given callback has run.
    """

    def __init__(self, callback=lambda: None, text='Loading ...'):
        """Initialize the LoadingDialog."""
        super(LoadingDialog, self).__init__()
        self.setupUi(self)

        self.callback = callback
        self.return_value = None
        self.painted = False

        # Set the window opacity
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setAttribute(QtCore.Qt.WA_PaintOnScreen)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)

        # Fill the screen
        desktop = QtGui.QApplication.instance().desktop()
        self.setGeometry(desktop.screenGeometry(QtGui.QCursor().pos()))

        # Set the semi-transparent background
        palette = QtGui.QPalette()
        pxm = QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'resource',
                                         'semi_transparent_bg.png'))
        brush = QtGui.QBrush(pxm)
        palette.setBrush(QtGui.QPalette.Window, brush)
        self.setPalette(palette)

        # Set the text
        self.label.setText(text)

        # Show the loading dialog
        self.exec_()
    # end def __init__

    def paintEvent(self, event):
        """Overridden to show the dialog while running the callback.

        After the first paint event, that paints the widget on the
        screen, the callback is launched. This ensures that the dialog
        is visible while running the background task and makes it
        possible to close the dialog afterwards.
        @param event The QPaintEvent
        """
        if not self.painted:
            self.painted = True
            cursor = QtGui.QCursor()
            cursor.setShape(QtCore.Qt.WaitCursor)
            self.setCursor(cursor)
            self.update(self.rect())
        elif self.painted:
            try:
                self.return_value = self.callback()
            except Exception as e:
                logging.exception(e)
            # end try to
            self.close()
        # end if
    # end def paintEvent
# end class LoadingDialog
