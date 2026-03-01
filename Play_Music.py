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

def play_unstoppable_music():
    """Plays music while actively fighting the user to keep volume at 100%"""
    
    # Initialize Windows COM libraries
    comtypes.CoInitialize() 
    
    try:
        # Get the audio device and volume interface
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        
        # Initialize the audio mixer and load the song
        pygame.mixer.init()
        music_file = resource_path("song.mp3") 
        pygame.mixer.music.load(music_file)
        
        # Start the music
        pygame.mixer.music.play()
        
        # The Aggressive Loop: Keep running while the music is active
        while pygame.mixer.music.get_busy():
            # Constantly force unmute and 100% volume
            volume.SetMute(0, None) 
            volume.SetMasterVolumeLevelScalar(1.0, None)
            
            # Pause for just a fraction of a second before enforcing it again
            # This makes the volume slider instantly snap back to 100 if dragged down
            time.sleep(0.1) 
            
    except Exception as e:
        print(f"\n[!] Error: {e}\n")
    finally:
        # Clean up
        comtypes.CoUninitialize()

if __name__ == '__main__':
    play_unstoppable_music()