"""Animated confirm dialog for a better guidance of the user."""
from functools import partial

from Qt import QtCore, QtWidgets

from widgets import utility
__all__ = ['ConfirmDialog']


class ConfirmDialog(utility.ui_class(__file__, 'ConfirmDialog')):
    """The dialog slides in from the left.

    The dialog is fixed to the center of the screen, spanning the whole
    screen width. The dialog slides out to right when closed.
    """

    def __init__(self,
                 title='Confirm Dialog',
                 subtitle='Please cancel or confirm',
                 message=None,
                 buttons=['Confirm', 'Cancel'],
                 default_button='Confirm',
                 cancel_button='Cancel',
                 inner_widget=None,
                 size=None):
        """Initialize the ConfirmDialog.

        Args:
            title (str): The title for the dialog.
            message (str): The message to be displayed.
            button (list of str): The buttons.
            default_button (str): The preselected button.
            cancel_button (str): The cancel button.
            inner_widget (str): A qt widget that is to be displayed in
                                the ConfirmDialog.
            size ((int, int)): The size of the dialog.
        """
        super(ConfirmDialog, self).__init__()
        self.title = title
        self.subtitle = subtitle
        self.message = message
        self.default_button = default_button
        self.cancel_button = cancel_button
        self.inner_widget = inner_widget

        self.status = False
        self.clicked_button = None
        self.animation_speed = 100
        self.focused_button = None

        if size is not None:
            self.resize(size[0], size[1])
        # end if

        self._setup_ui()
        self._setup_buttons(buttons)
        self.exec_()
    # end def __init__

    def _setup_ui(self):
        """Set up the UI.

        * Set the Window title
        * Set the message text
        * Add the inner widget if any is given
        """
        self.setWindowTitle(self.title)
        self.title_lbl.setText(self.title)
        self.subtitle_lbl.setText(self.subtitle)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
        if self.message is not None:
            self.message_lbl.setText(self.message)
        else:
            self.message_lbl.hide()
        # end if
        if self.inner_widget is not None:
            self.inner_widget.dialog = self
            self.inner_widget_wid.layout().addWidget(self.inner_widget)
        else:
            self.inner_widget_wid.hide()
        # end if
    # end def _setup_ui

    def _setup_buttons(self, buttons):
        """Set up the buttons with the correct signals."""
        self.buttons = list()
        for i, button_name in enumerate(buttons):
            button = QtWidgets.QPushButton(button_name)
            self.actions_wid.layout().addWidget(button)
            if button_name == self.cancel_button:
                button.clicked.connect(partial(self.cancel, button_name))
            else:
                button.clicked.connect(partial(self.confirm, button_name))
            # end if
            self.buttons.append(button)
            if button_name == self.default_button:
                self._focus_button(i)
            # end if
        # end for
    # end def _setup_buttons

    def _focus_button(self, index):
        """Set the focus to the button behind the given index.

        @param index the index of the focus button in the button list
        """
        for i, button in enumerate(self.buttons):
            if i == index:
                button.setDefault(True)
                self.focused_button = button
            else:
                button.setDefault(False)
            # end if
        # end for
    # end def _focus_button

    def showEvent(self, event):
        """Execute the start animation."""
        self._start_animation()
        super(ConfirmDialog, self).showEvent(event)
    # end def showEvent

    def keyPressEvent(self, event):
        """Integrate key signals into to dialog.

        Integrates the following key signals into the ConfirmDialog:
        * arrow left/right - cycles through the buttons
        * enter - executes the currently selected button's click
                  action if any of the buttons has focus.
                  If no button has focus and an inner widget exists with
                  a focussed button, that buttons click event is being
                 executed.
        * esc - aborts the confirm dialog by using the cancel action
        @param event the key press event
        @return a standard keyPressEvent
        """
        key = event.key()
        if key == QtCore.Qt.Key_Right or key == QtCore.Qt.Key_Left:
            if self.focused_button is None:
                index = -1
            else:
                index = self.buttons.index(self.focused_button)
            # end if
            if key == QtCore.Qt.Key_Right:
                new_index = index + 1
                if new_index >= len(self.buttons):
                    new_index = 0
                # end if
            else:
                new_index = index - 1
                if new_index < 0:
                    new_index = len(self.buttons)-1
                # end if
            # end if
            self._focus_button(new_index)
        elif key == QtCore.Qt.Key_Enter:
            if self.focused_button is not None:
                self.focused_button.click()
            else:
                if self.inner_widget is not None:
                    if hasattr(self.inner_widget, 'focused_button'):
                        if self.inner_widget.focused_button is not None:
                            self.inner_widget.focused_button.click()
                        # end if
                    # end if
                # end if
            # end if
        elif key == QtCore.Qt.Key_Escape:
            self.cancel(None)
        # end if
        super(ConfirmDialog, self).keyPressEvent(event)
    # end def mousePressEvent

    def confirm(self, button_name):
        """Confirm and closes the dialog.

        The status is set to True and if the dialog is animated,
        the end animation is started.
        """
        self.status = True
        self.clicked_button = button_name
        try:
            self._end_animation()
        except Exception as err:
            print err
            self.close()
        # end try
    # end def confirm

    def cancel(self, button_name):
        """Cancel and close the dialog.

        The status is set to False, and if the dialog is animated,
        the end animation is started.
        """
        self.status = False
        self.clicked_button = button_name
        try:
            self._end_animation()
        except Exception as err:
            print err
            self.close()
        # end try
    # end def cancel

    def _start_animation(self):
        """Execute the start animation.

        Slides the dialog into the screen from the left side.
        """
        self.start_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.start_anim.setDuration(self.animation_speed)
        self.start_anim.setStartValue(self._get_start_geometry())
        self.start_anim.setEndValue(self._get_display_geometry())
        self.start_anim.start()
    # end def _start_animation

    def _end_animation(self):
        """Execute the end animation.

        Slides the dialog out to the right.
        """
        self.end_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.end_anim.setDuration(self.animation_speed)
        self.end_anim.setStartValue(self.geometry())
        self.end_anim.setEndValue(self._get_end_geometry())
        self.end_anim.finished.connect(self.close)
        self.end_anim.start()
    # end def _end_animation

    def _get_start_geometry(self):
        """The optimal geometry for the dialog in it's smallest form.

        @return a QRect with the correct geometry data.
        """
        desktop = QtWidgets.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtWidgets.QCursor().pos())
        x = available_geometry.x() - self.width()
        y = (available_geometry.height()/2) - (self.height()/2)
        w = self.width()
        h = self.height()
        return QtCore.QRect(x, y, w, h)
    # end def _get_start_geometry

    def _get_display_geometry(self):
        """The optimal geometry for the final display appearance.

        @return a QRect with the correct geometry data.
        """
        desktop = QtWidgets.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtWidgets.QCursor().pos())
        x = available_geometry.x()
        y = (available_geometry.height()/2) - (self.height()/2)
        w = available_geometry.width()
        h = self.height()
        return QtCore.QRect(x, y, w, h)
    # end def _get_display_geometry

    def _get_end_geometry(self):
        """The optimal geometry for the final display appearance.

        @return a QRect with the correct geometry data.
        """
        desktop = QtWidgets.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtWidgets.QCursor().pos())
        x = available_geometry.x() + available_geometry.width()
        y = (available_geometry.height()/2) - (self.height()/2)
        w = 0
        h = self.height()
        return QtCore.QRect(x, y, w, h)
    # end def _get_end_geometry
# end class ConfirmDialog


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog = ConfirmDialog()
    sys.exit(app.exec_())
