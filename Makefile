.PHONY: run
run:
	# This target builds and runs favagtk's development build
	flatpak-builder --force-clean _build org.gnome.gitlab.johannesjh.favagtk.devel.json
	flatpak-builder --run _build org.gnome.gitlab.johannesjh.favagtk.devel.json favagtk

