import os
from sklearn.feature_extraction.text import CountVectorizer
import nltk
import pandas as pd
from openpyxl import Workbook

# Taking input
sentences = input("Enter your sentences: ")
sentences = sentences.lower()

# Tokenization
tokenized_sentences = nltk.tokenize.sent_tokenize(sentences)
tokenized_sentences1 = [x.replace(".", "") for x in tokenized_sentences]

# CountVectorizer
countVectorizer = CountVectorizer()
tmpbow = countVectorizer.fit_transform(tokenized_sentences1)
bow = tmpbow.toarray()

# Vocabulary and Features
print("Vocabulary = ", countVectorizer.vocabulary_)
print("Features = ", countVectorizer.get_feature_names())
print("BOW ", bow)

# DataFrame
cv_dataframe = pd.DataFrame(bow, columns=countVectorizer.get_feature_names())
print("cv_dataframe is below\n", cv_dataframe)

# Saving to Excel
cv_dataframe.to_excel('./Bag of words model/bowp.xlsx', sheet_name='data')
