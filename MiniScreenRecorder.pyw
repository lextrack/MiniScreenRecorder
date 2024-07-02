import platform
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import datetime
import webbrowser
import time

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Screen Recorder")
        root.resizable(0, 0)

        self.set_dark_theme()

        self.audio_devices = self.get_audio_devices()

        self.set_icon()
        
        self.init_ui()

        self.create_output_folder()
        self.recording_process = None
        self.running = False
        self.elapsed_time = 0

    def set_icon(self):
        if platform.system() == 'Windows':
            self.root.iconbitmap('video.ico')
        elif platform.system() == 'Linux':
            self.icon = tk.PhotoImage(file='video.png')
            self.root.iconphoto(True, self.icon)
    
    def set_dark_theme(self):
        self.root.tk_setPalette(background="#2e2e2e", foreground="white", activeBackground="#1e1e1e", activeForeground="white")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TLabel", background="#2e2e2e", foreground="white")
        style.configure("TCombobox", fieldbackground="#1e1e1e", background="#2e2e2e", foreground="white")
        style.map("TCombobox", fieldbackground=[('readonly', '#1e1e1e')])
        style.configure("TButton", background="#1e1e1e", foreground="white")
        style.map("TButton", background=[('active', '#3e3e3e')], foreground=[('active', 'white')])
        
    def init_ui(self):
        self.fps_label = ttk.Label(self.root, text="Framerate:")
        self.fps_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fps_combo = ttk.Combobox(self.root, values=["30", "60"], width=25)
        self.fps_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.fps_combo.current(1)
        self.fps_combo.config(state="readonly")
        
        self.bitrate_label = ttk.Label(self.root, text="Bitrate:")
        self.bitrate_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.bitrate_combo = ttk.Combobox(self.root, values=["2000k", "4000k", "6000k", "8000k", "10000k", "15000k", "20000k", "30000k"], width=25)
        self.bitrate_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        self.bitrate_combo.current(0)
        self.bitrate_combo.config(state="readonly")
        
        self.audio_label = ttk.Label(self.root, text="Audio Device:")
        self.audio_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.audio_combo = ttk.Combobox(self.root, values=self.audio_devices, width=25)
        self.audio_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.audio_combo.config(state="readonly")

        if self.audio_devices:
            self.audio_combo.current(0)
        else:
            messagebox.showerror("Error", "No audio devices found.")
        
        self.start_btn = ttk.Button(self.root, text="Start Recording", command=self.start_recording)
        self.start_btn.grid(row=3, column=0, columnspan=2, pady=2)
        
        self.stop_btn = ttk.Button(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_btn.grid(row=4, column=0, columnspan=2, pady=2)
        self.stop_btn.config(state=tk.DISABLED)

        self.open_folder_btn = ttk.Button(self.root, text="Open Output Folder", command=self.open_output_folder)
        self.open_folder_btn.grid(row=5, column=0, columnspan=2, pady=2)

        self.timer_label = ttk.Label(self.root, text="00:00:00")
        self.timer_label.grid(row=6, column=0, columnspan=2, pady=10)
        self.timer_label.config(font=("Arial", 13))

    def create_output_folder(self):
        self.output_folder = os.path.join(os.getcwd(), "OutputFiles")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def get_audio_devices(self):
        if platform.system() == 'Windows':
            cmd = ["ffmpeg", "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            lines = result.stderr.splitlines()
            devices = []
            for line in lines:
                if "audio" in line:
                    parts = line.split("\"")
                    if len(parts) > 1:
                        devices.append(parts[1])
            return devices
        elif platform.system() == 'Linux':
            cmd = ["pactl", "list", "sources"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            lines = result.stdout.splitlines()
            devices = []
            for line in lines:
                if "Name:" in line:
                    parts = line.split()
                    if len(parts) > 1:
                        devices.append(parts[1])
            return devices

    def start_recording(self):
        video_name = f"Video.{datetime.datetime.now().strftime('%m-%d-%Y.%H.%M.%S')}.mp4"
        self.video_path = os.path.join(self.output_folder, video_name)
        
        fps = int(self.fps_combo.get())
        bitrate = self.bitrate_combo.get()

        audio_device = self.audio_combo.get()

        if platform.system() == 'Windows':
            ffmpeg_args = [
                "ffmpeg",
                "-f", "gdigrab",
                "-framerate", str(fps),
                "-i", "desktop",
                "-f", "dshow",
                "-i", f"audio={audio_device}",
                "-c:v", "libx264",
                "-b:v", bitrate,
                "-pix_fmt", "yuv420p",
                self.video_path
            ]
            creationflags = subprocess.CREATE_NO_WINDOW
        elif platform.system() == 'Linux':
            ffmpeg_args = [
                "ffmpeg",
                "-f", "x11grab",
                "-framerate", str(fps),
                "-i", os.getenv('DISPLAY'),
                "-f", "pulse",
                "-i", audio_device,
                "-c:v", "libx264",
                "-b:v", bitrate,
                "-pix_fmt", "yuv420p",
                self.video_path
            ]
            creationflags = 0 
        
        self.recording_process = subprocess.Popen(ffmpeg_args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE, universal_newlines=True, creationflags=creationflags)

        self.toggle_widgets(state=tk.DISABLED)

        self.start_timer()

        threading.Thread(target=self.read_ffmpeg_output, daemon=True).start()

    def read_ffmpeg_output(self):
        if self.recording_process:
            for stdout_line in iter(self.recording_process.stderr.readline, ""):
                print(stdout_line)
            if self.recording_process is not None:
                self.recording_process.stderr.close()

    def stop_recording(self):
        if self.recording_process:
            self.recording_process.communicate(input='q')
            self.recording_process.wait()
            self.recording_process = None

            self.toggle_widgets(state=tk.NORMAL)

            self.stop_timer()

    def toggle_widgets(self, state):
        if state == tk.DISABLED:
            self.fps_combo.config(state=state)
            self.bitrate_combo.config(state=state)
            self.audio_combo.config(state=state)
        else:
            self.fps_combo.config(state="readonly")
            self.bitrate_combo.config(state="readonly")
            self.audio_combo.config(state="readonly")

        self.start_btn.config(state=state)
        self.stop_btn.config(state=tk.NORMAL if state == tk.DISABLED else tk.DISABLED)

    def open_output_folder(self):
        webbrowser.open(self.output_folder)

    def start_timer(self):
        self.running = True
        self.elapsed_time = 0
        self.update_timer()

    def stop_timer(self):
        self.running = False
        self.timer_label.config(text="00:00:00", foreground="white")

    def update_timer(self):
        if self.running:
            self.elapsed_time += 1
            elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.timer_label.config(text=elapsed_time_str, foreground="red")
            self.root.after(1000, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
