import tkinter as tk
from ui import ArduinoCLIApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ArduinoCLIApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error starting the application: {e}")