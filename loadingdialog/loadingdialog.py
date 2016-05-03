"""@package
@brief A loading screen for time consuming processes.
@date 2016/02/05
@version 2.0
@author Paul Schweizer
@email paulschweizer@gmx.net
"""
import os
import logging

from PySide import QtCore, QtGui

import utils
__all__ = ['LoadingDialog']


base_class, form_class = utils.load_ui_bases(__file__, 'LoadingDialog')


class LoadingDialog(base_class, form_class):

    """A dialog that can be used as a loading screen.

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
    # END def __init__

    def paintEvent(self, event):
        """The paint event for the loading dialog.

        Hijacked to provide the possibility to display this dialog
        until the callback has been executed.
        @param event the QPaintEvent
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
        # END if
    # END def paintEvent
# END class LoadingDialog
