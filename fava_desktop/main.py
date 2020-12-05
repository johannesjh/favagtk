import logging
import os
import socketserver
import sys
from multiprocessing import Process

import gi
from fava.application import app

gi.require_versions({"Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import Gtk, Gio, WebKit2 as WebKit  # noqa: E402

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = ApplicationWindow(self)
        self.add_window(window)
        window.show_all()


class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Fava")
        self.app = app
        self.set_default_size(950, 700)

        self.header = Header(self)
        self.set_titlebar(self.header)

        self.server = Server()
        # TODO add an initial, empty view:
        self.server.load_files(["/home/jh/Downloads/example.beancount"])
        self.server.start()

        self.webview = WebKit.WebView()
        settings = WebKit.Settings()
        settings.set_property("enable-developer-extras", True)
        self.webview.set_settings(settings)
        self.webview.load_uri(self.server.url)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.webview)
        self.add(scrolled_window)

        open_action = Gio.SimpleAction.new("open", None)
        open_action.connect("activate", self.file_open)
        self.add_action(open_action)

    def do_destroy(self):
        self.server.stop()
        self.app.remove_window(self)

    def file_open(self, action):
        open_dialog = Gtk.FileChooserDialog(
            title="Open beancount files", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        open_dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.ACCEPT,
        )
        open_dialog.set_local_only(False)
        open_dialog.set_modal(True)
        open_dialog.connect("response", self.file_open_cb)
        open_dialog.show()

    def file_open_cb(self, dialog, response_id):
        if response_id == Gtk.ResponseType.ACCEPT:
            file = dialog.get_filename()
            logger.debug(f"User chose file {file}.")
            self.server.load_files([file])
            self.webview.load_uri(self.server.url)
        dialog.destroy()


class Header(Gtk.HeaderBar):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.set_title("Fava")
        self.set_show_close_button(True)
        self.button_open = Gtk.Button(label="Open")
        self.button_open.connect("clicked", window.file_open)
        self.pack_start(self.button_open)


class Server:
    def load_files(self, files):
        restart = self.is_alive()
        if restart:
            self.stop()
        app.config["BEANCOUNT_FILES"] = files
        if restart:
            self.start()

    def find_free_port(self):
        with socketserver.TCPServer(("localhost", 0), None) as s:
            return s.server_address[1]

    def start(self):
        self.port = self.find_free_port()
        self.host = "127.0.0.1"
        self.url = f"http://{self.host}:{self.port}/"
        self.process = Process(
            target=app.run,
            kwargs={"host": self.host, "port": self.port, "debug": False},
        )
        self.process.start()

    def stop(self):
        self.process.terminate()

    def is_alive(self):
        try:
            return self.process.is_alive()
        except AttributeError:
            return False


if __name__ == "__main__":
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)
