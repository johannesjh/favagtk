import gi

gi.require_versions({"Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import Gtk, WebKit2 as WebKit  # noqa: E402

window = Gtk.Window(title="Hello World")
window.set_default_size(700, 500)

webview = WebKit.WebView()
webview.load_uri("https://gnome.org/")
scrolled_window = Gtk.ScrolledWindow()
scrolled_window.add(webview)
window.add(scrolled_window)

window.show_all()
window.connect("destroy", Gtk.main_quit)

Gtk.main()
