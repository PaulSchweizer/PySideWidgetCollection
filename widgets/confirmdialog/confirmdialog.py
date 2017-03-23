"""@package PySideWidgetCollection.confirmdialog.confirmdialog
@brief A PySide confirm dialog providing multiple ways of use.
@date 2014/11/20
@version 1.0
@author Paul Schweizer
@email paulschweizer@gmx.net
"""
from PySide import QtCore, QtGui

from widgets import utility
__all__ = ['WindowHeader', 'ConfirmDialog']


wh_base_class, wh_form_class = utility.load_ui_bases(__file__, 'WindowHeader')


class WindowHeader(wh_base_class, wh_form_class):

    """A header for the Confirm Dialog and other tools."""

    def __init__(self, title, subtitle=''):
        """Initialize the Header.

        @param title The title of the window
        @param subtitle An optional subtitle
        """
        super(WindowHeader, self).__init__()
        self.setupUi(self)
        self.title_lbl.setText(title)
        if subtitle != '':
            self.subtitle_lbl.setText(subtitle)
        else:
            self.subtitle_lbl.hide()
        # end if
        utility.set_stylesheet(self, __file__)
    # end def __init__
# end class WindowHeader


cd_base_class, cd_form_class = utility.load_ui_bases(__file__, 'ConfirmDialog')


