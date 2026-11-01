
# CodeAlpha - College Information Assistant
# CSV-Based College FAQ Chatbot

from pathlib import Path

import pandas as pd
import streamlit as st

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------------------------
# 1. Configure the webpage
# --------------------------------------------------

st.set_page_config(
    page_title="College Information Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 College Information Assistant")

st.write(
    "Welcome! Ask me questions about a college's courses, "
    "admissions, facilities and contact information."
)

st.divider()


# --------------------------------------------------
# 2. Load FAQ data from CSV
# --------------------------------------------------

DATA_FILE = Path(__file__).parent / "faq_data.csv"

REQUIRED_COLUMNS = [
    "college_id",
    "college_name",
    "question",
    "answer",
    "source_url",
    "verified_on"
]

try:
    faq_data = pd.read_csv(DATA_FILE)

    # Check whether all required columns exist
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in faq_data.columns
    ]

    if missing_columns:
        st.error(
            "Missing CSV columns: "
            + ", ".join(missing_columns)
        )
        st.stop()

    # Remove incomplete FAQ records
    faq_data = faq_data.dropna(
        subset=["college_id", "college_name", "question", "answer"]
    )

    # Remove empty text values
    for column in ["college_id", "college_name", "question", "answer"]:
        faq_data[column] = faq_data[column].astype(str).str.strip()

    faq_data = faq_data[
        (faq_data["college_name"] != "") &
        (faq_data["question"] != "") &
        (faq_data["answer"] != "")
    ].reset_index(drop=True)

    if faq_data.empty:
        st.error("The FAQ database is empty.")
        st.stop()

except FileNotFoundError:
    st.error(
        "faq_data.csv was not found. "
        "Keep it in the same folder as app.py."
    )
    st.stop()

except Exception as error:
    st.error(f"Could not load FAQ database: {error}")
    st.stop()


# --------------------------------------------------
# 3. College selection
# --------------------------------------------------

college_options = sorted(
    faq_data["college_name"].unique()
)

selected_college = st.selectbox(
    "Select your college:",
    college_options
)

# Filter FAQs for the selected college
college_faqs = faq_data[
    faq_data["college_name"] == selected_college
].reset_index(drop=True)

faq_questions = college_faqs["question"].tolist()


# --------------------------------------------------
# 4. Create the NLP model
# --------------------------------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 2)
)

faq_vectors = vectorizer.fit_transform(faq_questions)

# Separate analyzer for meaningful single words
word_analyzer = TfidfVectorizer(
    stop_words="english",
    ngram_range=(1, 1)
).build_analyzer()


# Matching settings
THRESHOLD = 0.30
MIN_QUERY_TERMS = 2
MIN_QUERY_COVERAGE = 0.60


# --------------------------------------------------
# 5. Initialize chat history
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "active_college" not in st.session_state:
    st.session_state.active_college = selected_college

# Clear previous conversation when college changes
if st.session_state.active_college != selected_college:
    st.session_state.messages = []
    st.session_state.active_college = selected_college


# --------------------------------------------------
# 6. Sidebar information
# --------------------------------------------------

with st.sidebar:

    st.header("About the Chatbot")

    st.write(
        "This chatbot uses Natural Language Processing "
        "to match your questions with stored college FAQs."
    )

    

    st.write("**Selected college:**")
    st.write(selected_college)

    st.write("**Available FAQs:**")
    st.write(len(college_faqs))

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# 7. Display previous messages
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# --------------------------------------------------
# 8. Accept user question
# --------------------------------------------------

user_question = st.chat_input(
    "Ask your college-related question..."
)


# --------------------------------------------------
# 9. Process user question
# --------------------------------------------------

if user_question:

    # Save user question
    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })


    # Normalize the user's question
    normalized_question = user_question.strip().casefold()

    # Check for an exact FAQ match first
    exact_matches = [
        i for i, question in enumerate(faq_questions)
        if question.strip().casefold() == normalized_question
    ]

    if exact_matches:
        best_match_index = exact_matches[0]
        best_score = 1.0
        query_coverage = 1.0

    else:
        # Convert user question into TF-IDF vector
        user_vector = vectorizer.transform([user_question])

        user_terms = set(word_analyzer(user_question))

        best_score = 0
        best_match_index = 0
        query_coverage = 0

        if user_vector.nnz > 0 and user_terms:

            # Calculate cosine similarity
            similarity_scores = cosine_similarity(
                user_vector,
                faq_vectors
            )[0]

            best_match_index = similarity_scores.argmax()
            best_score = similarity_scores[best_match_index]

            # Calculate meaningful word coverage
            faq_terms = set(
                word_analyzer(faq_questions[best_match_index])
            )

            common_terms = user_terms.intersection(faq_terms)

            query_coverage = (
                len(common_terms) / len(user_terms)
            )

    matched_question = faq_questions[best_match_index]

    # Debug information
    print("User Question:", user_question)
    print("Matched FAQ:", matched_question)
    print("Similarity Score:", round(best_score, 3))
    print("Question Coverage:", round(query_coverage, 3))


    # Debug information in VS Code terminal
    print("\nUser Question:", user_question)
    print("Matched FAQ:", matched_question)
    print("Similarity Score:", round(best_score, 3))
    print("Question Coverage:", round(query_coverage, 3))

    # --------------------------------------------------
    # 10. Generate chatbot response
    # --------------------------------------------------

    if (
    exact_matches
    or (
        len(user_terms) >= MIN_QUERY_TERMS
        and best_score >= THRESHOLD
        and query_coverage >= MIN_QUERY_COVERAGE
    )
):

        matched_row = college_faqs.iloc[best_match_index]

        bot_response = str(matched_row["answer"])

        # Add official source link
        source_url = matched_row["source_url"]

        if pd.notna(source_url) and str(source_url).strip():

            bot_response += (
                "\n\n**Official source:** "
                f"[Visit source]({str(source_url).strip()})"
            )

        # Add verification date
        verified_date = matched_row["verified_on"]

        if pd.notna(verified_date) and str(verified_date).strip():

            bot_response += (
                f"\n\n*Information checked: {verified_date}*"
            )

        # Display matching information
        bot_response += (
            f"\n\n*Matched FAQ: {matched_question}*"
            f"\n*Similarity Score: {best_score:.3f}*"
        )

    else:

        bot_response = (
            "Sorry, I could not find a sufficiently relevant "
            "answer in the selected college's FAQ database. "
            "Please try rephrasing your question or visit "
            "the college's official website."
        )

    # --------------------------------------------------
    # 11. Save chatbot response
    # --------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_response
    })

    # Refresh the application
    st.rerun()
