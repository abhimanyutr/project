import os
import eel
import time
import subprocess
import threading
import cv2
from engine.features import *
from engine.command import *
from engine.auth import recoganize

def start():
    eel.init("www")
    playAssistantSound()

    @eel.expose
    def init():
        subprocess.call([r'device.bat'])
        eel.hideLoader()
        speak("Ready for Face Authentication")

        auth_result = [None]  # Store authentication result
        auth_done = threading.Event()  # Event to track authentication completion

        def authenticate():
            auth_result[0] = recoganize.AuthenticateFace()
            auth_done.set()  # Mark authentication as completed

        # Start authentication in a separate thread
        auth_thread = threading.Thread(target=authenticate)
        auth_thread.daemon = True  # Ensure it stops if the main process exits
        auth_thread.start()

        # Wait for up to 10 seconds
        auth_done.wait(timeout=10)

        # If authentication is still running, force close it
        if not auth_done.is_set():
            speak("Face Authentication Failed. No face detected.")
            cv2.destroyAllWindows()  # Close OpenCV windows
            eel.hideFaceAuth()
            os.system("taskkill /IM chrome.exe /F")  # Close Chrome

        elif auth_result[0] == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can I help you?")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Failed.")
            cv2.destroyAllWindows()  # Ensure OpenCV windows are closed

        # Final cleanup to ensure everything closes
        cv2.destroyAllWindows()

    os.system('start chrome --app="http://localhost:8000/index.html" --auto-open-devtools-for-tabs"')
    eel.start('index.html', mode=None, host='localhost', block=True)