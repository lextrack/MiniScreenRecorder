#WINDOWS

import json
import platform
import sys
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import threading
import os
import datetime
import webbrowser
import time
import mss
import numpy as np
import cv2
import logging

from audio_manager import AudioManager
from themes import set_dark_theme, set_light_theme, set_dark_blue_theme, set_light_green_theme, set_purple_theme, set_starry_night_theme
from translation_manager import TranslationManager
from area_selector import AreaSelector
from logging_config import setup_logging
from configparser import ConfigParser
from screeninfo import get_monitors
from PIL import ImageGrab, Image, ImageTk
from venv import logger

logger = setup_logging()

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.initialize_ffmpeg()
        logger.info("THE APP WAS OPEN")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.title("Mini Screen Recorder")
        root.resizable(0, 0)

        self.config = ConfigParser()
        self.config_file = 'config.ini'
        self.load_config()

        self.translation_manager = TranslationManager(self.config.get('Settings', 'language', fallback='en-US'))
        self.set_theme(self.config.get('Settings', 'theme', fallback='dark'))

        self.audio_manager = AudioManager()
        self.audio_devices = self.audio_manager.audio_devices
        if len(self.audio_devices) == 0:
            messagebox.showerror("Error", "No audio devices.")
            return

        self.monitors = self.get_monitors()
        if len(self.monitors) == 0:
            messagebox.showerror("Error", "No monitors found.")
            return

        self.set_icon()

        self.init_ui()

        self.create_output_folder()
        self.recording_process = None
        self.running = False
        self.elapsed_time = 0
        self.record_area = None
        self.area_selector = AreaSelector(root)
        self.preview_window = None
        self.preview_running = False

        self.current_video_part = 0
        self.video_parts = []

    def t(self, key):
        return self.translation_manager.t(key)

    def set_icon(self):
        if platform.system() == 'Windows':
            self.root.iconbitmap('video.ico')
        elif platform.system() == 'Linux':
            self.icon = tk.PhotoImage(file='video.png')
            self.root.iconphoto(True, self.icon)

    def change_theme(self, event=None):
        theme = self.theme_combo.get().lower()
        self.set_theme(theme)
        self.save_config()

    def set_theme(self, theme):
        if theme == "dark":
            set_dark_theme(self.root)
        elif theme == "light":
            set_light_theme(self.root)
        elif theme == "dark blue":
            set_dark_blue_theme(self.root)
        elif theme == "light green":
            set_light_green_theme(self.root)
        elif theme == "purple":
            set_purple_theme(self.root)
        elif theme == "starry night":
            set_starry_night_theme(self.root)

        self.current_theme = theme

    def save_config(self, event=None):
        self.config['Settings'] = {
            'language': self.translation_manager.language,
            'theme': self.theme_combo.get().lower(),
            'monitor': self.monitor_combo.current(),
            'fps': self.fps_combo.current(),
            'bitrate': self.bitrate_combo.current(),
            'codec': self.codec_combo.current(),
            'format': self.format_combo.current(),
            'audio': self.audio_combo.current()
        }
        with open(self.config_file, 'w') as configfile:
            self.config.write(configfile)

    def load_config(self):
        if os.path.exists(self.config_file):
            self.config.read(self.config_file)
        else:
            self.config['Settings'] = {
                'language': 'en-US',
                'theme': 'dark',
                'monitor': 0,
                'fps': 1,
                'bitrate': 0,
                'codec': 0,
                'format': 0,
                'audio': 0
            }
            with open(self.config_file, 'w') as configfile:
                self.config.write(configfile)

    def change_language(self, event=None):
        selected_language = self.language_combo.get()
        language_map = {
            'English': 'en-US',
            'Español': 'es-CL',
            '简体中文': 'zh-Hans',
            "繁體中文": 'zh-Hant',
            'Italiano': 'it-IT',
            'Français': 'fr-FR',
            'हिन्दी': 'hi-IN',
            'Deutsch': 'de-DE',
            'Português': 'pt-BR',
            'Pусский': 'ru-RU',
            "日本語": 'ja-JP',
            "한국어": 'ko-KR',
            "Polski": 'pl-PL',
            "العربية": 'ar',
            "Tiếng Việt": 'vi-VN',
            "українська мова": 'uk-UA',
            "ไทยกลาง": 'th-TH',
            "Filipino": 'fil-PH',
            "Türkçe": 'tr-TR'
        }
        new_language = language_map.get(selected_language, 'en-US')
        
        if new_language != self.translation_manager.language:
            self.translation_manager.change_language(new_language)
            self.save_config()
            messagebox.showinfo(self.t("language_change"), self.t("warning_change_lang"))
            self.root.destroy()
            os.execl(sys.executable, sys.executable, *sys.argv)

    def init_ui(self):
        self.language_label = ttk.Label(self.root, text=self.t("Language") + ":")
        self.language_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.language_combo = ttk.Combobox(self.root, values=["English", "Español", "简体中文", "繁體中文", "Italiano", "Français", "हिन्दी", "Deutsch", "Português", "Pусский", 
                                                              "日本語", "한국어", "Polski", "العربية", "Tiếng Việt", "українська мова", "ไทยกลาง", "Filipino", "Türkçe"], width=25)
        self.language_combo.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.language_combo.current(["en-US", "es-CL", "zh-Hans", "zh-Hant", "it-IT", "fr-FR", "hi-IN", "de-DE", "pt-BR", "ru-RU", 
                                     "ja-JP", "ko-KR", "pl-PL", "ar", "vi-VN", "uk-UA", "th-TH", "fil-PH", "tr-TR"].index(self.translation_manager.language))
        self.language_combo.config(state="readonly")
        self.language_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        self.theme_label = ttk.Label(self.root, text=self.t("theme") + ":")
        self.theme_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.theme_combo = ttk.Combobox(self.root, values=["Dark", "Light", "Dark Blue", "Light Green", "Purple", "Starry Night"], width=25)
        self.theme_combo.grid(row=1, column=1, padx=10, pady=5, sticky="w")
        current_theme = self.config.get('Settings', 'theme', fallback='dark')
        theme_index = {"dark": 0, "light": 1, "dark blue": 2, "light green": 3, "purple": 4, "starry night": 5}.get(current_theme, 0)
        self.theme_combo.current(theme_index)
        self.theme_combo.config(state="readonly")
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        self.monitor_label = ttk.Label(self.root, text=self.t("monitor") + ":")
        self.monitor_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.monitor_combo = ttk.Combobox(self.root, values=[f"Monitor {i+1}: ({monitor.width}x{monitor.height})" for i, monitor in enumerate(self.monitors)], width=25)
        self.monitor_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.monitor_combo.current(0)
        self.monitor_combo.config(state="readonly")
        self.monitor_combo.bind("<<ComboboxSelected>>", self.on_monitor_change)

        self.fps_label = ttk.Label(self.root, text=self.t("framerate") + ":")
        self.fps_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.fps_combo = ttk.Combobox(self.root, values=["30", "60"], width=25)
        self.fps_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.fps_combo.current(self.config.getint('Settings', 'fps'))
        self.fps_combo.config(state="readonly")
        self.fps_combo.bind("<<ComboboxSelected>>", self.save_config)
        
        self.bitrate_label = ttk.Label(self.root, text=self.t("bitrate") + ":")
        self.bitrate_label.grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.bitrate_combo = ttk.Combobox(self.root, values=["1000k", "2000k", "4000k", "6000k", "8000k", "10000k", "15000k", "20000k"], width=25)
        self.bitrate_combo.grid(row=4, column=1, padx=10, pady=5, sticky="w")
        self.bitrate_combo.current(self.config.getint('Settings', 'bitrate'))
        self.bitrate_combo.config(state="readonly")
        self.bitrate_combo.bind("<<ComboboxSelected>>", self.save_config)

        self.codec_label = ttk.Label(self.root, text=self.t("video_codec") + ":")
        self.codec_label.grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.codec_combo = ttk.Combobox(self.root, values=["libx264", "libx265"], width=25)
        self.codec_combo.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.codec_combo.current(self.config.getint('Settings', 'codec'))
        self.codec_combo.config(state="readonly")
        self.codec_combo.bind("<<ComboboxSelected>>", self.save_config)

        self.format_label = ttk.Label(self.root, text=self.t("output_format") + ":")
        self.format_label.grid(row=6, column=0, padx=10, pady=5, sticky="e")
        self.format_combo = ttk.Combobox(self.root, values=["mkv", "mp4"], width=25)
        self.format_combo.grid(row=6, column=1, padx=10, pady=5, sticky="w")
        self.format_combo.current(self.config.getint('Settings', 'format'))
        self.format_combo.config(state="readonly")
        self.format_combo.bind("<<ComboboxSelected>>", self.save_config)
        
        self.audio_label = ttk.Label(self.root, text=self.t("audio_device") + ":")
        self.audio_label.grid(row=7, column=0, padx=10, pady=5, sticky="e")
        self.audio_combo = ttk.Combobox(self.root, values=self.audio_devices, width=25)
        self.audio_combo.grid(row=7, column=1, padx=10, pady=5, sticky="w")
        self.audio_combo.current(self.config.getint('Settings', 'audio'))
        self.audio_combo.config(state="readonly")
        self.audio_combo.bind("<<ComboboxSelected>>", self.save_config)
        if self.audio_devices:
            self.audio_combo.current(0)
        else:
            messagebox.showerror(self.t("error"), self.t("error_no_audio_devices"))

        self.volume_label = ttk.Label(self.root, text=self.t("volume") + ":")
        self.volume_label.grid(row=8, column=0, padx=10, pady=5, sticky="e")
        self.volume_scale = ttk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.volume_scale.set(100)
        self.volume_scale.grid(row=8, column=1, padx=10, pady=5, sticky="w")

        self.toggle_btn = ttk.Button(self.root, text=self.t("start_recording"), command=self.toggle_recording)
        self.toggle_btn.grid(row=9, column=0, columnspan=2, pady=2)

        self.open_folder_btn = ttk.Button(self.root, text=self.t("open_output_folder"), command=self.open_output_folder)
        self.open_folder_btn.grid(row=10, column=0, columnspan=2, pady=2)

        self.select_area_btn = ttk.Button(self.root, text=self.t("select_recording_area"), command=self.select_area)
        self.select_area_btn.grid(row=11, column=0, columnspan=2, pady=2)

        self.preview_btn = ttk.Button(self.root, text=self.t("start_preview"), command=self.toggle_preview_monitor)
        self.preview_btn.grid(row=12, column=0, columnspan=2, pady=2)

        self.preview_frame = ttk.Frame(self.root)
        self.preview_frame.grid(row=13, column=0, columnspan=2, pady=5, padx=10)
        self.preview_label = ttk.Label(self.preview_frame)
        self.preview_label.pack()

        self.timer_label = ttk.Label(self.root, text="00:00:00")
        self.timer_label.grid(row=14, column=0, columnspan=2, pady=10)
        self.timer_label.config(font=("Arial", 13))

        self.info_btn = ttk.Button(self.root, text=self.t("about"), command=self.show_info)
        self.info_btn.grid(row=15, column=0, columnspan=2, pady=2)

        self.status_label = ttk.Label(self.root, text=self.t("status_ready"))
        self.status_label.grid(row=16, column=0, columnspan=2, pady=5)
        self.status_label.config(font=("Arial", 10))

    def refresh_audio_devices(self):
        self.audio_manager.refresh_devices()
        self.audio_combo['values'] = self.audio_manager.audio_devices
        self.audio_combo.current(0)

    def toggle_preview_monitor(self):
        if self.preview_running:
            self.close_preview()
            self.preview_btn.config(text=self.t("start_preview"))
        else:
            self.preview_running = True
            self.update_preview_loop()
            self.preview_btn.config(text=self.t("stop_preview"))

    def update_preview_loop(self):
        self.preview_thread = threading.Thread(target=self._update_preview_thread, daemon=True)
        self.preview_thread.start()

    def _update_preview_thread(self):
        with mss.mss() as sct:
            while self.preview_running:
                try:
                    if self.monitor_combo and self.monitor_combo.winfo_exists():
                        monitor_index = self.monitor_combo.current()
                    else:
                        break
                    
                    if monitor_index < len(sct.monitors) - 1:
                        monitor = sct.monitors[monitor_index + 1]
                    else:
                        return

                    screenshot = np.array(sct.grab(monitor))
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGBA2RGB)
                    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_BGR2RGB)

                    max_size = (400, 240)
                    screenshot = cv2.resize(screenshot, max_size, interpolation=cv2.INTER_AREA)

                    image = Image.fromarray(screenshot)
                    tk_image = ImageTk.PhotoImage(image=image)

                    if self.preview_label and self.preview_label.winfo_exists():
                        self.root.after(0, self._update_preview_label, tk_image)

                    time.sleep(0.03)
                except tk.TclError:
                    break
                
    def _update_preview_label(self, tk_image):
        if self.preview_running:
            self.preview_label.config(image=tk_image)
            self.preview_label.image = tk_image

    def close_preview(self):
        self.preview_running = False
        if hasattr(self, 'preview_thread'):
            self.preview_thread.join(timeout=1.0)
        self.preview_label.config(image='')
        self.preview_label.image = None

    def on_closing(self):
        self.close_preview()
        self.root.quit()
        self.root.destroy()

    def on_monitor_change(self, event=None):
        if self.running:
            self.stop_current_recording()
            self.start_new_recording()
        self.save_config()

    def start_new_recording(self):
        self.create_new_video_file()
        self.start_recording(continue_timer=True)

    def create_new_video_file(self):
        video_name = f"Video_part{self.current_video_part}.{datetime.datetime.now().strftime('%m-%d-%Y.%H.%M.%S')}.mkv"
        self.video_path = os.path.join(self.output_folder, video_name)

    def stop_current_recording(self):
        if self.recording_process:
            try:
                self.recording_process.stdin.write('q')
                self.recording_process.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
            try:
                self.recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.recording_process.terminate()
                try:
                    self.recording_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.recording_process.kill()

            if os.path.exists(self.video_path) and os.path.getsize(self.video_path) > 0:
                self.video_parts.append(self.video_path)
            self.current_video_part += 1
            self.recording_process = None

    def toggle_recording(self):
        if not self.running:
            self.start_recording()
            self.toggle_btn.config(text=self.t("stop_recording"))
        else:
            self.stop_recording()
            self.toggle_btn.config(text=self.t("start_recording"))

    def create_output_folder(self):
        self.output_folder = os.path.join(os.getcwd(), "OutputFiles")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def get_monitors(self):
        return get_monitors()

    def select_area(self):
        self.area_selector.select_area(self.set_record_area)

    def set_record_area(self, record_area):
        self.record_area = record_area
        if self.record_area:
            self.preview_record_area()

    def preview_record_area(self):
        x1, y1, x2, y2 = self.record_area
        width = x2 - x1
        height = y2 - y1
        preview_window = tk.Toplevel(self.root)
        preview_window.geometry(f"{width}x{height}+{x1}+{y1}")
        preview_window.overrideredirect(True)
        preview_window.attributes('-alpha', 0.3)
        preview_canvas = tk.Canvas(preview_window, width=width, height=height)
        preview_canvas.pack()
        preview_canvas.create_rectangle(0, 0, width, height, outline='red', width=2)
        preview_window.after(1000, preview_window.destroy)

    def get_ffmpeg_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        if platform.system() == 'Windows':
            ffmpeg_path = os.path.join(base_path, 'ffmpeg_files', 'ffmpeg.exe')
        else:  # Linux
            ffmpeg_path = os.path.join(base_path, 'ffmpeg_files', 'ffmpeg')

        print(f"FFmpeg path: {ffmpeg_path}")
        print(f"FFmpeg exists: {os.path.exists(ffmpeg_path)}")

        return ffmpeg_path
        
    def start_recording(self, continue_timer=False):
        video_name = f"Video.{datetime.datetime.now().strftime('%m-%d-%Y.%H.%M.%S')}.{self.format_combo.get()}"
        self.video_path = os.path.join(self.output_folder, video_name)

        fps = int(self.fps_combo.get())
        bitrate = self.bitrate_combo.get()
        codec = self.codec_combo.get()
        audio_device = self.audio_combo.get()
        volume = self.volume_scale.get()

        audio_device = self.audio_manager._normalize_audio_device_name(audio_device)

        monitor_index = self.monitor_combo.current()
        monitor = self.monitors[monitor_index]

        if self.record_area:
            x1, y1, x2, y2 = self.record_area
            width = x2 - x1
            height = y2 - y1

            if width <= 0 or height <= 0:
                messagebox.showerror(self.t("error"), self.t("error_invalid_area"))
                self.update_status_label_error_recording(self.t("error_recording"))
                self.stop_recording()
                self.stop_timer()
                self.toggle_widgets()
                return

            width -= width % 2
            height -= height % 2
            if width <= 0 or height <= 0:
                messagebox.showerror(self.t("error"), self.t("error_adjusted_area"))
                self.update_status_label_error_recording(self.t("error_recording"))
                self.stop_recording()
                self.stop_timer()
                self.toggle_widgets()
                return
        else:
            x1 = y1 = 0
            width = monitor.width
            height = monitor.height

        ffmpeg_path = self.get_ffmpeg_path()
        ffmpeg_args = [
            ffmpeg_path,
            "-f", "gdigrab",
            "-framerate", str(fps),
            "-offset_x", str(x1 + monitor.x),
            "-offset_y", str(y1 + monitor.y),
            "-video_size", f"{width}x{height}",
            "-i", "desktop",
            "-f", "dshow",
            "-i", f"audio={audio_device}",
            "-filter:a", f"volume={volume/100}",
            "-threads", "0",
            "-pix_fmt", "yuv420p",
            "-loglevel", "info",
            "-hide_banner"
        ]

        if codec == "libx264":
            ffmpeg_args.extend([
                "-c:v", "libx264",
                "-preset", "veryfast",
                "-b:v", bitrate,
            ])
        elif codec == "libx265":
            ffmpeg_args.extend([
                "-c:v", "libx265",
                "-preset", "medium",
                "-b:v", bitrate,
            ])
        else:
            ffmpeg_args.extend([
                "-c:v", codec,
                "-b:v", bitrate,
            ])

        ffmpeg_args.append(self.video_path)

        creationflags = subprocess.CREATE_NO_WINDOW
        try:
            self.recording_process = subprocess.Popen(
                ffmpeg_args, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, 
                universal_newlines=True,
                creationflags=creationflags
            )
        except FileNotFoundError as e:
            messagebox.showerror("Error", f"FFmpeg not found.")
            self.update_status_label_error_recording(self.t("error_recording"))
            logger.error(f"FFmpeg not found: {e}")
            self.stop_recording()
            self.stop_timer()
            self.toggle_widgets()
        except Exception as e:
            messagebox.showerror("Error", f"An error has occurred.")
            self.update_status_label_error_recording(self.t("error_recording"))
            logger.error(f"Error starting recording: {e}")
            self.stop_recording()
            self.stop_timer()
            self.toggle_widgets()

        self.toggle_widgets(recording=True)
        self.status_label.config(text=self.t("status_recording"))

        if not continue_timer:
            self.start_timer()

        threading.Thread(target=self.read_ffmpeg_output, daemon=True).start()

    def update_status_label_error_recording(self, text):
        self.status_label.after(0, lambda: self.status_label.config(text=text))

    def stop_recording(self):
        if self.recording_process:
            try:
                self.recording_process.stdin.write('q')
                self.recording_process.stdin.flush()
            except (BrokenPipeError, OSError):
                pass
            try:
                self.recording_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.recording_process.terminate()
                try:
                    self.recording_process.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    self.recording_process.kill()

            for pipe in [self.recording_process.stdin, self.recording_process.stdout, self.recording_process.stderr]:
                try:
                    pipe.close()
                except:
                    pass

            if os.path.exists(self.video_path) and os.path.getsize(self.video_path) > 0:
                self.video_parts.append(self.video_path)

            self.recording_process = None

        self.concat_video_parts()
        
        self.toggle_widgets(recording=False)
        self.stop_timer()
        self.status_label.config(text=self.t("status_ready"))
        
        self.record_area = None
        self.running = False

    def read_ffmpeg_output(self):
        if self.recording_process:
            buffer = []
            try:
                for stdout_line in iter(self.recording_process.stderr.readline, ""):
                    buffer.append(stdout_line)
                    if len(buffer) >= 100:
                        logger.error("".join(buffer))
                        buffer = []
            except BrokenPipeError:
                logger.warning("FFMPEG PROCESS HAS BEEN CLOSED")
            except Exception as e:
                logger.error(f"ERROR READING FFMPEG OUTPUT: {e}")
                self.update_status_label_error_recording(self.t("error_recording"))
            finally:
                if buffer:
                    logger.info("".join(buffer))
                if self.recording_process and self.recording_process.stderr:
                    self.recording_process.stderr.close()

    def initialize_ffmpeg(self):
        ffmpeg_path = self.get_ffmpeg_path()
        if not os.path.exists(ffmpeg_path):
            logger.error("FFmpeg not found.")
            self.update_status_label_error_recording(self.t("error_recording"))
            messagebox.showerror("Error", f"FFmpeg not found.")
            sys.exit(1)
        logger.info("FFmpeg was found.")

    def concat_video_parts(self):
        if len(self.video_parts) > 0:
            ffmpeg_path = self.get_ffmpeg_path()
            concat_file = os.path.join(self.output_folder, "concat_list.txt")
            output_file = os.path.join(self.output_folder, f"Video_{datetime.datetime.now().strftime('%m-%d-%Y.%H.%M.%S')}.{self.format_combo.get()}")

            with open(concat_file, 'w') as f:
                for video in self.video_parts:
                    f.write(f"file '{os.path.abspath(video)}'\n")

            concat_command = [
                ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy", 
                "-movflags", "+faststart",
                output_file
            ]

            try:
                print(f"Executing command: {' '.join(concat_command)}")
                result = subprocess.run(concat_command, check=True, capture_output=True, text=True)
                print(f"FFmpeg output: {result.stderr}")

                os.remove(concat_file)
                for video in self.video_parts:
                    if os.path.exists(video):
                        os.remove(video)

            except subprocess.CalledProcessError as e:
                error_message = e.stderr if e.stderr else str(e)
                messagebox.showerror(self.t("error"), self.t("error_concat_video").format(error=error_message))
                logger.error(f"ERROR MERGING VIDEO: {error_message}")
                self.update_status_label_error_recording(self.t("error_recording"))

            self.video_parts = []
            self.current_video_part = 0

    def on_closing(self):
        self.close_preview()
        if self.running:
            if messagebox.askokcancel(self.t("warning"), self.t("warning_quit")):
                self.stop_recording()
                self.root.destroy()
        else:
            self.root.destroy()

    def toggle_widgets(self, recording):
        state = "disabled" if recording else "normal"
        readonly_state = "disabled" if recording else "readonly"
        
        #self.monitor_combo.config(state=readonly_state)
        self.fps_combo.config(state=readonly_state)
        self.bitrate_combo.config(state=readonly_state)
        self.codec_combo.config(state=readonly_state)
        self.format_combo.config(state=readonly_state)
        self.audio_combo.config(state=readonly_state)
        self.volume_scale.config(state=state)
        self.select_area_btn.config(state=state)
        self.language_combo.config(state=readonly_state)
        self.theme_combo.config(state=readonly_state)
        #self.preview_btn.config(state=state)
        #self.monitor_combo.config(state="disabled" if recording else "readonly")

        self.toggle_btn.config(text=self.t("stop_recording") if recording else self.t("start_recording"))

    def open_output_folder(self):
        if platform.system() == "Windows":
            os.startfile(self.output_folder)
        elif platform.system() == "Linux":
            subprocess.Popen(["xdg-open", self.output_folder])

    def start_timer(self):
        self.running = True
        self.elapsed_time = 0
        self.update_timer()

    def stop_timer(self):
        self.running = False
        if self.current_theme == "light":
            self.timer_label.config(text="00:00:00", foreground="black")
        else:
            self.timer_label.config(text="00:00:00", foreground="white")

    def update_timer(self):
        if self.running:
            self.elapsed_time += 1
            elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(self.elapsed_time))
            self.timer_label.config(text=elapsed_time_str, foreground="red")
            self.root.after(1000, self.update_timer)

    def show_info(self):
        info_window = tk.Toplevel(self.root)
        info_window.title(self.t("about"))
        info_window.geometry("360x260")
        info_window.resizable(0, 0)

        text = self.t("version_info")

        if self.translation_manager.is_rtl:
            justify = tk.RIGHT
        else:
            justify = tk.LEFT

        text_widget = tk.Text(info_window, wrap=tk.WORD, padx=10, pady=10, bg=info_window.cget("bg"), bd=0, font=("Arial", 10))
        text_widget.insert(tk.END, text)
        text_widget.configure(state=tk.DISABLED) 
        text_widget.pack(fill=tk.BOTH, expand=True)

        text_widget.tag_configure("justify", justify=justify)
        text_widget.tag_add("justify", "1.0", tk.END)

    def reload_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.init_ui()

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ScreenRecorderApp(root)
        root.mainloop()
    except Exception as e:
        print(f"An error occurred: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        logger.error(f"AN ERROR OCCURRED: {e}")