from cmath import e
import datetime
import webbrowser
import pyautogui
import pyttsx3 
import speech_recognition as sr 
import eel
import time
import re
import wikipedia
import pywhatkit as wk
import os


def speak(text):
  text = str(text)
  engine = pyttsx3.init('sapi5')
  voices = engine.getProperty('voices')
  engine.setProperty('voice', voices[1].id)
  engine.setProperty('rate', 174) 
  eel.DisplayMessage(text)
  engine.say(text)
  eel.receiverText(text)
  engine.runAndWait() 


def takecommand():

    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('Listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source,10,30)

    try:
        print('recognizing')
        eel.DisplayMessage('Recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        print("Say that again please...")
        return "None"
    
    return query.lower()

@eel.expose 
def allCommands(message=1):

  if message == 1:
    query = takecommand()
    print(query)
    eel.senderText(query)
  else:
    query = message
    eel.senderText(query)
      
  try:
    if "open" in query:
          from engine.features import openCommand
          openCommand(query)

    
    elif "type" in query:
          query = query.replace("type", "")
          pyautogui.typewrite(f"query",0.1)
          
    elif "on youtube" in query:
          from engine.features import PlayYoutube
          PlayYoutube(query)
          #wk.playonyt(f"{query}")
    
    elif "close browser" in query or "exit browser" in query:
          speak("Closing Browser")
          os.system("taskkill /IM chrome.exe /F")

    elif "search" in query and "on" in query:
            print(f"Searching Website for: {query}")
            from engine.features import SearchWebsite
            SearchWebsite(query)

    elif "who are you" in query:
          print("My name is ALEXA")     
          speak("My name is ALEXA")
    
    elif "what is" in query:
          speak("Searching Net...")
          query = query.replace("what is","")
          results = wikipedia.summary(query, sentences=2)
          speak("According to the Internet")
          print(results)
          speak(results)

    elif "who is" in query:
          speak("Searching Net...")
          query = query.replace("who is","")
          results = wikipedia.summary(query, sentences=2)
          speak("According to the Internet")
          print(results)
          speak(results)


    elif "just open google" in query:
          webbrowser.open("https://www.google.com")
    
    elif "go to google" in query:
          speak("What should I search?")
          qry = takecommand().lower()
    
          #if qry== "facebook" or "instagram" or "flipkart" or "spotify" or "Twitter" or "WhatsApp" or "Snapchat" or "Telegram" or "Messenger" or "LinkedIn" or "Netflix" :
          if qry!=None:
            print(f"Searching for {qry} on Google...")
            general_url = f"https://www.{qry}.com/login"
            webbrowser.open(general_url)   # Corrected search URL
        
            # try:
            #   result = wikipedia.summary(qry, sentences=1)
            #   speak(result)  # Speak Wikipedia summary
            # except wikipedia.exceptions.DisambiguationError as e:
            #   speak("There are multiple results. Please be more specific.")
            # except wikipedia.exceptions.PageError:
            #   speak("No relevant Wikipedia page found.")

   

          
    
    
    # elif "go to facebook" in query:
    #       speak("Opening Facebook , if you are not login please login with user username and password")
    #       webbrowser.open("https://www.facebook.com/login")
    
    # elif "go to instagram" in query:
    #       speak("Opening Instagram ")
    #       webbrowser.open("https://www.instagram.com/accounts/login/")

    elif "go to gpt" in query:
          
          speak("What should I search on ChatGPT?")
          qry = takecommand().lower()

          if qry != "none":
            speak(f"Searching for {qry} on ChatGPT")
            webbrowser.open(f"https://chat.openai.com/?q={qry}")  # Open ChatGPT with query




    elif "send a message" in query or "phone call" in query or "video call" in query:
          from engine.features import findContact, whatsApp, makeCall, sendMessage
          contact_no, name = findContact(query)
          if(contact_no != 0):
              speak("Which mode you want to use whatsapp or mobile")
              preferance = takecommand()
              print(preferance)

              if "mobile" in preferance:
                  if "send a message" in query or "send sms" in query: 
                      speak("what message to send")
                      message = takecommand()
                      sendMessage(message, contact_no, name)
                  elif "phone call" in query:
                      makeCall(name, contact_no)
                  else:
                      speak("please try again")
              elif "whatsapp" in preferance:
                  message = ""
                  if "send message" in query:
                      message = 'message'
                      speak("what message to send")
                      query = takecommand()
                                        
                  elif "phone call" in query:
                    message = 'call'
                  else:
                    message = 'video call'
                                        
                  whatsApp(contact_no, query, message, name)


    else:
          from engine.features import chatBot
          chatBot(query)
  except Exception as e:
    print(f"An error occurred: {e}")

  eel.ShowHood()
  
