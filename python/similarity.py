# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 15:36:07 2020

@author: Vaishali
"""
import spacy
import pandas as pd 
data = pd.read_csv(r'C:\Users\Vaishali\Desktop\New folder\qa_data.csv',encoding= 'unicode_escape') 
data.head()
len(data)

import numpy as np 
topic=np.unique(data['Concept'] ) 

  

finaldata = data[["Concept", "Answer"]]          # Required columns - Title and movie plot 
#finaldata = finaldata.set_index('Concept')
  
finaldata.head(10) 


import nltk 
  
from nltk.stem import WordNetLemmatizer 
lemmatizer = WordNetLemmatizer() 
  
from nltk.corpus import stopwords 
stop_words = set(stopwords.words('english')) 
  
VERB_CODES = {'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}

def preprocess_sentences(text): 
  text = text.lower() 
  temp_sent =[] 
  words = nltk.word_tokenize(text) 
  tags = nltk.pos_tag(words) 
  for i, word in enumerate(words): 
      if tags[i][1] in VERB_CODES:  
          lemmatized = lemmatizer.lemmatize(word, 'v') 
      else: 
          lemmatized = lemmatizer.lemmatize(word) 
      if lemmatized not in stop_words and lemmatized.isalpha(): 
          temp_sent.append(lemmatized) 
          
  finalsent = ' '.join(temp_sent) 
  finalsent = finalsent.replace("n't", " not") 
  finalsent = finalsent.replace("'m", " am") 
  finalsent = finalsent.replace("'s", " is") 
  finalsent = finalsent.replace("'re", " are") 
  finalsent = finalsent.replace("'ll", " will") 
  finalsent = finalsent.replace("'ve", " have") 
  finalsent = finalsent.replace("'d", " would") 
  return finalsent 

import speech_recognition as sr 
 
mic_name = "USB Device 0x46d:0x825: Audio (hw:1, 0)"
#Sample rate is how often values are recorded 
sample_rate = 48000
chunk_size = 2048
#Initialize the recognizer 
r = sr.Recognizer() 
  
#generate a list of all audio cards/microphones 


finaldata["Answer_processed"]= finaldata["Answer"].apply(preprocess_sentences) 
finaldata.head()

from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 

# tokenization
Y_list = word_tokenize(Y) 
sw = stopwords.words('english')  
l1 =[]
l2 =[]

X=finaldata.loc[finaldata['Concept'] == question[0]]
X_list=[]
for i in X["Answer_processed"]:
    X_list.append(word_tokenize(i))    

nlp = spacy.load('en')

def check(Y):
    flag=0
    for i in X["Answer"]:
        main_doc = nlp(i)
        similar=main_doc.similarity(nlp(Y))
        if similar > 0.65:
            print("Valid answer")
            flag=1
            break 
    if flag == 0:
         print("Invalid answer")          
    
def chat():
    question=random.choices(topic)
    print("Tell me about %s" %question)
    mic_list = sr.Microphone.list_microphone_names() 
  
    for i, microphone_name in enumerate(mic_list): 
        if microphone_name == mic_name: 
            device_id = i 
    with sr.Microphone(device_index = 1, sample_rate = sample_rate,chunk_size = chunk_size) as source:  
        r.adjust_for_ambient_noise(source) 
        print("Say Something")
        #listens for the user's input 
        audio = r.listen(source) 
        text=""
          
        try: 
            text = r.recognize_google(audio) 
            print("you said: %s" %text) 
 
        except sr.UnknownValueError: 
            print("Google Speech Recognition could not understand audio") 
      
        except sr.RequestError as e: 
            print("Could not request results from Google")
    check(text)
        
for _ in range(4):
    main_doc=nlp("hello")
    Y="hai"
    main_doc.similarity(nlp(Y))
    chat()