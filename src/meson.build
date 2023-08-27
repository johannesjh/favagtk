# meson.build
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

pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'favagtk')
gnome = import('gnome')

blueprints = custom_target('blueprints',
  input: files(
    'recents.blp',
    'shortcuts.blp',
    'window.blp',
  ),
  output: '.',
  command: [find_program('blueprint-compiler'), 'batch-compile', '@OUTPUT@', '@CURRENT_SOURCE_DIR@', '@INPUT@'],
)

gnome.compile_resources('favagtk',
  'favagtk.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
  dependencies: blueprints,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('VCS_TAG', run_command('git', 'describe', '--always', check: false).stdout().strip())
conf.set('PROFILE', get_option('profile'))
conf.set('localedir', join_paths(get_option('prefix'), get_option('localedir')))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'favagtk.in',
  output: 'favagtk',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
)

init_file = configure_file(
  input: '__init__.py',
  output: '__init__.py',
  configuration: conf,
)

favagtk_sources = [
  init_file,
  'about.py',
  'app.py',
  'file_open_dialog.py',
  'main.py',
  'recents.py',
  'server.py',
  'shortcuts.py',
  'window.py',
]

install_data(favagtk_sources, install_dir: moduledir)
