import gi

gi.require_versions({"Gtk": "4.0"})
from gi.repository import Gtk


class FileOpenDialog(Gtk.FileChooserNative):
    """File-Open Dialog for choosing a beancount file."""

    def __init__(self, *args, **kwargs):
        kwargs = {
            "title": "Open Beancount Files",
            "action": Gtk.FileChooserAction.OPEN,
            **kwargs,
        }
        super().__init__(*args, **kwargs)

        filter_beancount = Gtk.FileFilter()
        filter_beancount.set_name("Beancount files")
        filter_beancount.add_pattern("*.beancount")
        self.add_filter(filter_beancount)

        filter_plain = Gtk.FileFilter()
        filter_plain.set_name("Plaintext files")
        filter_plain.add_mime_type("text/plain")
        self.add_filter(filter_plain)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        self.add_filter(filter_any)

        self.set_modal(True)
