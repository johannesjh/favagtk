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

import gi

gi.require_versions({"Gtk": "4.0", "WebKit2": "5.0"})

from gi.repository import Gdk, Gio, Gtk, WebKit2

from . import BUILDTYPE
from .server import Server
from .shortcuts import FavagtkShortcutsWindow


@Gtk.Template(resource_path="/io/github/johannesjh/favagtk/window.ui")
class FavagtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavagtkWindow"

    shortcuts_window = FavagtkShortcutsWindow()

    # webkit workaround from https://stackoverflow.com/a/60128243
    WebKit2.WebView()
    webview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        # Initialize the application window
        super().__init__(**kwargs)
        self.set_help_overlay(self.shortcuts_window)

        # Initialize the fava server
        self.server = Server()
        self.server.connect("start", self.load_url)

        # Configure the webkit widget
        settings = WebKit2.Settings()
        settings.set_property("enable-developer-extras", True)
        self.webview.set_settings(settings)

        # set "devel" style class depending on build type
        print(f"the builtype is {BUILDTYPE}")
        if BUILDTYPE == "debug":
            self.get_style_context().add_class("devel")

    def load_url(self, _server, url):
        """Loads the URL in the webview and displays the web page"""
        print(url)
