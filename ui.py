# Style constants
BACKGROUND_COLOR = "#1E1E1E"
FOREGROUND_COLOR = "#E0E0E0"
ACCENT_COLOR = "#0288D1"
ACCENT_COLOR_ACTIVE = "#03A9F4"
CARD_COLOR = "#1E1E1E"
BORDER_COLOR = "#FFFFF0"
PADDING = 10
FONT_DEFAULT = ("Helvetica", 10)
FONT_BOLD = ("Helvetica", 10, "bold")

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from arduino_cli import ArduinoCLIManager
from compiler import ProjectCompiler
from config import ConfigManager
import platform
import sys
from utils import get_system_key

class ArduinoCLIApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATphonOS - INO to HEX Compiler")
        self.root.geometry("700x500")
        self.root.configure(bg=BACKGROUND_COLOR)
        self.root.resizable(False, False)

        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)

        icon_ico_path = os.path.join(base_path, "icon", "logo_app.ico")
        print(f"Searching icon_ico_path: {icon_ico_path} - Exist: {os.path.exists(icon_ico_path)}")
        if os.path.exists(icon_ico_path):
            try:
                self.root.iconbitmap(default=icon_ico_path)
                print(f"Icon set with iconbitmap from: {icon_ico_path}")
            except tk.TclError as e:
                print(f"Error iconbitmap: {e}")
        else:
            print("logo_app.ico not found")

        self.system_key = get_system_key()
        print(f"System detected: {self.system_key}")

        self.config_manager = ConfigManager()
        self.cli_manager = ArduinoCLIManager(self.config_manager)
        self.compiler = ProjectCompiler(self.cli_manager)

        self.project_path = tk.StringVar()
        self.board_name = tk.StringVar(value="Arduino Uno")
        cli_name = f"arduino-cli-{self.system_key}" if platform.system() != "Windows" else f"arduino-cli-{self.system_key}.exe"
        default_cli_path = os.path.join(os.path.dirname(__file__), cli_name)
        self.cli_path = tk.StringVar(value=self.config_manager.cli_path or default_cli_path)

        self.create_widgets()
        self.apply_styles()

    def create_widgets(self):
        project_frame = ttk.LabelFrame(self.root, padding=PADDING, style="Custom.TLabelframe")
        project_frame.pack(fill="x", padx=PADDING, pady=PADDING//2)

        ttk.Label(project_frame, text="Project Path:", font=FONT_DEFAULT, foreground=FOREGROUND_COLOR, style="Custom.TLabel").grid(row=0, column=0, padx=PADDING//2, pady=PADDING//2)
        ttk.Entry(project_frame, textvariable=self.project_path, width=50, style="Custom.TEntry").grid(row=0, column=1, padx=PADDING//2, pady=PADDING//2)
        ttk.Button(project_frame, text="Browse File", command=self.browse_file, style="Custom.TButton").grid(row=0, column=2, padx=PADDING//2, pady=PADDING//2)
        ttk.Button(project_frame, text="Browse Project Folder", command=self.browse_folder, style="Custom.TButton").grid(row=0, column=3, padx=PADDING//2, pady=PADDING//2)

        board_frame = ttk.LabelFrame(self.root, padding=PADDING, style="Custom.TLabelframe")
        board_frame.pack(fill="x", padx=PADDING, pady=PADDING//2)

        ttk.Label(board_frame, text="Select Board:", font=FONT_DEFAULT, foreground=FOREGROUND_COLOR, style="Custom.TLabel").grid(row=0, column=0, padx=PADDING//2, pady=PADDING//2)
        board_names = list(self.compiler.BOARDS.keys())
        max_length = max(len(name) for name in board_names)
        board_combobox = ttk.Combobox(board_frame, textvariable=self.board_name, values=board_names, state="readonly", style="Custom.TCombobox", width=max_length + 2)
        board_combobox.grid(row=0, column=1, padx=PADDING//2, pady=PADDING//2)
        board_combobox.current(0)
        self.board_name.set("Arduino Uno")
        self.root.update()

        config_frame = ttk.LabelFrame(self.root, padding=PADDING, style="Custom.TLabelframe")
        config_frame.pack(fill="x", padx=PADDING, pady=PADDING//2)

        ttk.Label(config_frame, text="Arduino CLI Path:", font=FONT_DEFAULT, foreground=FOREGROUND_COLOR, style="Custom.TLabel").grid(row=0, column=0, padx=PADDING//2, pady=PADDING//2)
        ttk.Entry(config_frame, textvariable=self.cli_path, width=50, style="Custom.TEntry").grid(row=0, column=1, padx=PADDING//2, pady=PADDING//2)
        ttk.Button(config_frame, text="Browse", command=self.browse_cli_path, style="Custom.TButton").grid(row=0, column=2, padx=PADDING//2, pady=PADDING//2)
        ttk.Button(config_frame, text="Save Config", command=self.save_config, style="Custom.TButton").grid(row=0, column=3, padx=PADDING//2, pady=PADDING//2)

        action_frame = ttk.Frame(self.root, padding=PADDING, style="Custom.TFrame")
        action_frame.pack(fill="x", padx=PADDING, pady=PADDING//2)

        ttk.Button(action_frame, text="Compile and Generate Hex", command=self.compile_project, style="Custom.TButton").pack(pady=PADDING//2)

        output_frame = ttk.LabelFrame(self.root, text="Output", padding=PADDING, style="Output.TLabelframe")
        output_frame.pack(fill="both", expand=True, padx=PADDING, pady=PADDING//2)

        output_inner_frame = ttk.Frame(output_frame)
        output_inner_frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(output_inner_frame, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.output_text = tk.Text(output_inner_frame, height=10, width=70, bg=BACKGROUND_COLOR, fg=FOREGROUND_COLOR, insertbackground=FOREGROUND_COLOR, font=FONT_DEFAULT, yscrollcommand=scrollbar.set, state="disabled")
        self.output_text.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar.config(command=self.output_text.yview)

        self.progress_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.progress_frame.pack(fill="x", padx=PADDING, pady=PADDING//2)
        self.progress_label = ttk.Label(self.progress_frame, text="", foreground=FOREGROUND_COLOR, background=BACKGROUND_COLOR)
        self.progress_label.pack(side=tk.LEFT)
        self.progress_bar = ttk.Progressbar(self.progress_frame, length=600, mode="determinate", style="Custom.Horizontal.TProgressbar")
        self.progress_bar.pack(side=tk.LEFT, fill="x", expand=True)

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Custom.TLabelframe", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, labeloutside=True, borderwidth=1, bordercolor=BORDER_COLOR)
        style.configure("Custom.TLabelframe.Label", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

        style.configure("Output.TLabelframe", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, labeloutside=True, borderwidth=0)
        style.configure("Output.TLabelframe.Label", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR)

        style.configure("Custom.TFrame", background=BACKGROUND_COLOR)
        style.configure("Custom.TButton", font=FONT_DEFAULT, padding=(3, 1), background=ACCENT_COLOR, foreground=FOREGROUND_COLOR, borderwidth=1, relief="flat")
        style.map("Custom.TButton", background=[("active", ACCENT_COLOR_ACTIVE)], foreground=[("active", FOREGROUND_COLOR)])
        style.configure("Custom.TEntry", fieldbackground=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, insertcolor=FOREGROUND_COLOR)
        style.configure("Custom.TCombobox", fieldbackground=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, background=BACKGROUND_COLOR, lightcolor=BACKGROUND_COLOR, darkcolor=BACKGROUND_COLOR, bordercolor=BACKGROUND_COLOR, arrowcolor=FOREGROUND_COLOR, selectbackground=ACCENT_COLOR, selectforeground=FOREGROUND_COLOR)
        style.map("Custom.TCombobox", fieldbackground=[("readonly", BACKGROUND_COLOR)], background=[("readonly", BACKGROUND_COLOR)], foreground=[("readonly", FOREGROUND_COLOR)], selectbackground=[("readonly", ACCENT_COLOR)], selectforeground=[("readonly", FOREGROUND_COLOR)])
        style.configure("Custom.TLabel", background=BACKGROUND_COLOR, foreground=FOREGROUND_COLOR, font=FONT_DEFAULT)
        style.configure("Custom.Horizontal.TProgressbar", background=ACCENT_COLOR, troughcolor=BACKGROUND_COLOR)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Arduino Files", "*.ino *.pde")])
        if file_path:
            self.project_path.set(file_path)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.project_path.set(folder_path)

    def browse_cli_path(self):
        filetypes = [("Executable Files", "*.exe" if platform.system() == "Windows" else "*")]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.cli_path.set(file_path)

    def save_config(self):
        self.config_manager.cli_path = self.cli_path.get()
        self.config_manager.save_config()
        self.cli_manager.update_cli_path(self.cli_path.get())
        messagebox.showinfo("Success", "Configuration saved successfully")

    def compile_project(self):
        if not self.project_path.get():
            messagebox.showerror("Error", "Please select a project file or folder")
            return
        self.compiler.compile_project(self.project_path.get(), self.board_name.get(), self.output_text, self.root, self)

    def open_directory(self, directory):
        system = platform.system()
        try:
            if system == "Windows":
                os.startfile(directory)
            elif system == "Darwin":
                subprocess.run(["open", directory])
            else:
                subprocess.run(["xdg-open", directory])
        except Exception as e:
            messagebox.showerror("Error", f"The directory could not be opened: {str(e)}")