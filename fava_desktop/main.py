import sys
from multiprocessing import Process

import gi
from fava.application import app

gi.require_versions({"Gtk": "3.0", "WebKit2": "4.0"})
from gi.repository import Gtk, WebKit2 as WebKit  # noqa: E402


class Application(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)

    def do_activate(self):
        self.server = Server()
        self.server.load_files(["/home/jh/Downloads/example.beancount"])
        self.server.start()

        window = ApplicationWindow()
        self.add_window(window)
        window.show_all()

    def quit(self, *args, **kwargs):
        self.server.stop()
        super().quit()


class ApplicationWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        Gtk.Window.__init__(self, *args, **kwargs)
        self.set_title("Fava")
        self.set_default_size(950, 700)

        self.header = Header()
        self.set_titlebar(self.header)

        self.webview = WebKit.WebView()
        self.webview.load_uri("http://127.0.0.1:8899/")

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.add(self.webview)
        self.add(scrolled_window)

        self.connect("destroy", application.quit)


class Header(Gtk.HeaderBar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Fava")
        self.set_show_close_button(True)

        self.button_open = Gtk.Button(label="Open")
        self.pack_start(self.button_open)


class Server:
    def load_files(self, files):
        restart = self.is_alive()
        if restart:
            self.stop()
        app.config["BEANCOUNT_FILES"] = files
        if restart:
            self.start()

    def start(self):
        self.process = Process(
            target=app.run, kwargs={"host": "127.0.0.1", "port": 8899, "debug": False}
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
