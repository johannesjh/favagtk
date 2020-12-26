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

    stack = Gtk.Template.Child()
    fava_icon = Gtk.Template.Child()
    fava_view = Gtk.Template.Child()

    # webkit workaround from https://stackoverflow.com/a/60128243
    WebKit.WebView()
    webview = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app, title="Fava")
        self.app = app
        self.server = Server()
        self.load_fava_icon()
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
        """Stops the server and closes the window"""
        self.server.stop()
        self.app.remove_window(self)

    @Gtk.Template.Callback("file_open")
    def file_open(self, action):
        """Shows the file open dialog"""
        open_dialog = FileOpenDialog(parent=self)
        open_dialog.connect("response", self.file_open_cb)
        open_dialog.show()

    def file_open_cb(self, dialog, response_id):
        """Opens a beancount file"""
        if response_id == Gtk.ResponseType.ACCEPT:
            file = dialog.get_filename()
            logger.debug(f"User chose file {file}.")
            self.server.load_files([file])
            self.server.start()
            self.webview.load_uri(self.server.url)
            self.stack.set_visible_child(self.fava_view)
        dialog.destroy()


class FileOpenDialog(Gtk.FileChooserDialog):
    def __init__(self, *args, **kwargs):
        kwargs = {
            "title": "Open Beancount Files",
            "action": Gtk.FileChooserAction.OPEN,
            **kwargs,
        }
        super().__init__(*args, **kwargs)

        self.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.ACCEPT,
        )
        self.set_default_response(Gtk.ResponseType.ACCEPT)

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

        self.set_local_only(False)
        self.set_modal(True)


class Server:
    """Fava application server"""

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
