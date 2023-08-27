# recents.py
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

"""
Popover for recently opened files.

Code inspired by Apostrophe, but rewritten in this project for GTK4.
For apostrophe's sources, see:
https://gitlab.gnome.org/World/apostrophe/-/blob/main/apostrophe/open_popover.py
https://gitlab.gnome.org/World/apostrophe/-/blob/main/data/ui/Recents.ui
"""

from itertools import islice

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Adw, Gdk, Gio, GLib, GObject, Gtk


class RecentItem(GObject.Object):
    def __init__(self, name, path, uri, **kwargs):
        super().__init__(**kwargs)
        self.name: str = name
        self.path: str = path
        self.uri: str = uri


@Gtk.Template(resource_path="/io/github/johannesjh/favagtk/recents.ui")
class RecentsPopover(Gtk.Popover):
    """Popover for recently opened files"""

    __gtype_name__ = "RecentsPopover"

    # ui elements:
    list_box = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    empty = Gtk.Template.Child()
    recent = Gtk.Template.Child()

    # data model:
    model = Gio.ListStore.new(RecentItem)
    recents_manager = Gtk.RecentManager.get_default()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_box.bind_model(self.model, self.create_row)
        self.on_manager_changed()
        self.recents_manager.connect("changed", self.on_manager_changed)

        display = Gdk.Display.get_default()
        provider = Gtk.CssProvider()
        provider.load_from_data(
            """
        #recents_popover label {
          font-weight: normal;
        }
        """,
            -1,
        )
        Gtk.StyleContext.add_provider_for_display(
            display, provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def create_row(self, item, **args):
        row = Adw.ActionRow.new()
        row.item = item
        row.set_title(item.name)
        row.set_subtitle(item.path)
        row.set_subtitle_lines(1)

        delete_button = Gtk.Button.new_from_icon_name("window-close-symbolic")
        delete_button.get_style_context().add_class("flat")
        delete_button.get_style_context().add_class("circular")
        delete_button.set_valign(Gtk.Align.CENTER)
        delete_button.set_visible(True)
        delete_button.connect("clicked", self.on_delete_click, item)

        row.add_suffix(delete_button)
        row.set_activatable(True)
        row.set_action_name("win.open_file")
        row.set_action_target_value(GLib.Variant.new_string(item.uri))

        return row

    def on_manager_changed(self, *args, **kwargs):
        self.model.remove_all()

        items = self.recents_manager.get_items()
        items = filter(lambda i: i.exists(), items)  # only existing items
        items = filter(
            lambda i: i.get_uri().endswith(".beancount"), items
        )  # only beancount files
        items = islice(items, 8)  # only the first 8 files

        for item in items:
            self.model.append(
                RecentItem(
                    item.get_display_name(), item.get_uri_display(), item.get_uri()
                )
            )

        self.stack.set_visible_child(self.recent if self.model else self.empty)

    @Gtk.Template.Callback()
    def on_search_entry_changed_cb(self, search_entry):
        recents_list = self.recents_manager.get_items()
        filtered_list = filter(
            lambda item: search_entry.get_text() in item.get_display_name(),
            recents_list,
        )

        self.model.remove_all()
        for item in filtered_list:
            self.model.append(
                RecentItem(
                    item.get_display_name(), item.get_uri_display(), item.get_uri()
                )
            )

    @Gtk.Template.Callback()
    def on_search_entry_activate_cb(self, *arg, **kwargs):
        print("activate")

    @Gtk.Template.Callback()
    def on_search_entry_stop_cb(self, *arg, **kwargs):
        print("stop")

    def on_delete_click(self, _widget, item):
        self.recents_manager.remove_item(item.uri)
