import logging
import os
import socketserver
import sys
from importlib import resources
from multiprocessing import Process

import gi
from fava.application import app

gi.require_versions({"GdkPixbuf": "2.0", "Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import GdkPixbuf, Gtk, WebKit2 as WebKit  # noqa: E402

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = ApplicationWindow(self)
        self.add_window(window)
        window.show_all()


@Gtk.Template.from_string(resources.read_text("fava_desktop", "window.ui"))
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavaDesktopWindow"

    btn_open = Gtk.Template.Child()
    stack = Gtk.Template.Child()
    placeholder_view = Gtk.Template.Child()
    fava_icon = Gtk.Template.Child()
    btn_open2 = Gtk.Template.Child()
    fava_view = Gtk.Template.Child()

    # webkit workaround from https://stackoverflow.com/a/60128243
    WebKit.WebView()
    webview = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app, title="Fava")
        self.app = app
        self.server = Server()

        self.load_fava_icon()
        self.btn_open.connect("clicked", self.on_file_open)
        self.btn_open2.connect("clicked", self.on_file_open)

        settings = WebKit.Settings()
        settings.set_property("enable-developer-extras", True)
        self.webview.set_settings(settings)

    def load_fava_icon(self):
        """Loads fava's icon from python package resources"""
        loader = GdkPixbuf.PixbufLoader()
        loader.write(resources.read_text("fava_desktop", "icon.svg").encode())
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.fava_icon.set_from_pixbuf(pixbuf)

    def do_destroy(self):
        self.server.stop()
        self.app.remove_window(self)

    def on_file_open(self, action):
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
            self.server.start()
            self.webview.load_uri(self.server.url)
            self.stack.set_visible_child(self.fava_view)
        dialog.destroy()


class Server:
    def load_files(self, files):
        start_again = self.is_alive()
        if start_again:
            self.stop()
        app.config["BEANCOUNT_FILES"] = files
        if start_again:
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
        try:
            self.process.terminate()
        except AttributeError:
            pass

    def is_alive(self):
        try:
            return self.process.is_alive()
        except AttributeError:
            return False


def main():
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
