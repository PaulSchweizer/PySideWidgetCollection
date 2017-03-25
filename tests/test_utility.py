import os

import unittest

from widgets import utility


class TestUtility(unittest.TestCase):
    """Test utilities."""

    def test_get_ui_file_path(self):
        """Get the ui file path."""
        widget_file = os.path.join('test', 'test_widget.py')
        widget_name = 'TestWidget'
        path = utility.get_ui_file_path(widget_file, widget_name)
        self.assertEqual(path, os.path.join('test', 'resource', 'TestWidget.ui'))
    # end def test_get_ui_file_path

    def test_get_css_file_path(self):
        """Get the ui file path."""
        widget_file = os.path.join('test', 'test_widget.py')
        widget_name = 'TestWidget'
        path = utility.get_css_file_path(widget_file, widget_name)
        self.assertEqual(path, os.path.join('test', 'resource', 'TestWidget.css'))
    # end def test_get_css_file_path
# end class TestUtility


if __name__ == '__main__':
    unittest.main()
# end if
