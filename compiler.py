import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
from utils import get_system_key

class ProjectCompiler:
    BOARDS = {
        "Arduino Uno": "arduino:avr:uno",
        "Arduino Mega": "arduino:avr:mega",
        "Arduino Leonardo": "arduino:avr:leonardo",
        "Arduino Nano": "arduino:avr:nano",
        "Arduino Micro": "arduino:avr:micro",
        "Arduino Pro Mini": "arduino:avr:pro",
        "Arduino Yun": "arduino:avr:yun",
    }

    def __init__(self, cli_manager):
        self.cli_manager = cli_manager
        self.system_key = get_system_key()

    def get_fqbn(self, board_name):
        return self.BOARDS.get(board_name, self.BOARDS["Arduino Uno"])

    def get_core(self, fqbn):
        parts = fqbn.split(":")
        return f"{parts[0]}:{parts[1]}" if len(parts) >= 2 else fqbn

    def compile_project(self, project_path, board_name, output_text, root, app):
        cli_path = self.cli_manager.cli_path
        if not cli_path:
            messagebox.showerror("Error", "arduino-cli path not specified")
            return

        fqbn = self.get_fqbn(board_name)
        core = self.get_core(fqbn)

        output_text.config(state="normal")
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Installing core {core}...\n")
        output_text.config(state="disabled")
        output_text.see(tk.END)
        root.update()

        success, message = self.cli_manager.install_core(core)
        if not success:
            output_text.config(state="normal")
            output_text.insert(tk.END, f"Error installing the core:\n{message}\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)
            return

        project_path = Path(project_path)
        project_dir = project_path.parent if project_path.is_file() else project_path
        build_dir = project_dir / "build"

        try:
            build_dir.mkdir(exist_ok=True)
            output_text.config(state="normal")
            output_text.insert(tk.END, f"Build directory created: {build_dir}\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)
        except PermissionError:
            output_text.config(state="normal")
            output_text.insert(tk.END, "Error: You don't have permissions to create the build directory. Try running as administrator.\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)
            messagebox.showerror("Permissions Error", "No permissions to create the build directory. Run the program as administrator.")
            return
        except Exception as e:
            output_text.config(state="normal")
            output_text.insert(tk.END, f"Error creating build directory: {str(e)}\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)
            return

        cmd = [
            str(cli_path),
            "compile",
            "--fqbn", fqbn,
            "--export-binaries",
            str(project_path)
        ]

        output_text.config(state="normal")
        output_text.insert(tk.END, f"Running command: {' '.join(cmd)}\n")
        output_text.config(state="disabled")
        output_text.see(tk.END)
        root.update()

        try:
            process = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output_text.config(state="normal")
            output_text.insert(tk.END, process.stdout)
            output_text.insert(tk.END, "Compilation successful! .hex file generated in the build folder.\n")
            output_text.insert(tk.END, f"Open build directory: {build_dir}\n", "link")
            output_text.tag_add("link_path", "end-2l", "end-1l")
            output_text.tag_config("link", foreground="#0288D1", underline=True)
            output_text.tag_bind("link", "<Button-1>", lambda event: app.open_directory(str(build_dir)))
            output_text.tag_bind("link", "<Enter>", lambda event: output_text.config(cursor="hand2"))
            output_text.tag_bind("link", "<Leave>", lambda event: output_text.config(cursor=""))
            output_text.config(state="disabled")
            output_text.see(tk.END)
        except subprocess.CalledProcessError as e:
            output_text.config(state="normal")
            output_text.insert(tk.END, f"Compilation failure:\n{e.stdout}\n{e.stderr}\n")
            output_text.config(state="disabled")
            output_text.see(tk.END)