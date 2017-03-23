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

from widgets import utility
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

        # Full screen
        desktop = QtGui.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtGui.QCursor().pos())
        self.setGeometry(available_geometry)
        self.image_lbl.setGeometry(available_geometry)
        self.text_lbl.setGeometry(available_geometry)

        # Set the window frame less mode
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)

        # Grab current screen
        pxm = QtGui.QPixmap.grabWindow(QtGui.QApplication.desktop().winId())

        # Blur it
        effect = QtGui.QGraphicsBlurEffect()
        self.image_lbl.setGraphicsEffect(effect)
        effect.setBlurRadius(12)

        # Set the image
        self.image_lbl.setPixmap(pxm)

        # Set the text and put it on top of the image
        self.text_lbl.setText(text)
        self.text_lbl.setParent(self)

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


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = LoadingDialog()
    sys.exit(app.exec_())
