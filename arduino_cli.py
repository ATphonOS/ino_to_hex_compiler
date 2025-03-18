import os
import platform
import subprocess
from config import ConfigManager

class ArduinoCLIManager:
    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.cli_path = config_manager.cli_path
        self.system = platform.system()

    def update_cli_path(self, new_path):
        #Update the arduino-cli path dynamically
        self.cli_path = new_path

    def check_cli_installation(self):
        #Check if arduino-cli is installed and accessible
        if not self.cli_path:
            return False, "arduino-cli path not specified."
        if not os.path.exists(self.cli_path):
            return False, "arduino-cli not found in the specified path."
        try:
            result = subprocess.run([self.cli_path, "--version"], capture_output=True, text=True, check=True)
            return True, f"arduino-cli version: {result.stdout.strip()}"
        except subprocess.CalledProcessError as e:
            return False, f"Error checking arduino-cli version: {e.stderr}"
        except FileNotFoundError:
            return False, "The arduino-cli executable is not found or is not executable."

    def install_core(self, core):
        #Install a specific Arduino core if not already installed
        if not self.cli_path:
            return False, "Arduino CLI path not specified."

        try:
            result = subprocess.run([self.cli_path, "core", "list"], check=True, capture_output=True, text=True)
            if core in result.stdout:
                return True, f"Core {core} is already installed."
        except subprocess.CalledProcessError as e:
            return False, f"Error verifying installed cores: {e.stderr}"

        try:
            subprocess.run([self.cli_path, "core", "install", core], check=True, capture_output=True, text=True)
            return True, f"Core {core} installed successfully."
        except subprocess.CalledProcessError as e:
            return False, f"Error installing core {core}: {e.stderr}"