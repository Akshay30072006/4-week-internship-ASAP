# -----------------------------
# Imports
# -----------------------------
from groq import Groq
import re
import streamlit as st

# -----------------------------
# Backend: LLM Client
# -----------------------------
class LLMClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=800
        )
        return response.choices[0].message.content


# -----------------------------
# Prompt & Formatting Functions
# -----------------------------
def explanation_prompt(topic, level):
    return f"Explain {topic} in {level} terms for a student."

def summarization_prompt(text):
    return f"Summarize the following text in bullet points:\n{text}"

def quiz_prompt(text):
    return f"Create 5 quiz questions with answers from the text:\n{text}"

def flashcard_prompt(text):
    return f"Create flashcards (Question and Answer) from the text:\n{text}"

def format_explanation(text):
    return re.sub(r"\. ", ".\n", text.strip())

def format_summary(text):
    lines = text.split("\n")
    return "\n".join("- " + line.strip() for line in lines if line.strip())

def format_quiz(text):
    return re.sub(r"(\d+\.)", r"\n\1", text.strip())

def format_flashcards(text):
    text = re.sub(r"Question:", "\n📌 Question:", text)
    text = re.sub(r"Answer:", "👉 Answer:", text)
    return text.strip()


# -----------------------------
# Study Buddy Backend
# -----------------------------
class StudyBuddyBackend:
    def __init__(self, api_key: str):
        self.llm = LLMClient(api_key)

    def explain_topic(self, topic: str, level: str) -> str:
        raw = self.llm.generate_response(explanation_prompt(topic, level))
        return format_explanation(raw)

    def summarize_text(self, text: str) -> str:
        raw = self.llm.generate_response(summarization_prompt(text))
        return format_summary(raw)

    def generate_quiz(self, text: str) -> str:
        raw = self.llm.generate_response(quiz_prompt(text))
        return format_quiz(raw)

    def generate_flashcards(self, text: str) -> str:
        raw = self.llm.generate_response(flashcard_prompt(text))
        return format_flashcards(raw)


# -----------------------------
# Initialize Backend
# -----------------------------
API_KEY = "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"   # Replace with your Groq API key
backend = StudyBuddyBackend(API_KEY)


# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="📚 AI Study Buddy", layout="wide")
st.markdown("## 📚 AI-Powered Study Buddy")
st.markdown("### 🎓 Learn, Summarize, Quiz & Flashcards")

menu = ["Explain Topic", "Summarize Text", "Generate Quiz", "Generate Flashcards"]
choice = st.sidebar.selectbox("Select Functionality", menu)


# -----------------------------
# Explain Topic
# -----------------------------
if choice == "Explain Topic":
    st.subheader("📝 Explain a Topic")
    col1, col2 = st.columns([1, 2])

    with col1:
        topic = st.text_input("Enter Topic:")
        level = st.selectbox("Select Level", ["simple", "medium", "advanced"])
        if st.button("Explain"):
            if topic:
                with st.spinner("Generating explanation..."):
                    output = backend.explain_topic(topic, level)
            else:
                st.warning("Please enter a topic!")

    with col2:
        if 'output' in locals():
            st.text_area("💡 Explanation", output, height=300)


# -----------------------------
# Summarize Text
# -----------------------------
elif choice == "Summarize Text":
    st.subheader("🗒️ Summarize Text")
    col1, col2 = st.columns([1, 2])

    with col1:
        text = st.text_area("Paste text here:", height=200)
        if st.button("Summarize"):
            if text:
                with st.spinner("Generating summary..."):
                    output = backend.summarize_text(text)
            else:
                st.warning("Please paste some text!")

    with col2:
        if 'output' in locals():
            st.text_area("📝 Summary", output, height=300)


# -----------------------------
# Generate Quiz
# -----------------------------
elif choice == "Generate Quiz":
    st.subheader("❓ Generate Quiz")
    col1, col2 = st.columns([1, 2])

    with col1:
        text = st.text_area("Paste text here:", height=200)
        if st.button("Generate Quiz"):
            if text:
                with st.spinner("Generating quiz..."):
                    output = backend.generate_quiz(text)
            else:
                st.warning("Please paste some text!")

    with col2:
        if 'output' in locals():
            st.text_area("📝 Quiz", output, height=300)


# -----------------------------
# Generate Flashcards
# -----------------------------
elif choice == "Generate Flashcards":
    st.subheader("📇 Generate Flashcards")
    col1, col2 = st.columns([1, 2])

    with col1:
        text = st.text_area("Paste text here:", height=200)
        if st.button("Generate Flashcards"):
            if text:
                with st.spinner("Generating flashcards..."):
                    output = backend.generate_flashcards(text)
            else:
                st.warning("Please paste some text!")

    with col2:
        if 'output' in locals():
            st.text_area("📝 Flashcards", output, height=300)


# -----------------------------
# Footer
# -----------------------------
st.markdown("---")
st.markdown("💡 Developed as an AI Study Buddy Demo")
