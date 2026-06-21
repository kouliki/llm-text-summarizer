from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st

# Load API key
load_dotenv()
client = Groq(api_key=os.getenv("API key"))

# Function to summarize text
def summarize_text(text, mode):
    if mode == "Short":
        prompt = "Summarize this in 2 lines"
    elif mode == "Bullet":
        prompt = "Summarize this in bullet points"
    else:
        prompt = "Explain this in simple and easy words"

    # Split text into chunks
    chunk_size = 1000
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    summaries = []

    for chunk in chunks:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": f"{prompt}:\n{chunk}"}
            ],
            temperature=0.3
        )
        summaries.append(response.choices[0].message.content)

    # Combine summaries
    final_text = " ".join(summaries)

    # Final summarization
    final_response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": f"Summarize this overall:\n{final_text}"}
        ],
        temperature=0.3
    )

    return final_response.choices[0].message.content

# Streamlit UI
st.title("🧠 Text Summarizer (Groq)")

st.write("Paste your text below and choose how you want it summarized.")

text = st.text_area("Enter your text here:", height=200)

mode = st.selectbox("Select summary type:", ["Short", "Bullet", "Simple"])

if st.button("Summarize"):
    if text.strip() == "":
        st.warning("Please enter some text!")
    else:
        with st.spinner("Generating summary..."):
            result = summarize_text(text, mode)
        st.subheader("Summary:")
        st.write(result)