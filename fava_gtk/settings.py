import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dataclasses_json import dataclass_json
from gi.repository import GLib

logger = logging.getLogger(__name__)
logger.setLevel(os.environ.get("LOGLEVEL", "INFO"))


@dataclass_json
@dataclass
class Settings:

    # Settings:
    last_used_file: Optional[str] = None
    settings_version: int = 1

    @staticmethod
    def load():
        """Loads settings from JSON."""
        try:
            json_string = Settings.path().read_text()
            return Settings.from_json(json_string)
            logger.info(f"Loaded settings from {str(Settings.path())}.")
        except FileNotFoundError:
            logger.warning(f"Settings file {str(Settings.path())} not found.")
            return Settings()

    def save(self):
        """Saves settings to JSON"""
        json_string = self.to_json()
        Settings.path().write_text(json_string)
        logger.info(f"Saved settings to {str(Settings.path())}.")

    @staticmethod
    def path() -> Path:
        """Path to the settings file."""
        return Path(GLib.get_user_cache_dir()) / "fava-gtk.settings.json"
