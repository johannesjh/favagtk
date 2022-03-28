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

from gi.repository import Gtk, Gio

from .server import Server
from .shortcuts import FavagtkShortcutsWindow


@Gtk.Template(resource_path="/io/github/johannesjh/favagtk/window.ui")
class FavagtkWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavagtkWindow"

    label = Gtk.Template.Child()
    shortcuts_window = FavagtkShortcutsWindow()

    def __init__(self, **kwargs):
        # Initialize the application window
        super().__init__(**kwargs)
        self.set_help_overlay(self.shortcuts_window)

        # Initialize the fava server
        self.server = Server()
        self.server.connect("start", self.load_url)

    def load_url(self, _server, url):
        """Loads the URL in the webview and displays the web page"""
        print(url)

