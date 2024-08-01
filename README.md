# Mini Screen Recorder

It's an open-source screen and audio recorder for Windows and Linux.

<p align="center">
  <a href="https://i.postimg.cc/"><img src="https://i.postimg.cc/TwNGNVCF/2024-07-31-20h19-14.png"></a>
</p>

## Software required to execute this app

- Python 3.x
- FFmpeg

### To run this app you must install these libraries
For Windows and Linux run this on your terminal:

    ```bash
    pip install pillow mss numpy opencv-python screeninfo
    ```
Additionally for Linux:

    ```bash
    sudo apt-get update
    sudo apt-get install python3-pil.imagetk
    sudo apt-get install libjpeg-dev zlib1g-dev libpng-dev libgl1-mesa-glx

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

## Steps

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
    python3 main.py
    ```
    Or in Windows (In the release section you can find a .exe for this app if you don't like the CMD)::

    ```bash
    python main.py
    ```

### Warning about User Account Control

To prevent Windows UAC prompts from interrupting recording, you should select the second-to-last option, which says "Notify me only when apps try to make changes to my computer (do not dim my desktop)". Or, if you want, completely disable it.

## How to install FFmpeg

- **Windows**:
  1. Download `ffmpeg-release-full.7z` from [FFmpeg official website](https://www.gyan.dev/ffmpeg/builds/).
  2. Extract the downloaded file in a folder called "ffmpeg" on your C:\ drive.
  3. Add the paths of the base folder and the bin folder of ffmpeg to the System Variables' PATH in Windows.

  <p align="center">
  <a href="https://i.postimg.cc/"><img src="https://i.postimg.cc/nhtSMSty/ffmpeg-Install-Windows.png"></a>
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
