# Mini Screen Recorder

An open-source screen and audio recorder for Windows and Linux.

<p align="center">
  <a href="https://i.postimg.cc/HLx0D8Jj/Mini-Screen-Rec-Linux.png"><img src="https://i.postimg.cc/HLx0D8Jj/Mini-Screen-Rec-Linux.png"></a>
</p>

## Required packages to run this app

- Python 3.x
- FFmpeg
- Pillow
- tkinter

## Features

- Select theme
- Set framerate
- Set bitrate
- Choose video codec
- Select output format
- Select audio device
- Select recording area

## Steps

1. Clone the repository from GitHub:

    ```bash
    git clone https://github.com/Lextrack/MiniScreenRecorder.git
    ```

2. Navigate to the project directory:

    ```bash
    cd MiniScreenRecorder
    ```

3. Run the app:

    ```bash
    python MiniScreenRecorder.py
    ```

## Installing FFmpeg

- **Windows**:
  1. Download `ffmpeg-release-full.7z` from [FFmpeg official website](https://www.gyan.dev/ffmpeg/builds/).
  2. Extract the downloaded file in a folder called "ffmpeg" on your C:\ drive.
  3. Add the base folder and the bin folder from the extracted files to your system's PATH.

  <p align="center">
  <a href="https://i.postimg.cc/nhtSMSty/ffmpeg-Install-Windows.png"><img src="https://i.postimg.cc/nhtSMSty/ffmpeg-Install-Windows.png"></a>
</p>

- **Linux**:
  1. Update the package index:
      ```bash
      sudo apt update
      ```
  2. Install FFmpeg:
      ```bash
      sudo apt install ffmpeg
      ```
  3. Verify the installation:
      ```bash
      ffmpeg -version
      ```

## License

This project is licensed under the MIT License. See the LICENSE file for details.