class ConfirmDialog(cd_base_class, cd_form_class):

    """The dialog can be used in three different ways:

    * floating: The dialog floats normally, no specific attributes
                or styles are set, except that the dialog appears
                frameless which should be implemented as the
                standard behavior for all widgets.
                The mode identifier for floating is 0
    * non-floating: The dialog is fixed to the center of the screen,
                    spanning the whole screen width. Furthermore,
                    the dialog is styled to fit with the companies
                    colors and form.
                    In fixed mode, also animation is possible. The
                    dialog is then being slid in from the left when
                    opening and out to left when closing.
                    The mode identifier for non-floating is 1
    * loading screen: When given a callback, the dialog acts as
                      loading screen, displaying the given message
                      and title until the callback has run.
                      After that, the dialog is automatically
                      closed. Animations are disabled in this mode.
                      The mode identifier for loading screen is 2
    """

    def __init__(self,
                 title='Confirm Dialog',
                 subtitle='Please cancel or confirm',
                 message=None,
                 button=['Confirm', 'Cancel'],
                 default_button='Confirm',
                 cancel_button='Cancel',
                 dismiss_string='Cancel',
                 floating=False,
                 animated=True,
                 inner_widget=None,
                 callback=None,
                 predefined_style=None,
                 size=None,
                 auto_close=True,
                 auto_raise=True):
        """Initialize the ConfirmDialog.

        @param title the title for the dialog
        @param message the message to be displayed
        @param button the buttons
        @param default_button the preselected button
        @param cancel_button the cancel button
        @param dismiss_string the string used for canceling, not
                              implemented
        @param floating whether the confirm dialog is floating or fixed
                        to the center of the screen
        @param animated whether the dialog is animated, animation only
                        works in non-floating mode
        @param inner_widget a qt widget that is to be displayed in the
                             confirm dialog.
        @param callback a callback that gets executed after the dialog
                        has been shown. The dialog is closed once the
                        callback has run.
        @param predefined_style the id for a predefined style for the
                                confirm dialog.
        @param size the size of the dialog
        @param auto_close whether to close the dialog automatically
               after any button has been pressed
        @param auto_raise whether to automatically raise the dialog
        @todo Better title setup

        """
        super(ConfirmDialog, self).__init__()
        self.setupUi(self)
        utility.set_stylesheet(self, __file__)
        self.status = False
        self._animation_speed = 100
        self._title = title
        self._subtitle = subtitle
        self._message = message
        self._button = button
        self._default_button = default_button
        self._cancel_button = cancel_button
        self.focussed_button = None
        self._dismiss_string = dismiss_string
        self._floating = floating
        self._animated = animated
        self.inner_widget = inner_widget
        self._callback = callback
        self.callback_result = None
        self._predefined_style = predefined_style
        self._auto_close = auto_close
        self.painted = False
        if size is not None:
            self.resize(size[0], size[1])
        # end if
        self._set_predefined_style()
        self._set_mode()
        self._setup_button()
        self._setup_ui()
        self._init_signals()
        if auto_raise:
            self.show_dialog()
        # end if
    # end def __init__

    def _set_mode(self):
        """Set the mode according to the provided inputs."""
        if self._floating:
            self._mode = 0
        # end if
        if not self._floating:
            self._mode = 1
        # end if
        if self._callback is not None:
            self._mode = 2
            self._button = list()
        # end if
    # end def _set_mode

    def _set_predefined_style(self):
        """Set the confirm dialog to one of the predefined styles.

        Available styles are:
        * 0 - Info
        * 1 - Warning
        * 2 - Error
        """
        if self._predefined_style == 0:
            self._button = ['OK']
            self._default_button = 'OK'
            self.predefined_style_lbl.setAccessibleName('Info')
            css = ('background-color:#222822; color:#99cc99;')
            self.predefined_style_lbl.setStyleSheet(css)
            self.predefined_style_lbl.setText('Information')
        elif self._predefined_style == 1:
            self._button = ['OK']
            self._default_button = 'OK'
            css = ('background-color:#333322; color:#cccc99;')
            self.predefined_style_lbl.setStyleSheet(css)
            self.predefined_style_lbl.setText('Warning')
        elif self._predefined_style == 2:
            self._button = ['OK']
            self._default_button = 'OK'
            css = ('background-color:#332222; color:#99cccc;')
            self.predefined_style_lbl.setStyleSheet(css)
            self.predefined_style_lbl.setText('Error')
        else:
            self.predefined_style_lbl.hide()
        # end if
    # end def _set_predefined_style

    def _setup_ui(self):
        """Set up the UI.

        * Set the Window title
        * Set the message text
        * Some stylesheet and geometry adjustments for non floating
        * Add the inner widget if any is given
        """
        header = WindowHeader(self._title, self._subtitle)
        self.maincontent_vlay.insertWidget(0, header)
        self.setWindowTitle(self._title)
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint)
        if self._message is not None:
            self.message_lbl.setText(self._message)
        else:
            self.message_lbl.hide()
        # end if
        if self._mode > 0:
            self.close_btn.hide()
            self.topbar_hlay.hide()
            self.layout().setContentsMargins(9, 25, 9, 25)
            self.background_wid.layout().insertSpacing(0, 40)
            self.background_wid.layout().insertSpacing(2, 40)
            self.main_widget.setMaximumWidth(800)
        # end if

        if self.inner_widget is not None:
            self.inner_widget.dialog = self
            self.inner_widget_vlay.addWidget(self.inner_widget)
        # end if
    # end def _setup_ui

    def _get_start_geometry(self):
        """The optimal geometry for the dialog in it's smallest form.

        @return a QRect with the correct geometry data.
        """
        desktop = QtGui.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtGui.QCursor().pos())
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
        desktop = QtGui.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtGui.QCursor().pos())
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
        desktop = QtGui.QApplication.instance().desktop()
        available_geometry = desktop.screenGeometry(QtGui.QCursor().pos())
        x = available_geometry.x() + available_geometry.width()
        y = (available_geometry.height()/2) - (self.height()/2)
        w = 0
        h = self.height()
        return QtCore.QRect(x, y, w, h)
    # end def _get_end_geometry

    def _setup_button(self):
        """Set up the buttons with the correct signals."""
        self.buttons = list()
        for i, button_name in enumerate(self._button):
            button = QtGui.QPushButton(button_name)
            self.actions_vlay.addWidget(button)
            if button_name == self._cancel_button:
                button.clicked.connect(self.cancel)
            else:
                button.clicked.connect(self.confirm)
            # end if
            self.buttons.append(button)
            if button_name == self._default_button:
                self._focus_button(i)
            # end if
        # end for
    # end def _setup_button

    def _focus_button(self, index):
        """Set the focus to the button behind the given index.

        @param index the index of the focus button in the button list
        """
        for i, button in enumerate(self.buttons):
            if i == index:
                button.setDefault(True)
                self.focussed_button = button
            else:
                button.setDefault(False)
            # end if
        # end for
    # end def _focus_button

    def _init_signals(self):
        """Initialize the signals."""
        self.close_btn.clicked.connect(self.close)
    # end def _init_widgets

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
        next = 16777236
        prev = 16777234
        enter = 16777220
        esc = 16777216
        if key == next or key == prev:
            if self.focussed_button is None:
                index = -1
            else:
                index = self.buttons.index(self.focussed_button)
            # end if
            if key == next:
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
        elif key == enter:
            if self.focussed_button is not None:
                self.focussed_button.click()
            else:
                if self.inner_widget is not None:
                    if hasattr(self.inner_widget, 'focussed_button'):
                        if self.inner_widget.focussed_button is not None:
                            self.inner_widget.focussed_button.click()
                        # end if
                    # end if
                # end if
            # end if
        elif key == esc:
            self.cancel()
        # end if
        return QtGui.QWidget.keyPressEvent(self, event)
    # end def mousePressEvent

    def mousePressEvent(self, event):
        """The mouse press event.

        Captures the position of the press event, so the window can be
        moved relative to the cursor position.
        @note only active if floating is set to False.
        @param event the move event
        @return a standard mousePressEvent
        """
        self.mouse_press_position = event.pos()
        return QtGui.QWidget.mousePressEvent(self, event)
    # end def mousePressEvent

    def mouseMoveEvent(self, event):
        """Move the widget to the given location on the screen.

        @note only active if floating is set to False.
        @param event the move event
        @return a standard mouseMoveEvent
        """
        if self._floating:
            self.move(event.globalPos().x() - self.mouse_press_position.x(),
                      event.globalPos().y() - self.mouse_press_position.y())
        # end if
        return QtGui.QWidget.mouseMoveEvent(self, event)
    # end def mousePressEvent

    def confirm(self):
        """Confirm and closes the dialog.

        The status is set to True and if the dialog is animated,
        the end animation is started.
        """
        self.status = True
        if not self._auto_close:
            return
        # end if
        if self._mode == 1:
            try:
                self._end_animation()
            except Exception as err:
                print err
                self.close()
            # end try
        else:
            self.close()
        # end if
    # end def confirm

    def cancel(self):
        """Cancel and close the dialog.

        The status is set to False, and if the dialog is animated,
        the end animation is started.
        """
        self.status = False
        if self._mode == 1:
            try:
                self._end_animation()
            except Exception as err:
                print err
                self.close()
            # end try
        else:
            self.close()
        # end if
    # end def cancel

    def _start_animation(self):
        """Execute the start animation.

        Slides the dialog into the screen from the left side.
        """
        self.start_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.start_anim.setDuration(self._animation_speed)
        self.start_anim.setStartValue(self._get_start_geometry())
        self.start_anim.setEndValue(self._get_display_geometry())
        self.start_anim.start()
    # end def _start_animation

    def _end_animation(self):
        """Execute the end animation.

        Slides the dialog out to the right.
        """
        self.end_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.end_anim.setDuration(self._animation_speed)
        self.end_anim.setStartValue(self.geometry())
        self.end_anim.setEndValue(self._get_end_geometry())
        self.end_anim.finished.connect(self.close)
        self.end_anim.start()
    # end def _end_animation

    def show_dialog(self):
        """Show the dialog."""
        self.exec_()
    # end def show_dialog

    def showEvent(self, event):
        """Execute the start animation

        Only active if the dialog is animated and in non-floating mode.
        @param event the show event
        @return a standard showEvent
        """
        if self._mode == 1:
            self._start_animation()
        # end if
        return QtGui.QWidget.showEvent(self, event)
    # end def showEvent

    def paintEvent(self, event):
        """The paint event for the confirm dialog.

        Hijacked to provide the possibility to display this confirm
        dialog until the callback has been executed.
        If no callback is set, a standard QPaintEvent is returned.
        @param event the QPaintEvent
        @return a standard QPaintEvent
        """
        if self._mode != 2:
            QtGui.QPaintEvent(self.rect())
            return
        elif not self.painted:
            self.painted = True
            cursor = QtGui.QCursor()
            cursor.setShape(QtCore.Qt.WaitCursor)
            self.setCursor(cursor)
            self.update(self.rect())
        elif self.painted:
            try:
                self.callback_result = self._callback()
                self.confirm()
            except:
                self.cancel()
            # end try
        # end if
    # end def paintEvent
# end class ConfirmDialog


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    dialog = ConfirmDialog()
    sys.exit(app.exec_())
