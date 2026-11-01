
# Day 3 - Understanding TF-IDF
# CodeAlpha AI Internship

from sklearn.feature_extraction.text import TfidfVectorizer

# Sample documents
documents = [
    "college admission requirements",
    "college admission process",
    "college examination schedule",
    "college placement information"
]

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Convert text into numerical vectors
tfidf_matrix = vectorizer.fit_transform(documents)

# Display vocabulary
print("Vocabulary:")
print(vectorizer.get_feature_names_out())

# Display numerical representation
print("\nTF-IDF Matrix:")
print(tfidf_matrix.toarray())

print("\nShape of TF-IDF Matrix:")
print(tfidf_matrix.shape)
