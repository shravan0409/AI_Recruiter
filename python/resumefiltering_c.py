# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 12:30:07 2020

@author: Vaishali
"""

from PIL import Image 
import pytesseract 
from rake_nltk import Rake
import sys 
from pdf2image import convert_from_path 
import os 
from nltk.corpus import stopwords
import math

def read_resume():
    PDF_file=r"C:\Users\Vaishali\Desktop\Placements\res_test_c1.pdf"
    pages = convert_from_path(PDF_file, 500) 
    
     
    image_counter = 1
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Vaishali\AppData\Local\Tesseract-OCR\tesseract.exe'
      
    # Iterate through all the pages stored above 
    for page in pages: 
        filename = "page_"+str(image_counter)+".jpg" 
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
      
    ''' 
    Part #2 - Recognizing text from the images using OCR 
    '''
    filelimit = image_counter-1
      
    # Creating a text file to write the output 
    outfile = "out_text1.txt"
      
    # Open the file in append mode so that  
    # All contents of all images are added to the same file 
    f = open(outfile, "a") 
      
    # Iterate from 1 to total number of pages 
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
              
        # Recognize the text as string in image using pytesserct 
        text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = text.replace('-\n', '')     
      
        # Finally, write the processed text to the file. 
        f.write(text)  
    f.close()
    main_words=['python','database','django','web','framework','c++']
    key_words=preprocess(text)
    idf=find_freq(main_words,key_words)
    #return idf

def find_freq(key_words,text):
    dic={}
    for i in text:
        if i in key_words:
            if i in dic.keys():
                dic[i]+=1
            else:
                dic[i]=1
    tf_idf(dic,len(text))
    


def tf_idf(freq_matrix,total_documents):
 
    idf = 0
    for i in freq_matrix.keys():
        idf += (total_documents / float(freq_matrix[i]))
    if idf > 0:
        idf= math.log10(idf)
    if idf > 2.5:
        print("Resume Short listed")
    else:
        print("Resume Not Short listed")
    return idf


def text_lowercase(text): 
    return text.lower() 

def preprocess(text):
    words=stopwords.words('english')
    words.append(' ')
    key_words=[]
    text=text_lowercase(text)
    text_split=text.split(' ')
    key_words=[txt for txt in text_split if txt not in words]
    return key_words
    
read_resume()
