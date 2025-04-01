import re
from pipes import quote
import struct
import subprocess
import time
from playsound import playsound
import eel
import os
import sqlite3
import webbrowser
import pyaudio
import pyautogui
import sys
import os
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
from hugchat import hugchat
from engine.helper import extract_yt_term,remove_words,extract_search_term
import pvporcupine

con = sqlite3.connect("alexa.db")
cursor = con.cursor()

# starting assistant sound
@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME,"")
    query = query.replace("open","")
    query = query.strip()
    query = query.lower()

    app_name = query

    if app_name:

        try:
            cursor.execute(
                'SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()
            print(f"Database sys_command result: {results}")  # Debug print
            
            if results:
                speak(f"Opening {app_name}")
                print(f"Opening path: {results[0][0]}")  # Debug print
                os.startfile(results[0][0])  # opening application

            else: 
                cursor.execute(
                'SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()
                print(f"Database web_command result: {results}")  # Debug print
                
                if results:
                    speak(f"Opening {app_name}")
                    print(f"Opening url: {results[0][0]}")  # Debug print
                    webbrowser.open(results[0][0])  # opening website

                else:
                    # Try to open the app using the system command
                    speak(f"Trying to open {app_name}")
                    try:
                        print(f"Running system command: start {app_name}")  # Debug print
                        os.system(f'start {app_name}')  # opening command in cmd
                    except Exception as e:
                        speak(f"Could not open {app_name}")
                        print(f"Error: {e}") #Debug print
        except Exception as e:
            speak(f"some thing went wrong:{e}")
            print(f"Database error: {e}")  # Show actual error


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing "+search_term+" on YouTube")
    kit.playonyt(search_term)


def SearchWebsite(query):
    #Extract search query and open the specific website"""
    search_term, website = extract_search_term(query)
    
    if search_term and website:
        speak(f"Searching {search_term} on {website}")
        search_url = f"https://www.{website}.com/search?q={search_term}"
        webbrowser.open(search_url)
    else:
        speak("Sorry, I couldn't understand the website or search term.")



def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0

   
def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        target_tab = 12
        j_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 7
        message = ''
        j_message = "calling to "+name

    else:
        target_tab = 6
        message = ''
        j_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(j_message)

# chat bot 
def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response

# android automation
def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(100, 1480)
    #start chat
    tapEvents(550, 1485)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(285, 470)
    # tap on input
    tapEvents(350, 1530)
    #message
    adbInput(message)
    #send
    tapEvents(645, 1000)
    speak("message send successfully to "+name)