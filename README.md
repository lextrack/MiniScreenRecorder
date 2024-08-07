# Mini Screen Recorder

It's an open-source screen and audio recorder for Windows and Linux.

<p align="center">
  <a href="https://i.postimg.cc/"><img src="https://i.postimg.cc/TwNGNVCF/2024-07-31-20h19-14.png"></a>
</p>

## Requirements to run the application

### Windows Users

If you download the packaged .exe file from the [Releases](https://github.com/Lextrack/MiniScreenRecorder/releases) section, you **do not** need to install Python, FFmpeg, or any additional libraries. Everything is included in the executable.

### Linux Users

You need to have Python 3.x and FFmpeg installed on your system, beside the additional libraries.

### To run this app you must install these libraries

For Linux, run this in your terminal:

    ```bash
    pip install pillow mss numpy opencv-python screeninfo
    ```

    ```bash
    sudo apt-get update
    sudo apt-get install python3-pil.imagetk
    sudo apt-get install libjpeg-dev zlib1g-dev libpng-dev libgl1-mesa-glx
    ```

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

## Steps (Linux)

1. Clone the repository from GitHub

    ```bash
    git clone https://github.com/Lextrack/MiniScreenRecorder.git
    ```

2. Navigate to the project directory

    ```bash
    cd MiniScreenRecorder
    ```

3. Run the app on Linux:

    ```bash
    python3 miniscreenrecorderLinux.py
    ```

### Warning about User Account Control

To prevent Windows UAC prompts from interrupting recording, you should select the second-to-last option, which says "Notify me only when apps try to make changes to my computer (do not dim my desktop)". Or, if you want, completely disable it.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
