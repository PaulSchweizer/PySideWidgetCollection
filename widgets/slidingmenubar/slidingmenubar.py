"""@package PySideWidgetCollection.slidingmenubar.slidingmenubar
@brief A header including a slide in menu, a title and a help option.
@date 2016/04/01
@version 1.0
@author Paul Schweizer
@email pschweizer@gmx.net
"""
import webbrowser

from PySide import QtCore, QtGui

from PySideWidgetCollection import utility
__all__ = ['SlidingMenuBar']


sm_form_class, sm_base_class = utility.load_ui_bases(__file__, 'SlidingMenu')


class SlidingMenu(sm_form_class, sm_base_class):

    """The menu widget for the sliding menu bar."""

    def __init__(self, parent=None):
        """Initialize the menu.

        @param parent The parent widget of the menu
        """
        super(SlidingMenu, self).__init__(parent=None)
        self.setupUi(self)
        self.scrollAreaWidgetContents.setLayout(QtGui.QVBoxLayout())
        self.scrollAreaWidgetContents.layout().addStretch()
        self.menu_bar = self.parent()
    # end def __init__

    def showEvent(self, event):
        """Run the slide-in animation and show the widget.

        @param event The show event
        @return A standard showEvent
        """
        self.slide_in_animation()

        return QtGui.QWidget.showEvent(self, event)
    # END def showEvent

    def leaveEvent(self, event):
        """Close automatically when the mouse leaves the widget.

        @param The leave event
        @return A standard leave event
        """
        self.slide_out_animation()
        self.menu_bar.show_menu_btn.clicked.disconnect()
        self.menu_bar.show_menu_btn.clicked.connect(self.menu_bar.show_menu)
        return QtGui.QWidget.leaveEvent(self, event)
    # end def leaveEvent

    def slide_in_animation(self):
        """Run the slide-in animation."""
        self.start_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.start_anim.setDuration(150)
        height = self.menu_bar.parent().geometry().height() - 46
        self.start_anim.setStartValue(QtCore.QRect(-250, 46, 0, height))
        self.start_anim.setEndValue(QtCore.QRect(0, 46, 250, height))
        self.start_anim.start()
        self.menu_bar.show_menu_btn.setChecked(True)
    # end def slide_in_animation

    def slide_out_animation(self):
        """Run the slide-out animation."""
        self.end_anim = QtCore.QPropertyAnimation(self, 'geometry')
        self.end_anim.setDuration(150)
        self.end_anim.setStartValue(self.geometry())
        height = self.menu_bar.parent().geometry().height()
        self.end_anim.setEndValue(QtCore.QRect(-250, 46, 0, height))
        self.end_anim.finished.connect(self.hide)
        self.end_anim.start()
        self.menu_bar.show_menu_btn.setChecked(False)
    # end def slide_out_animation
# end class SlidingMenu


smb_form_class, smb_base_class = utility.load_ui_bases(__file__,
                                                       'SlidingMenuBar')


class SlidingMenuBar(smb_form_class, smb_base_class):

    """A header including a slide in menu, a title and a help option.

    The that slides in from the left side over the widget.
    """

    def __init__(self, parent=None, title='', help_url=''):
        """Initialize menu.

        @param parent The parent widget
        @param title The title
        @param help_url The url to the help page.
                        The help pages are ideally set up within the
                        intranet, but any accessible url will do.
        """
        super(SlidingMenuBar, self).__init__(parent=parent)
        self.setupUi(self)
        self.sliding_menu.hide()
        self.show_menu_btn.clicked.connect(self.show_menu)
        self.help_btn.clicked.connect(self.show_help)

        self.help_url = help_url
        if self.property('help_url') is not None:
            self.help_url = self.property('help_url')
        # end if
    # end def __init__

    def showEvent(self, event):
        """Attach the menu to the parent, if a parent widget exists.

        @param event The show event
        @return A standard showEvent
        """
        if self.parent() is not None:
            self.sliding_menu.setParent(self.parent())
            self.sliding_menu.menu_bar = self
            self.sliding_menu.setEnabled(True)
        # end if
        return QtGui.QWidget.showEvent(self, event)
    # end def showEvent

    def show_menu(self):
        """Show the menu."""
        self.sliding_menu.show()
        self.show_menu_btn.clicked.disconnect()
        self.show_menu_btn.clicked.connect(self.hide_menu)
    # end def show_menu

    def hide_menu(self):
        """Hide the menu."""
        self.sliding_menu.slide_out_animation()
        self.show_menu_btn.clicked.disconnect()
        self.show_menu_btn.clicked.connect(self.show_menu)
    # end def hide_menu

    def add_menu_item(self, widget):
        """Add the given widget as an item to the menu.

        @param widget A widget
        """
        layout = self.sliding_menu.scrollAreaWidgetContents.layout()
        layout.insertWidget(layout.count()-1, widget)
    # end def add_menu_item

    def show_help(self):
        """Show the help for this tool in the browser."""
        if self.help_url != '':
            webbrowser.open(self.help_url)
        # end if
    # end def show_help
# end class SlidingMenuBar
