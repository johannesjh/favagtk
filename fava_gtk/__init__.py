import logging
import os

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gio

from fava_gtk.window import ApplicationWindow

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


class Application(Gtk.Application):
    """The FavaGTK application."""

    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        """
        Handler for the "activate" signal.
        Starts the application, displays the application window.
        """
        window = ApplicationWindow(self)
        self.add_window(window)
        window.show_all()
        window.open_last_file()

        quit_action = Gio.SimpleAction(name="quit")
        quit_action.connect("activate", lambda *args: self.do_quit())
        self.add_action(quit_action)

        self.set_accels_for_action("app.quit", ["<Primary>Q"])
        self.set_accels_for_action("win.file_open", ["<Primary>O"])
        self.set_accels_for_action("win.close", ["<Primary>W"])
        self.set_accels_for_action("win.search", ["<Primary>F"])

    def do_quit(self):
        """
        Handler for the "quit" signal.
        Destroys all application windows.
        """
        for win in self.get_windows():
            win.do_destroy()
