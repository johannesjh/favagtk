# server.py
#
# Copyright 2022 johannesjh
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import os
import socketserver
import time
import urllib.request
from multiprocessing.context import Process
from threading import Thread
from urllib.error import URLError

from fava.application import app
from gi.repository import GObject

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


class Server(GObject.GObject):
    """
    Fava's web application and web server running in a separate process,
    provided as GObject with start and stop signals.
    """

    def __init__(self):
        GObject.GObject.__init__(self)

    __gsignals__ = {
        "start": (GObject.SIGNAL_RUN_FIRST, None, (str,)),
        "stop": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }

    def start(self, file):
        """
        Starts the server in order to open the requested files.
        Existing server instances are stopped before the new server is started.
        A "start" signal is emitted once the server's URL is available.
        """
        self.stop()
        logger.info(f"Starting the web server with file {file}...")
        app.config["BEANCOUNT_FILES"] = [file]
        port = self._find_free_port()
        host = "127.0.0.1"
        self.url = f"http://{host}:{port}/"
        self.process = Process(
            target=app.run,
            kwargs={"host": host, "port": port, "debug": False, "use_reloader": False},
        )
        self.process.start()

        # notify once the url is available
        def signal_that_server_started():
            logger.info(f"Server is now available a URL {self.url}.")
            self.emit("start", self.url)

        self.wait_until_available(signal_that_server_started)

    def stop(self):
        """
        Stops the webserver. A "stop" signal is then emitted.
        """
        logger.info("Stopping the web server...")
        try:
            self.process.terminate()
            self.process.join()
            self.url = None
            self.emit("stop")
        except AttributeError:
            pass

    def is_running(self):
        """
        Returns whether the server process is alive
        """
        try:
            return self.process.is_alive()
        except AttributeError:
            return False

    def wait_until_available(self, cb, *args, **kwargs):
        """
        Waits until the server's URL is available, then calls the `cb` function.
        The wait loop runs in a separate thread, repeatedly polling the URL.
        When the server returns a response for the URL, the loop stops
        and the callback function `cb` is called.
        """

        # from: https://stackoverflow.com/a/45498191
        def wait_loop(somepredicate, *args, timeout=3, period=0.01, **kwargs):
            must_end = time.time() + timeout
            while time.time() < must_end:
                if somepredicate(*args, **kwargs):
                    return True
                time.sleep(period)
            return False

        # from: https://stackoverflow.com/a/45498191
        def wait_until(*args, **kwargs):
            t = Thread(target=wait_loop, args=args, kwargs=kwargs)
            t.start()

        wait_until(self.is_available, self.url)
        cb(*args, **kwargs)

    @staticmethod
    def is_available(url):
        """
        Returns whether the URL is available,
        i.e., if a request to that URL gets a response from the server.
        """
        try:
            with urllib.request.urlopen(url, timeout=1):
                logger.debug(f"Checking server URL: {url} is available.")
                return True
        except URLError:
            logger.debug(f"Checking server URL: {url} is not (yet) available...")
            return False
        except Exception as e:
            logger.warn(
                f"An exception occurred while checking server URL: {url}...\n{e}"
            )
            return False

    @staticmethod
    def _find_free_port():
        """Returns a port number that is currently not used."""
        with socketserver.TCPServer(("localhost", 0), None) as s:
            return s.server_address[1]
