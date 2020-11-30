import sys

import gi

gi.require_versions({"Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import Gtk, WebKit2 as WebKit  # noqa: E402


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = ApplicationWindow(self)
        window.show_all()


class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self, application):
        Gtk.Window.__init__(self, application=application)
        self.set_title("Fava")
        self.set_default_size(700, 500)

        self.webview = WebKit.WebView()
        self.webview.load_uri("https://gnome.org/")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.webview)
        self.add(scrolled_window)

        self.connect("destroy", Gtk.main_quit)


if __name__ == "__main__":
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)
