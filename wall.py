import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import webbrowser
import platform

class DriverTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Driver Updater")
        self.root.geometry("900x600")

        ttk.Button(
            root,
            text="Listar Drivers",
            command=self.list_drivers
        ).pack(pady=5)

        ttk.Button(
            root,
            text="Detectar GPU",
            command=self.detect_gpu
        ).pack(pady=5)

        ttk.Button(
            root,
            text="Abrir Windows Update",
            command=self.windows_update
        ).pack(pady=5)

        self.output = scrolledtext.ScrolledText(root)
        self.output.pack(fill="both", expand=True)

    def write(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    def list_drivers(self):
        try:
            result = subprocess.check_output(
                "driverquery /v",
                shell=True,
                text=True,
                encoding="cp850",
                errors="ignore"
            )
            self.write(result)
        except Exception as e:
            self.write(str(e))

    def detect_gpu(self):
        try:
            result = subprocess.check_output(
                "wmic path win32_VideoController get name",
                shell=True,
                text=True,
                encoding="cp850",
                errors="ignore"
            )

            self.write(result)

            gpu = result.lower()

            if "nvidia" in gpu:
                webbrowser.open(
                    "https://www.nvidia.com/en-us/software/nvidia-app/"
                )

            elif "amd" in gpu or "radeon" in gpu:
                webbrowser.open(
                    "https://www.amd.com/en/support/download/drivers.html"
                )

            elif "intel" in gpu:
                webbrowser.open(
                    "https://www.intel.com/content/www/us/en/support/detect.html"
                )

        except Exception as e:
            self.write(str(e))

    def windows_update(self):
        subprocess.run(
            "start ms-settings:windowsupdate",
            shell=True
        )

root = tk.Tk()
app = DriverTool(root)
root.mainloop()