# window.py
#
# Copyright 2022 johannesjh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
from pathlib import Path

import gi

gi.require_versions({"Gtk": "4.0", "WebKit2": "5.0"})


from gi.repository import Gdk, Gio, GLib, Gtk, WebKit2

from . import BUILDTYPE
from .file_open_dialog import FileOpenDialog
from .recents import RecentsPopover
from .server import Server
from .shortcuts import FavagtkShortcutsWindow

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "DEBUG"))


@Gtk.Template(resource_path="/io/github/johannesjh/favagtk/window.ui")
class FavagtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavagtkWindow"

    # ui elements:
    header_bar = Gtk.Template.Child()
    recents_popover = Gtk.Template.Child()
    shortcuts_window = FavagtkShortcutsWindow()
    search_entry = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    placeholder_view = Gtk.Template.Child()
    fava_view = Gtk.Template.Child()

    # webkit workaround from https://stackoverflow.com/a/60128243
    WebKit2.WebView()
    webview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        # Initialize the application window
        super().__init__(**kwargs)
        self.set_help_overlay(self.shortcuts_window)

        # set "devel" style class depending on build type
        if BUILDTYPE == "debug":
            self.get_style_context().add_class("devel")

        # Initialize the fava server
        self.server = Server()
        self.server.connect("start", self.load_url)

        # Configure the webkit widget
        settings = WebKit2.Settings()
        settings.set_property("enable-developer-extras", True)
        self.webview.set_settings(settings)

        # Configure actions

        action = Gio.SimpleAction(name="open")
        action.connect("activate", self.show_file_open_dialog)
        self.add_action(action)

        action = Gio.SimpleAction.new("open_file", GLib.VariantType("s"))
        action.connect("activate", self.open_file_from_gvariant)
        self.add_action(action)

        action = Gio.SimpleAction(name="close")
        action.connect("activate", self.close)
        self.add_action(action)

        action = Gio.SimpleAction(name="search")
        action.set_enabled(False)
        action.connect("activate", self.search_start)
        self.add_action(action)

        action = Gio.SimpleAction.new_stateful(
            name="search_toggle",
            parameter_type=None,
            state=GLib.Variant.new_boolean(False),
        )
        action.set_enabled(False)
        action.connect("change-state", self.search_toggle)
        self.add_action(action)

    def show_file_open_dialog(self, *args):
        """
        Handler for the open action.
        Shows the file open dialog and opens the requested beancount file.
        """
        dialog = FileOpenDialog(transient_for=self)

        def on_response(dialog, response: Gtk.ResponseType, *args):
            if response == Gtk.ResponseType.ACCEPT:
                file = dialog.get_file()
                logger.info(f"User chose file {file.get_path()}.")
                self.open_file(file)

        dialog.connect("response", on_response, dialog)
        dialog.show()

    def open_file_from_gvariant(self, _action, gvariant):
        self.recents_popover.popdown()  # hides the popover
        self.open_file(Gio.File.new_for_uri(gvariant.get_string()))

    def open_file(self, file):
        """
        Opens a beancount file using fava.
        Note: A previously opened file will be closed without saving
        simply because the old server instance is discarded and a new
        instance is started for the new file.
        """
        # Verify that the file parameter is not None
        if file is None:
            logger.warning("File could not be opened because it was None.")
            return

        # Convert from Gio.File to str
        if isinstance(file, Gio.File):
            file = file.get_path()

        # Verify that the file exists
        file = Path(file)
        if not file.is_file():
            logger.warning(
                f"File {file} could not be opened because it does not exist."
            )
            return

        # Remember the file name
        self.beancount_file = str(file)

        # Show filename as the window's title
        self.set_property("title", str(file.name))

        # Adds to the list of recently used files
        Gtk.RecentManager().add_item(file.as_uri())

        # Instructs the server to load the beancount file.
        # Note: The server will then emit a "start" signal.
        # The application window, when handling this signal, will
        # instruct the webkit webview to load the URL.
        self.server.start(str(file))

    def load_url(self, _server, url):
        """Loads the URL in the webview and displays the web page"""
        self.webview.load_uri(self.server.url)
        self.stack.set_visible_child(self.fava_view)
        self.search_action.set_enabled(True)
        self.search_toggle_action.set_enabled(True)

    def search_toggle(self, action: Gio.SimpleAction, state):
        """
        Handler for the search_toggle action.
        Starts or stops the search.
        """
        if state:
            self.search_start()
        else:
            self.search_stop()

    def search_start(self, *args):
        """
        Handler for the search action, and also called directly.
        Displays the search bar, allowing the user to start searching.
        """
        self.search_toggle_action.set_state(GLib.Variant.new_boolean(True))
        self.search_bar.set_search_mode(True)
        self.search_entry.select_region(0, -1)
        self.search_entry.grab_focus()

    # @Gtk.Template.Callback("on_searchentry_changed")
    def on_searchentry_changed(self, search_entry):
        """
        Handler for when the user typed a search term.
        Instructs the webkit webview to search for the term.
        """
        find_controller = self.webview.get_find_controller()
        find_options = (
            WebKit2.FindOptions.CASE_INSENSITIVE | WebKit2.FindOptions.WRAP_AROUND
        )
        find_controller.search(self.search_entry.get_text(), find_options, 32)

    # @Gtk.Template.Callback("search_entry_previous_match_cb")
    def search_previous(self, *args):
        """
        Handler for the search field's "previous match" keyboard shortcut.
        Instructs the webkit webview to jump to the previous match.
        """
        find_controller = self.webview.get_find_controller()
        find_controller.search_previous()

    # @Gtk.Template.Callback("search_entry_next_match_cb")
    def search_next_match(self, *args):
        """
        Handler for the search field's "next match" keyboard shortcut.
        Instructs the webkit webview to jump to the next match.
        """
        find_controller = self.webview.get_find_controller()
        find_controller.search_next()

    # @Gtk.Template.Callback("search_entry_stop_search_cb")
    def search_stop(self, *args):
        """
        Handler for the search field's "stop search" signal,
        also called directly.
        Instructs the webkit webview to stop searching
        and hides the search bar.
        """
        self.search_toggle_action.set_state(GLib.Variant.new_boolean(False))
        self.search_bar.set_search_mode(False)
        find_controller = (
            self.webview.get_find_controller()
        )  # type: WebKit2.FindController
        find_controller.search_finish()
        self.search_entry.set_text("")
        self.webview.grab_focus()

    def close(self, *args):
        """Closes currently opened file, or closes the window if no file is open"""
        if self.server.is_running():
            self.close_file()
        else:
            self.do_destroy()

    def close_file(self, *args):
        """Closes the currently opened beancount file"""

        # forget the file name
        self.beancount_file = None

        # stop showing filename and dirname in the headerbar
        self.header_bar.set_property("title", "Fava")
        self.header_bar.set_property("subtitle", None)

        # cancel ongoing searches
        self.search_stop()
        self.search_action.set_enabled(False)
        self.search_toggle_action.set_enabled(False)
        self.stack.set_visible_child(self.placeholder_view)

        # stop the server
        self.server.stop()

    def do_destroy(self):
        """Closes the window"""

        # save last used file in application settings
        settings = Settings.load()
        settings.last_used_file = self.beancount_file
        settings.save()

        # close beancount file and stop web server
        self.close_file()

        # close the window
        self.app.remove_window(self)
