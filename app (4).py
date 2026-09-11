import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly.")

# API Key Handling (Reads from Streamlit Secrets or manual input)
groq_api_key = st.secrets.get("GROQ_API_KEY") if "GROQ_API_KEY" in st.secrets else None

if not groq_api_key:
    groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")
    st.sidebar.markdown("[Get a free Groq API Key](https://console.groq.com/keys)")

# User Input Controls
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox("Content Type", ["Social Media Post", "Article/Blog Teaser", "Product Announcement", "Newsletter Snippet"])
    platform = st.selectbox("Target Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook", "Threads"])
    tone = st.selectbox("Tone of Voice", ["Professional", "Casual & Friendly", "Persuasive & Sales-oriented", "Witty & Funny", "Educational"])

with col2:
    target_audience = st.text_input("Target Audience", placeholder="e.g., Tech Founders, Fitness Enthusiasts")
    topic = st.text_area("Topic / Main Idea", placeholder="e.g., The benefits of morning routines for productivity", height=110)

# Generate Button
if st.button("Generate Content", type="primary", use_container_width=True):
    if not groq_api_key:
        st.error("Please provide a Groq API Key to proceed.")
    elif not topic.strip():
        st.warning("Please enter a topic or main idea.")
    else:
        try:
            # Initialize Groq Client
            client = Groq(api_key=groq_api_key)
            
            # Formulate the Prompt
            prompt = f"""
            You are an expert social media strategist and content creator.
            Create a high-engaging {content_type} optimized for {platform}.
            
            Details:
            - Topic: {topic}
            - Target Audience: {target_audience if target_audience else 'General Audience'}
            - Tone: {tone}
            
            Requirements:
            1. Write a compelling, platform-ready main post/caption using formatting (emojis, line breaks) appropriate for {platform}.
            2. Provide 5-8 relevant, high-traffic hashtags at the very bottom.
            """
            
            with st.spinner("Drafting your post..."):
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": "You are a professional content creator."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000,
                )
                
                output = response.choices[0].message.content

            st.success("Content Generated Successfully!")
            st.subheader("Your Generated Content")
            st.markdown(output)
            
            # Download Button for Output
            st.download_button(
                label="Copy / Download Post",
                data=output,
                file_name="generated_post.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")