#Windows

import platform
import subprocess
import os
import sys

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
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            lines = result.stderr.splitlines()
            devices = [line.split("\"")[1] for line in lines if "audio" in line and len(line.split("\"")) > 1]
            return devices
        except subprocess.CalledProcessError as e:
            print(f"Error running FFmpeg (Audio): {e}")
            return []
        except FileNotFoundError:
            print(f"FFmpeg (Audio) not found at {ffmpeg_path}")
            return []

    def _get_linux_audio_devices(self):
        cmd = ["pactl", "list", "sources"]
        result = subprocess.run(cmd, capture_output=True, text=True)
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
