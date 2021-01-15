import logging
import os
import socketserver
import sys
from importlib import resources
from multiprocessing import Process
from typing import Callable
from typing import Optional

import gi

from fava.application import app

gi.require_versions({"GdkPixbuf": "2.0", "Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import GdkPixbuf, Gtk, WebKit2, Gio, GLib  # noqa: E402

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
        self.set_accels_for_action("win.search", ["<Primary>F"])

    def do_quit(self):
        for win in self.get_windows():
            win.do_destroy()


@Gtk.Template.from_string(resources.read_text("fava_desktop", "window.ui"))
class ApplicationWindow(Gtk.ApplicationWindow):
    __gtype_name__ = "FavaDesktopWindow"

    stack = Gtk.Template.Child()  # type: Gtk.Stack
    placeholder_view = Gtk.Template.Child()  # type: Gtk.Box
    fava_icon = Gtk.Template.Child()  # type: Gtk.Image
    fava_view = Gtk.Template.Child()  # type: Gtk.Box
    search_bar = Gtk.Template.Child()  # type: Gtk.SearchBar

    # webkit workaround from https://stackoverflow.com/a/60128243
    WebKit2.WebView()
    webview = Gtk.Template.Child()

    def __init__(self, app):
        super().__init__(application=app, title="Fava")
        self.app = app
        self.server = Server()
        self.load_fava_icon()
        settings = WebKit2.Settings()
        settings.set_property("enable-developer-extras", True)
        self.webview.set_settings(settings)

        self.open_action = Gio.SimpleAction(name="file_open")
        self.open_action.connect("activate", self.file_open)
        self.add_action(self.open_action)

        self.close_action = Gio.SimpleAction(name="close")
        self.close_action.connect("activate", self.close)
        self.add_action(self.close_action)

        self.search_action = Gio.SimpleAction(name="search")
        self.search_action.set_enabled(False)
        self.search_action.connect("activate", self.search_start)
        self.add_action(self.search_action)

        self.search_toggle_action = Gio.SimpleAction.new_stateful(
            name="search_toggle",
            parameter_type=None,
            state=GLib.Variant.new_boolean(False),
        )
        self.search_toggle_action.set_enabled(False)
        self.search_toggle_action.connect("change-state", self.search_toggle)
        self.add_action(self.search_toggle_action)

        # workaround because
        # `self.search_entry = Gtk.Template.Child()` does not work, neither does
        # `self.get_template_child(Gtk.SearchEntry, "search_entry")`.
        self.search_entry = find_child(
            self.search_bar, lambda widget: isinstance(widget, Gtk.SearchEntry)
        )  # type: Gtk.SearchEntry

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
            self.search_action.set_enabled(True)
            self.search_toggle_action.set_enabled(True)

    def search_toggle(self, action: Gio.SimpleAction, state):
        """Toggles the search bar"""
        if state:
            self.search_start()
        else:
            self.search_stop()

    def search_start(self, *args):
        self.search_toggle_action.set_state(GLib.Variant.new_boolean(True))
        self.search_bar.set_search_mode(True)
        self.search_entry.select_region(0, -1)
        self.search_entry.grab_focus()

    @Gtk.Template.Callback("search_entry_search_changed_cb")
    def search_changed(self, search_entry):
        find_controller = self.webview.get_find_controller()
        find_options = (
            WebKit2.FindOptions.CASE_INSENSITIVE | WebKit2.FindOptions.WRAP_AROUND
        )
        find_controller.search(self.search_entry.get_text(), find_options, 32)

    @Gtk.Template.Callback("search_entry_previous_match_cb")
    def search_previous(self, *args):
        find_controller = self.webview.get_find_controller()
        find_controller.search_previous()

    @Gtk.Template.Callback("search_entry_next_match_cb")
    def search_next_match(self, *args):
        find_controller = self.webview.get_find_controller()
        find_controller.search_next()

    @Gtk.Template.Callback("search_entry_stop_search_cb")
    def search_stop(self, *args):
        self.search_toggle_action.set_state(GLib.Variant.new_boolean(False))
        self.search_bar.set_search_mode(False)
        find_controller = (
            self.webview.get_find_controller()
        )  # type: WebKit2.FindController
        find_controller.search_finish()
        self.search_entry.set_text("")
        self.webview.grab_focus()

    def close(self, *args):
        """Closes currently opened file, or closes the window if no file is open"""
        if self.server.is_alive():
            self.close_file()
        else:
            self.do_destroy()

    def close_file(self, *args):
        """Closes the currently opened beancount file"""
        self.search_stop()
        self.search_action.set_enabled(False)
        self.search_toggle_action.set_enabled(False)
        self.stack.set_visible_child(self.placeholder_view)
        self.server.stop()

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


def find_child(widget: Gtk.Widget, criterion: Callable) -> Optional[Gtk.Widget]:
    """Returns first matching widget amongst the widget itself and its descandants"""
    if criterion(widget):
        return widget
    for child in widget.get_children():
        result = find_child(child, criterion)
        if isinstance(result, Gtk.Widget):
            return result
    return None


def main():
    application = Application()
    exit_status = application.run(sys.argv)
    sys.exit(exit_status)


if __name__ == "__main__":
    main()
