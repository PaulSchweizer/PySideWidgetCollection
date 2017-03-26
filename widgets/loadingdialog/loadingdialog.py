"""A loading screen for time consuming processes."""
import logging

from Qt import QtCore, QtWidgets

from widgets import utility
__all__ = ['LoadingDialog']


class LoadingDialog(utility.ui_class(__file__, 'LoadingDialog')):
    """Show a screen while running a background process.

    The dialog will be shown until the given callback has terminated.
    """

    def __init__(self, callback=lambda: None, text=''):
        """Initialize the LoadingDialog.

        Args:
            callback (object): The function to execute during the
                               loading dialog
            text (str): The text to show
        """
        super(LoadingDialog, self).__init__()
        self.callback = callback
        self.text = text
        self.return_value = None
        self.painted = False

        # Set the window frame less mode
        self.setWindowFlags(QtCore.Qt.Widget |
                            QtCore.Qt.FramelessWindowHint |
                            QtCore.Qt.WindowStaysOnTopHint)

        cursor = QtWidgets.QCursor()
        cursor.setShape(QtCore.Qt.WaitCursor)
        self.setCursor(cursor)

        self._blur()
    # end def __init__

    def _blur(self):
        """Blur a snapshot of the current screen and display it."""
        # Full screen
        desktop = QtWidgets.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtWidgets.QCursor().pos())
        self.setGeometry(available_geometry)
        self.image_lbl.setGeometry(available_geometry)
        self.text_lbl.setGeometry(available_geometry)
        self.update(self.rect())

        # Grab current screen
        pxm = QtWidgets.QPixmap.grabWindow(
                                    QtWidgets.QApplication.desktop().winId())

        # Blur it
        effect = QtWidgets.QGraphicsBlurEffect(self.image_lbl)
        self.image_lbl.setGraphicsEffect(effect)
        effect.setBlurRadius(12)

        # Set the image
        self.image_lbl.setPixmap(pxm)

        # Set the text and put it on top of the image
        self.text_lbl.setText(self.text)
        self.text_lbl.setParent(self)
    # end def _blur
# end class LoadingDialog


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = LoadingDialog()
    dialog.exec_()
    sys.exit(app.exec_())
