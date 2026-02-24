1. Install [Pyhton](#)
2. Install depedency:
```python
pip install pygame pyinstaller
```
3. Create two files in same directory. First file as `Play_Music.py` and `Song.mp3` (You can download `SOng.mp3` file from internet).
## `Play_Music.py`:
```python
import os
import sys
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def resource_path(relative_path):
    """Get the absolute path to the resource, handling PyInstaller's temporary folder."""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def play_music():
    pygame.mixer.init()
    # Locate the embedded music file
    music_file = resource_path("song.mp3") 
    
    try:
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play()
        # Keep the script running while the music plays
        while pygame.mixer.music.get_busy():
            time.sleep(1)
    except Exception as e:
        print(f"Error playing music: {e}")
        input("Press Enter to exit...")

if __name__ == '__main__':
    play_music()
```

4. Compile into single `.exe` file. You can do this by typing following command in terminal.
```python
pyinstaller --onefile --noconsole --add-data "Song.mp3;." play_music.py
```

- `--onefile`: Bundles everything into a single `.exe`.
- `--noconsole`: Hides the black command prompt window while the music plays.
- `--add-data "Song.mp3;."`: Tells the compiler to embed your music file into the executable.

New directory will be created as `dist`, where you see `.exe` file, you can share this file your friends or where you wish to send.

---
You have been created `.exe` file successfully, but issues is if system's sound is muted while executing `.exe` file or volume is low then you can't hear anything. What is solution? You can override system's global settings through python library. Consider following steps:

**Step 1:** Install `pycaw` library.
```python
pip install pycaw comtypes
```

After installing `pycaw` library, you can modify `Play_Music.py` file as follow:

```python
import os

import sys

import time

import comtypes

from pycaw.pycaw import AudioUtilities

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame

  

def resource_path(relative_path):

    try:

        base_path = sys._MEIPASS

    except Exception:

        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

  

def force_max_volume():

    """Interacts with Windows API to unmute and set volume to 100%"""

    try:

        # Initialize the COM libraries for Windows API interaction

        comtypes.CoInitialize()

        # Get the primary speaker device

        device = AudioUtilities.GetSpeakers()

        # Access the volume interface directly (new syntax)

        volume = device.EndpointVolume

        # Unmute (0) and set scalar volume to 100% (1.0)

        volume.SetMute(0, None)

        volume.SetMasterVolumeLevelScalar(1.0, None)

    except Exception as e:

        print(f"\n[!] Volume Error: {e}\n")

    finally:

        # Clean up COM libraries

        comtypes.CoUninitialize()

  

def play_music():

    force_max_volume()

    pygame.mixer.init()

    music_file = resource_path("song.mp3")

    try:

        pygame.mixer.music.load(music_file)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():

            time.sleep(1)

    except Exception as e:

        print(f"\n[!] Audio Playback Error: {e}\n")

        input("Press Enter to exit...")

  

if __name__ == '__main__':

    play_music()
```
**Step 2:** Compile into `.exe` by following command:

```python
pyinstaller --onefile --noconsole --add-data "Song.mp3;." play_music.py
```

---
Every application deserves an `Icon` and `Name`, how can you add icon to your application? Well, don't worry I'm here to help you.

**Step 1:** Download and put `.ico` file in same directory where `Song.mp3`, `Play_Music.py` file exist.
**Step 2:** Now you know what to do in 2nd step, don't you? Relax! In 2nd step you can to run following command:
```python
pyinstaller --onefile --noconsole --name "SuperLoudMusic" --icon "my_icon.ico" --add-data "Song.mp3;." play_music.py
```
- `--name "SuperLoudMusic"`: This tells PyInstaller to name the final file `SuperLoudMusic.exe` instead of `play_music.exe`. You can change the text inside the quotes to whatever you like.
- `--icon "my_icon.ico"`: This embeds your custom `.ico` file directly into the executable.

>[!NOTE]
>### :warning: A Quick Note on Windows "Ghosting"
>Windows has a very stubborn "Icon Cache." Sometimes, after you compile the `.exe`, it might still look like the default blank application icon on _your_ computer.
>Don't panic! The icon is actually there. Windows is just loading an old, cached visual of the folder. To force Windows to show it:
>- Move the `.exe` file to your Desktop or a completely different folder.
>- **Or**, just send it to your friend. Because their computer has never seen the file before, the custom icon will appear perfectly for them immediately.