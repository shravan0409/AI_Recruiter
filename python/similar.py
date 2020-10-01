 # -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 14:55:30 2020

@author: Vaishali
"""
import random
import pandas as pd 
data = pd.read_csv(r'C:\Users\Vaishali\Desktop\New folder\qa_data.csv',encoding= 'unicode_escape') 
data.head()
len(data)

  
import numpy as np 
topic=np.unique(data['Concept'] ) 
question=random.choices(topic)


print("Tell me about %s" %question)
  
finaldata = data[["Concept", "Answer"]]          # Required columns - Title and movie plot 
finaldata = finaldata.set_index('Concept')
  
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
  
finaldata["Answer_processed"]= finaldata["Answer"].apply(preprocess_sentences) 
finaldata.head()


from sklearn.feature_extraction.text import TfidfVectorizer 
  
# Vectorizing pre-processed movie plots using TF-IDF 
tfidfvec = TfidfVectorizer() 
tfidf_id = tfidfvec.fit_transform((finaldata["Answer_processed"])) 
  
# Finding cosine similarity between vectors 
from sklearn.metrics.pairwise import cosine_similarity 
cos_sim = cosine_similarity(tfidf_id, tfidf_id) 


indices = pd.Series(finaldata.index) 
  
def recommendations(title, cosine_sim = cos_sim): 
    recommended_movies = [] 
    index = indices[indices == title].index[0] 
    similarity_scores = pd.Series(cosine_sim[index]).sort_values(ascending = False) 
    top_10_movies = list(similarity_scores.iloc[1:11].index) 
    for i in top_10_movies: 
        recommended_movies.append(list(finaldata.index)[i]) 
    return recommended_movies


recommendations("Arrays")