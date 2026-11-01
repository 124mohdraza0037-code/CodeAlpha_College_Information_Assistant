
# CodeAlpha - FAQ Question Matching Engine

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# FAQ database
faq_questions = [
    "What are the college timings?",
    "What courses are available?",
    "How can I apply for admission?",
    "Where is the college located?"
]

faq_answers = [
    "The college timings are 9 AM to 5 PM.",
    "The college offers various undergraduate engineering courses.",
    "You can apply through the official admission process.",
    "Please visit the college website for its address."
]

# Create TF-IDF vectors for FAQs
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)

# Take user input
user_question = input("Ask your question: ")

# Convert user question into a vector
user_vector = vectorizer.transform([user_question])

# Calculate similarity with all FAQs
scores = cosine_similarity(user_vector, faq_vectors)

# Find the best matching question
best_match_index = scores.argmax()
best_score = scores[0][best_match_index]

print("\nSimilarity Score:", round(best_score, 3))

# Set a basic matching threshold
# Minimum similarity threshold
THRESHOLD = 0.60

if best_score >= THRESHOLD:
    print("Chatbot:", faq_answers[best_match_index])
else:
    print("Chatbot: Sorry, I could not find a suitable answer.")
