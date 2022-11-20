# minecraft-pitch-control
A simple program to control Minecraft using flute/recorder by detecting its pitch.

## Youtube video
<a href="https://www.youtube.com/watch?v=fcOwzUq6cvs"><img src="https://i.ytimg.com/vi/fcOwzUq6cvs/maxresdefault.jpg" width="400"/></a>

# Requirements
1. Python 3
2. Visual Studio Build Tool 
2. Python library: `pyaudio`, `sys`, `numpy`, `aubio`, `pydirectinput`, `subprocess`, `pynput`

# Installation
1. Download Visual Studio [here](https://visualstudio.microsoft.com/downloads/). Install by clicking the file, then tick ``Desktop development with C++`` option. This is needed to make sure ``aubio`` work properly.
2. Install all required python libraries:
``
pip install pyaudio sys numpy aubio pydirectinput subprocess pynput
``

# Setup
- Run ``python detect.py``, blow every note from the flute/recorder and write down the number that appeared
- Change the number you see in line 60-90 of ``main.py`` using those new number. For example, if C note give you ``72.5``, you can input ``72 < pitch < 73`` to give room for error.
- Run ``python main.py``
- In Minecraft, you need to change mouse setting: Option > Control > Mouse Settings > Raw Input > OFF

That's all. 


