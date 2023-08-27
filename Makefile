# Makefile
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


# This makefile is for building and running favagtk

.PHONY: build
build:
	flatpak-builder --verbose --force-clean --repo=_repo _build org.gnome.gitlab.johannesjh.favagtk.json

.PHONY: run
run: build
	flatpak-builder --verbose --run _build org.gnome.gitlab.johannesjh.favagtk.json favagtk

dist: build
dist:
	flatpak build-bundle --verbose _repo favagtk.flatpak org.gnome.gitlab.johannesjh.favagtk

