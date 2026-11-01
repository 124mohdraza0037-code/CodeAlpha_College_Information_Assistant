# College Information Assistant 🎓

A Python-based college FAQ chatbot developed as part of the **CodeAlpha Artificial Intelligence Internship**.

The application allows students to ask questions about college information and receive relevant answers from a structured FAQ database.

## Project Overview

The College Information Assistant uses Natural Language Processing (NLP) techniques to identify the most relevant FAQ for a user's question.

Instead of generating answers independently, the chatbot retrieves information from a CSV-based knowledge database. This helps reduce unsupported responses.

The initial dataset contains information for Don Bosco Institute of Technology (DBIT), Mumbai.

## Features

- Interactive chatbot interface using Streamlit.
- CSV-based FAQ database.
- College selection functionality.
- TF-IDF text vectorization.
- Cosine similarity-based question matching.
- Exact question matching.
- Question coverage validation.
- Rejection of unsupported questions.
- Official source links alongside answers.
- Chat history and Clear Chat functionality.
- Support for adding more colleges through the CSV database.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web application interface |
| Pandas | CSV data handling |
| Scikit-learn | NLP and similarity matching |
| TF-IDF | Text vectorization |
| Cosine Similarity | FAQ matching |

## Project Structure

```text
CodeAlpha_FAQChatbot/
│
├── app.py
├── faq_data.csv
├── requirements.txt
├── README.md
│
├── day2_nlp_basics.py
├── day3_tfidf_similarity.py
├── day3_cosine_similarity.py
├── day3_faq_matching.py
├── test.py
│
└── venv/
```

## How It Works

1. The application loads college questions and answers from `faq_data.csv`.
2. The user selects a college.
3. The user enters a question through the Streamlit chat interface.
4. The system first checks for an exact FAQ question match.
5. If no exact match is found, TF-IDF converts the question into numerical vectors.
6. Cosine similarity compares the question against stored FAQs.
7. A question-coverage check helps validate the matching result.
8. If the match satisfies the configured conditions, the chatbot displays the corresponding answer and source link.
9. If no suitable match is found, the chatbot displays a fallback response.

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project directory

```bash
cd CodeAlpha_FAQChatbot
```

### 3. Create a virtual environment

```bash
py -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
python -m streamlit run app.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

## FAQ Database Format

The chatbot uses `faq_data.csv` as its knowledge database.

The CSV file contains these columns:

| Column | Description |
|---|---|
| college_id | Unique college identifier |
| college_name | College name |
| question | Stored FAQ question |
| answer | Corresponding answer |
| source_url | Information source |
| verified_on | Date recorded as checked |

New colleges can be added by inserting additional FAQ records with their respective college identifiers and names.

## Testing

The application should be tested with:

- Exact FAQ questions.
- Different question phrasings.
- Questions about college facilities and admissions.
- Questions not available in the database.
- Unrelated questions.
- College selection and chat clearing.
- Source-link functionality.

Actual test results should be recorded before submission.

## Limitations

- The chatbot retrieves answers only from its available FAQ database.
- It does not independently generate new information.
- Matching quality depends on the stored FAQ questions and configured thresholds.
- Some valid paraphrased questions may not match.
- College information must be updated when official details change.

## Future Improvements

- Add more colleges and universities.
- Expand the FAQ database.
- Improve semantic question matching.
- Add multilingual question support.
- Integrate an administrative interface for updating FAQs.
- Deploy the chatbot online.
- Add more advanced NLP techniques.

## Internship

**Project:** College Information Assistant  
**Internship:** CodeAlpha Artificial Intelligence Internship  
**Language:** Python

---

*Developed as an educational project to explore Natural Language Processing, information retrieval and chatbot development.*