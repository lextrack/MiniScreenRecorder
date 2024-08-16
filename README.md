# Mini Screen Recorder

It's an open-source screen and audio recorder for Windows and Linux.

<p align="center">
  <a href="https://i.postimg.cc/"><img src="https://i.postimg.cc/TwNGNVCF/2024-07-31-20h19-14.png"></a>
</p>

## Features

- Select theme
- Set frame rate
- Set bitrate
- Choose video codec
- Select output format
- Select audio device
- Select recording area
- Support for multiple monitors
- Multi-language support

## Video Demo

Just a simple gameplay recorded with this app. Click the badge to watch the video:

[![Watch on YouTube](https://img.shields.io/badge/YouTube-Watch%20Video-red?style=for-the-badge&logo=youtube)](https://youtu.be/7Ji-maVmPac)

## Requirements to run the application

### Windows Users

If you download the packaged .exe file from the [Releases](https://github.com/Lextrack/MiniScreenRecorder/releases) section, you **do not** need to install Python, FFmpeg, or any additional libraries. Everything is included in the executable.

### Linux Users

You need to have Python 3.x and FFmpeg installed on your system, beside the additional libraries.

### To run this app you must install these libraries

For Linux, run this in your terminal:

    sudo apt-get update
    pip install pillow mss numpy opencv-python screeninfo
    sudo apt-get install python3-pil.imagetk

## How to install FFmpeg for Linux

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

## Steps (Linux)

1. Clone the repository from GitHub

    ```bash
    git clone https://github.com/Lextrack/MiniScreenRecorder.git
    ```

2. Navigate to the project directory

    ```bash
    cd MiniScreenRecorder
    ```

3. Run the app:

    ```bash
    python3 miniscreenrecorderLinux.py
    ```

### Warning about User Account Control

To prevent Windows UAC prompts from interrupting recording, you should select the second-to-last option, which says "Notify me only when apps try to make changes to my computer (do not dim my desktop)". Or, if you want, completely disable it.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
