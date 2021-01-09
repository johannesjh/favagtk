import logging
import os
import socketserver
import sys
from importlib import resources
from multiprocessing import Process

import gi

from fava.application import app

gi.require_versions({"GdkPixbuf": "2.0", "Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import GdkPixbuf, Gtk, WebKit2 as WebKit, Gio  # noqa: E402

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        window = ApplicationWindow(self)
        self.add_window(window)
        window.show_all()

        quit_action = Gio.SimpleAction(name="quit")
        quit_action.connect("activate", lambda *args: self.do_quit())
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Primary>Q"])

        self.set_accels_for_action("win.file_open", ["<Primary>O"])
        self.set_accels_for_action("win.close", ["<Primary>W"])

    def do_quit(self):
        for win in self.get_windows():
            win.do_destroy()


@Gtk.Template.from_string(resources.read_text("fava_desktop", "window.ui"))
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavaDesktopWindow"

    stack = Gtk.Template.Child()
    placeholder_view = Gtk.Template.Child()
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

        open_action = Gio.SimpleAction(name="file_open")
        open_action.connect("activate", self.file_open)
        self.add_action(open_action)

        close_action = Gio.SimpleAction(name="close")
        close_action.connect("activate", self.close)
        self.add_action(close_action)

    def load_fava_icon(self):
        """Loads fava's icon from python package resources"""
        loader = GdkPixbuf.PixbufLoader()
        loader.write(resources.read_text("fava_desktop", "icon.svg").encode())
        loader.close()
        pixbuf = loader.get_pixbuf()
        self.fava_icon.set_from_pixbuf(pixbuf)

    def file_open(self, *args):
        """Shows the file open dialog and opens the requested beancount file"""
        dialog = FileOpenDialog(transient_for=self)
        response = dialog.run()
        if response == Gtk.ResponseType.ACCEPT:
            file = dialog.get_filename()
            logger.info(f"User chose file {file}.")
            self.server.start([file])
            self.webview.load_uri(self.server.url)
            self.stack.set_visible_child(self.fava_view)

    def close(self, *args):
        """Closes currently opened file, or closes the window if no file is open"""
        if self.server.is_alive():
            self.close_file()
        else:
            self.do_destroy()

    def close_file(self, *args):
        """Closes the currently opened beancount file"""
        self.server.stop()
        self.stack.set_visible_child(self.placeholder_view)

    def do_destroy(self):
        """Destroys the window, having first closed the file and stopped the server."""
        self.close_file()
        self.app.remove_window(self)


class FileOpenDialog(Gtk.FileChooserNative):
    """Dialog for choosing beancount files."""

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

        self.set_local_only(False)
        self.set_modal(True)


class Server:
    """Fava's application server running in a separate process"""

    def find_free_port(self):
        with socketserver.TCPServer(("localhost", 0), None) as s:
            return s.server_address[1]

    def start(self, files):
        """
        Starts the fava webserver in order to open the requested files.
        Existing server instances are stopped before the new server is started.
        """
        logger.info("Loading files " + ", ".join(files) + "...")
        self.stop()
        app.config["BEANCOUNT_FILES"] = files
        port = self.find_free_port()
        host = "127.0.0.1"
        self.url = f"http://{host}:{port}/"
        self.process = Process(
            target=app.run,
            kwargs={"host": host, "port": port, "debug": False},
        )
        self.process.start()
        logger.info(f"Server started at {self.url}.")

    def stop(self):
        """Stops the fava webserver."""
        try:
            self.process.terminate()
            self.process.join()
            self.url = None
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
