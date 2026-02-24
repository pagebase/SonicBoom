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