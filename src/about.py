# about.py
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

from gi.repository import Adw, Gtk

from . import PROFILE, VCS_TAG, VERSION


class AboutDialog(Adw.Window):
    # Implementation Notes:
    # We cannot inherit from Adw.AboutWindow because Adwaita marked the
    # AboutWindow class as "final". See, e.g.:
    # https://discourse.gnome.org/t/how-to-create-custom-libadwaita-widget/9379/2
    # https://gnome.pages.gitlab.gnome.org/libadwaita/doc/main/class.AboutWindow.html
    # We therefore use the __new__ method instead of __init__ in this class,
    # allowing to return an Adw.AboutWindow whenever this class is instantiated,
    # compare https://stackoverflow.com/a/2491881

    def __new__(cls, *, parent: Gtk.Window):
        # For inspiration, compare, e.g.,
        # https://gtk.justcode.com.br/gtk-libadwaita-widgets/
        dialog = Adw.AboutWindow()
        dialog.set_transient_for(parent=parent)

        dialog.set_application_name("favagtk")

        version = VERSION
        if PROFILE:
            version += f" {PROFILE} build "
        if VCS_TAG:
            version += f" ({VCS_TAG})"
        dialog.set_version(version)

        dialog.set_developer_name("johannesjh")
        dialog.add_credit_section(
            "Special Thanks to Upstream Projects",
            [
                "fava https://beancount.github.io/fava/",
                "beancount https://github.com/beancount/beancount",
            ],
        )

        dialog.set_license_type(Gtk.License.GPL_3_0)
        dialog.set_website("https://gitlab.gnome.org/johannesjh/favagtk")
        dialog.set_issue_url("https://gitlab.gnome.org/johannesjh/favagtk/-/issues")
        dialog.set_application_icon("org.gnome.gitlab.johannesjh.favagtk")

        return dialog
