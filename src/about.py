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

from gi.repository import Gtk

from . import PROFILE, VCS_TAG, VERSION


class AboutDialog(Gtk.AboutDialog):
    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = "favagtk"
        self.props.version = VERSION
        if PROFILE:
            self.props.version += f" {PROFILE} build "
        if VCS_TAG:
            self.props.version += f" ({VCS_TAG})"
        self.props.authors = ["johannesjh"]
        self.props.copyright = "2022 johannesjh"
        self.props.logo_icon_name = "org.gnome.gitlab.johannesjh.favagtk"
        self.props.modal = True
        self.set_transient_for(parent)
