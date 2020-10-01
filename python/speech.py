# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:41:00 2020

@author: Vaishali
"""
import speech_recognition as sr 
 
mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
#Sample rate is how often values are recorded 
sample_rate = 48000
chunk_size = 2048
#Initialize the recognizer 
r = sr.Recognizer() 
  
#generate a list of all audio cards/microphones 
mic_list = sr.Microphone.list_microphone_names() 
  
for i, microphone_name in enumerate(mic_list): 
    if microphone_name == mic_name: 
        device_id = i 
   
with sr.Microphone(device_index = 1, sample_rate = sample_rate,  
                        chunk_size = chunk_size) as source: 
    #wait for a second to let the recognizer adjust the  
    #energy threshold based on the surrounding noise level 
    r.adjust_for_ambient_noise(source) 
    print("Say Something")
    #listens for the user's input 
    audio = r.listen(source) 
          
    try: 
        text = r.recognize_google(audio) 
        print("you said: %s" %text) 
      
    #error occurs when google could not understand what was said 
      
    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio") 
      
    except sr.RequestError as e: 
        print("Could not request results from Google")