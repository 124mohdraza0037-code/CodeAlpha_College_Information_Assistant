
# Day 3 - Cosine Similarity
# CodeAlpha AI Internship

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Two questions
questions = [
    "What are the college timings?",
    "When does the college open?"
]

# Convert questions into TF-IDF vectors
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(questions)

# Calculate cosine similarity
similarity = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
)

# Display result
print("Question 1:", questions[0])
print("Question 2:", questions[1])

print("\nCosine Similarity Score:")
print(similarity[0][0])
