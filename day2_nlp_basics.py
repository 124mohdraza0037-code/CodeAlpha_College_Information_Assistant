
# Day 2 - NLP Basics
# CodeAlpha AI Internship

import nltk
from nltk.tokenize import wordpunct_tokenize

# Original sentence
sentence = "What are the ADMISSION requirements for this College?"

print("Original Sentence:")
print(sentence)

# Step 1: Convert text to lowercase
text = sentence.lower()

print("\nAfter Lowercase Conversion:")
print(text)

# Step 2: Tokenization
tokens = wordpunct_tokenize(text)

print("\nAfter Tokenization:")
print(tokens)

# Step 3: Remove punctuation
words = [word for word in tokens if word.isalpha()]

print("\nAfter Removing Punctuation:")
print(words)

# Step 4: Remove stopwords
stop_words = {
    "what", "are", "the", "is", "a",
    "an", "for", "this", "in", "of"
}

filtered_words = [
    word for word in words
    if word not in stop_words
]

print("\nAfter Stopword Removal:")
print(filtered_words)

# Step 5: Join processed words
processed_text = " ".join(filtered_words)

print("\nFinal Processed Text:")
print(processed_text)
