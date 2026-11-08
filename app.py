import streamlit as st
import google.generativeai as genai
from PIL import Image

# Page Configuration
st.set_page_config(page_title="Sarcasm & Rage Translator", page_icon="🕵️‍♂️", layout="centered")

st.title("🕵️‍♂️ Sarcasm, Toxicity & Rage Translator")
st.write("Decode shady emails, WhatsApp chats, toxic gaming lobbies, ragebait posts, or social media arguments (English or Bangla).")

# Sidebar for API Key input and Context selection
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google Gemini API Key:", type="password")
    st.markdown("[Get a free key here](https://aistudio.google.com/)")
    st.markdown("---")
    
    st.header("Context Setting")
    context_mode = st.selectbox(
        "Where is this message/post from?",
        [
            "🎮 Gamer Rage / In-Game Chat / Discord",
            "🎣 Ragebait / Engagement Bait Post",
            "🏢 Workplace / Corporate Email",
            "💬 Casual Chat / WhatsApp / Messenger",
            "📱 Social Media Comment (Facebook/Instagram/X)",
            "🌐 Forum / Reddit Thread Comment"
        ]
    )
    
    st.markdown("---")
    st.markdown("### Features:")
    st.markdown("- Supports text & screenshots")
    st.markdown("- Detects gaming slang & ragebaiting")
    st.markdown("- Multilingual (English & Bangla)")

# Input options
message_text = st.text_area(
    "1. Paste the message, comment, or post text here (optional if uploading image):", 
    height=120, 
    placeholder="e.g., 'GG EZ uninstall trash team' or 'unpopular opinion: [obviously offensive take]'"
)

uploaded_file = st.file_uploader("2. Or upload a screenshot of the chat/comment/post:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Screenshot", use_container_width=True)

if st.button("Decode Message 🔍", type="primary"):
    if not api_key:
        st.error("Please enter your Google Gemini API Key in the sidebar first!")
    elif not message_text.strip() and not uploaded_file:
        st.warning("Please either type a message or upload a screenshot!")
    else:
        genai.configure(api_key=api_key)
        
        prompt = f"""
        You are a hyper-observant digital body-language and social dynamics expert specializing in modern internet culture, gaming toxicity/slang, ragebaiting tactics, passive-aggressiveness, and subtext. 
        The specific context of this input is: "{context_mode}".
        
        Analyze the provided message or image content (which could be in English or Bangla) and break it down into 3 clear sections:
        1. **The Vibe Check:** Rate the Toxicity / Sarcasm / Rage level from 1 to 10 and describe the exact emotional state (e.g., "Full Gamer Tilt", "Calculated Ragebait for Clicks", "Passive-Aggressive Seething").
        2. **Between the Lines & Tactics:** Unpack the subtext. If it's gaming rage, explain the tilt/blame shifting. If it's ragebait, reveal how it manipulates people into arguing for clicks/engagement. Highlight emojis, slang, or double meanings.
        3. **The Unfiltered Translation:** Rewrite the message into what they are *really* feeling or trying to accomplish in brutally honest terms (match the primary language of the input).
        """
        
        with st.spinner("Decoding rage, tilt, and internet tactics..."):
            try:
                # Use standard model initialization
                model = genai.GenerativeModel('gemini-3.8-flash')
                
                content_inputs = [prompt]
                if message_text.strip():
                    content_inputs.append(f"Content to analyze: {message_text}")
                if uploaded_file is not None:
                    content_inputs.append(image)
                
                response = model.generate_content(content_inputs)
                
                st.markdown("### 📊 Analysis Results")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
