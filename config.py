import json
from pathlib import Path

class ConfigManager:
    CONFIG_FILE = Path.home() / ".arduino_cli_config.json"

    def __init__(self):
        self.cli_path = ""
        self.load_config()

    def load_config(self):
        try:
            if self.CONFIG_FILE.exists():
                with self.CONFIG_FILE.open("r") as f:
                    config = json.load(f)
                    self.cli_path = config.get("cli_path", "")
            else:
                self.cli_path = ""
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading configuration: {e}")
            self.cli_path = ""

    def save_config(self):
        config = {"cli_path": self.cli_path}
        try:
            with self.CONFIG_FILE.open("w") as f:
                json.dump(config, f, indent=4)
        except IOError as e:
            print(f"Error saving configuration: {e}")