import gi

gi.require_versions({"Gtk": "3.0"})
from gi.repository import Gtk  # noqa: E402


window = Gtk.Window(title="Hello World")
window.show()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
