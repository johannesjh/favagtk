import time
import unittest
from unittest import TestCase

import gi

from fava_gtk.window import ApplicationWindow

gi.require_versions({"GdkPixbuf": "2.0", "Gdk": "3.0", "Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import Gtk  # noqa: E402


def refresh_gui(delay=0):
    while Gtk.events_pending():
        Gtk.main_iteration_do(blocking=False)
    time.sleep(delay)


class ApplicationWindowTest(TestCase):
    def setUp(self):
        self.window = ApplicationWindow(None)
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        refresh_gui()

    def test_initial_view(self):
        """Assert that the placeholder view is initially shown."""
        assert self.window.stack.get_visible_child() == self.window.placeholder_view


if __name__ == "__main__":
    unittest.main()
