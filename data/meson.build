desktop_file = i18n.merge_file(
  input: 'org.gnome.gitlab.johannesjh.favagtk.desktop.in',
  output: 'org.gnome.gitlab.johannesjh.favagtk.desktop',
  type: 'desktop',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'applications')
)

desktop_utils = find_program('desktop-file-validate', required: false)
if desktop_utils.found()
  test('Validate desktop file', desktop_utils,
    args: [desktop_file]
  )
endif

appstream_file = i18n.merge_file(
  input: 'org.gnome.gitlab.johannesjh.favagtk.appdata.xml.in',
  output: 'org.gnome.gitlab.johannesjh.favagtk.appdata.xml',
  po_dir: '../po',
  install: true,
  install_dir: join_paths(get_option('datadir'), 'appdata')
)

appstream_util = find_program('appstream-util', required: false)
if appstream_util.found()
  test('Validate appstream file', appstream_util,
    args: ['validate', appstream_file]
  )
endif

install_data('org.gnome.gitlab.johannesjh.favagtk.gschema.xml',
  install_dir: join_paths(get_option('datadir'), 'glib-2.0/schemas')
)

compile_schemas = find_program('glib-compile-schemas', required: false)
if compile_schemas.found()
  test('Validate schema file', compile_schemas,
    args: ['--strict', '--dry-run', meson.current_source_dir()]
  )
endif


# install mime type
install_data(
  'mime.xml',
  install_dir: 'share/mime/packages',
  rename: 'org.gnome.gitlab.johannesjh.favagtk.xml'
)

# update mime database
# using a custom install script as a workaround until I have meson 64,
# specifically see meson issue #10865 and
# release notes https://mesonbuild.com/Release-notes-for-0-64-0.html#added-update_mime_database-to-gnomepost_install
meson.add_install_script('update-mime-database', join_paths(get_option('prefix'), get_option('datadir'), 'mime'), skip_if_destdir: true)


# build and install meson sub directories:
subdir('icons')
