#Windows

import locale
import platform
import subprocess
import os
import sys
from tkinter import messagebox
from venv import logger

class AudioManager:
    def __init__(self):
        self.audio_devices = self.get_audio_devices()

    def get_audio_devices(self):
        if platform.system() == 'Windows':
            return self._get_windows_audio_devices()
        elif platform.system() == 'Linux':
            return self._get_linux_audio_devices()
        else:
            return []

    def _get_windows_audio_devices(self):
        ffmpeg_path = self._get_ffmpeg_path()
        if not ffmpeg_path:
            return []
        
        cmd = [ffmpeg_path, "-list_devices", "true", "-f", "dshow", "-i", "dummy"]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8', errors='replace')
            lines = result.stderr.splitlines()
            devices = []
            
            for line in lines:
                if "audio" in line and len(line.split("\"")) > 1:
                    device_name = line.split("\"")[1]
                    normalized_name = self._normalize_audio_device_name(device_name)
                    devices.append(normalized_name)

            if not devices:
                logger.error("No active audio devices were found. Please check your audio settings.")
                messagebox.showerror("Error", "No active audio devices were found. Please check your audio settings.")

            return devices

        except subprocess.CalledProcessError as e:
            print(f"Error running FFmpeg (Audio): {e}")
            return []
        except FileNotFoundError:
            print(f"FFmpeg (Audio) not found at {ffmpeg_path}")
            return []

    def _normalize_audio_device_name(self, audio_device):
        system_locale = locale.getdefaultlocale()[0]

        encodings_to_try = ['utf-8', 'latin-1', 'cp1252']

        for encoding in encodings_to_try:
            try:
                audio_device = audio_device.encode(encoding).decode('utf-8')
                break
            except (UnicodeEncodeError, UnicodeDecodeError):
                continue
            
        return audio_device

    def _get_linux_audio_devices(self):
        cmd = ["pactl", "list", "sources"]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        lines = result.stdout.splitlines()
        devices = [line.split()[1] for line in lines if "Name:" in line and len(line.split()) > 1]
        return devices

    def _get_ffmpeg_path(self):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(os.path.abspath(__file__))

        if platform.system() == 'Windows':
            ffmpeg_path = os.path.join(base_path, 'ffmpeg_files', 'ffmpeg.exe')
        else:  # Linux
            ffmpeg_path = os.path.join(base_path, 'ffmpeg_files', 'ffmpeg')

        return ffmpeg_path if os.path.exists(ffmpeg_path) else None


    def refresh_devices(self):
        self.audio_devices = self.get_audio_devices()