import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

# Try to import litellm
try:
    import litellm
except ImportError:
    st.error("Missing dependency: litellm. Please install it using 'pip install litellm'.")

st.set_page_config(page_title="Niche Content Calendar Generator", layout="wide")

st.title("🚀 Niche Content Calendar Generator")
st.markdown("Transform your niche into a structured, platform-optimized content plan in seconds.")

# Sidebar for Configuration
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter LLM API Key (OpenAI or Anthropic)", type="password")
    use_mock = st.checkbox("Use Demo/Mock Mode (No API Key needed)", value=False)
    model = st.selectbox("Select Model", ["gpt-4o", "gpt-3.5-turbo", "claude-3-5-sonnet-20240620"])
    
    if api_key:
        if "gpt" in model:
            litellm.openai_key = api_key
        elif "claude" in model:
            litellm.anthropic_key = api_key

# Input Form
with st.form("generator_form"):
    col1, col2 = st.columns(2)
    with col1:
        niche = st.text_input("Niche/Topic (Required)", placeholder="e.g., Vertical farming")
        platform = st.selectbox("Target Platform (Required)", [
            "Instagram (Reels & Carousels Focus)", "TikTok (Short-form Video Focus)", 
            "LinkedIn (Professional Focus)", "Twitter/X (Threads Focus)", "YouTube Shorts"
        ])
    with col2:
        frequency = st.selectbox("Posting Frequency", ["Daily (30 posts)", "5x/week (20 posts)", "3x/week (12 posts)"])
        goal = st.selectbox("Primary Goal", ["Awareness/Reach", "Engagement", "Conversion", "Education"])
    
    submitted = st.form_submit_button("Generate My Calendar")

if submitted:
    if not niche:
        st.error("Please enter a Niche/Topic.")
    elif not api_key and not use_mock:
        st.error("Please enter an API Key or use Demo Mode.")
    else:
        with st.spinner("Generating your strategic content calendar..."):
            if use_mock:
                # Mock data for testing/demo
                data = []
                count = 30 if "Daily" in frequency else (20 if "5x" in frequency else 12)
                for i in range(1, count + 1):
                    data.append({
                        "day": i, "title": f"Post {i} for {niche}", "type": "Story" if i % 2 == 0 else "Tutorial",
                        "cta": f"Like and follow for more {niche} tips!"
                    })
                df = pd.DataFrame(data)
                st.success("✅ Calendar Generated (Demo Mode)")
                st.table(df)
            else:
                # Actual LLM call would go here using litellm.completion
                st.info("In a live environment, this would call the AI with your API Key.")