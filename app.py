
import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Corporate Sarcasm Translator", layout="left")
st.markdown(
    "<h1 style='color: purple;'>Corporate Cop!</h1>", unsafe_allow_html=True
)
st.write("Paste that shady work email or text below. We'll decode the hidden rage and translate it into brutal honesty.")

# Sidebar for API Key input
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    st.markdown("[Get a free key here](https://aistudio.google.com/)")
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. Paste a polite corporate email.\n2. AI detects hidden tone.\n3. Get the unfiltered translation.")

# Main input area
email_text = st.text_area( 
"", height=150
)

if st.button("Decode Message 🔍", type="primary"):
    if not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar first!")
    elif not email_text.strip():
        st.warning("Please enter some text to analyze.")
    else:
        genai.configure(api_key=api_key)

        prompt = f"""
        You are a cynical, hyper-observant corporate body-language and tone expert. 
        Analyze the following workplace message and break it down into 3 sections:
        1. **The Brutally Honest Translation:** Rewrite the message into what they wish they could type if HR didn't exist.
        2. **The Vibe Check:** Rate the Passive-Aggressive / Sarcasm level from 1 to 10 and name the emotion (e.g., "Seething Rage wrapped in polite punctuation").
        3. **Between the Lines:** What are they *actually* trying to say? Unpack the hidden subtext.

        Message to analyze:
        "{email_text}"
        """

        with st.spinner("Analyzing passive-aggressive undertones..."):
            try:
                model = genai.GenerativeModel('gemini-3.8-flash')
                response = model.generate_content(prompt)

                st.markdown("### Analysis Results")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
