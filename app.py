import streamlit as st
from openai import OpenAI
import os

# --- Page Config ---
st.set_page_config(
    page_title="Claude Bot: Perfect AI Coding Partner",
    page_icon="🤖",
    layout="wide"
)

# --- Custom CSS for "Good UI" ---
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stChatMessage {
        background-color: #262730;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 10px;
    }
    h1 {
        color: #FF4B4B;
    }
    .stSidebar {
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Configuration")
    st.write("Enter your OpenRouter API Key to start chatting.")
    
    api_key = st.text_input("OpenRouter API Key", type="password", help="Get your key from openrouter.ai")
    
    st.divider()
    st.markdown("### Model Settings")
    model = st.selectbox("Select Model", ["anthropic/claude-3.5-sonnet", "anthropic/claude-3-opus", "anthropic/claude-3-haiku"], index=0)
    
    st.divider()
    st.image(
    "https://drive.google.com/uc?export=view&id=1wYSMgJtARFdvTt5g7E20mE4NmwUFUuog",
    width=200
)
    st.markdown("Made with ❤️ by BuildFastWithAI")

# --- Initialize Chat History ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": """You are Claude, the "Perfect AI Coding Partner". It is your job to help the user write excellent, bug-free, and efficient code.

Follow these strict guidelines:
1.  **Code Formatting**: ALWAYS use Markdown code blocks (e.g. ```python) for any code you generate. Never output code as plain text.
2.  **Quality**: Your code should be production-ready, clean, and follow best practices.
3.  **Explanation**: Explain your logic clearly. Focus on *why* you made specific design choices.
4.  **Error Handling**: Always include error handling where appropriate.
5.  **Persona**: Be professional, encouraging, and technically precise. You are a senior software engineer pairing with the user."""}
    ]

# --- Main Interface ---
st.title("🤖 Claude Bot: Perfect AI Coding Partner")
st.caption("Powered by OpenRouter & Streamlit")

# Display chat messages (excluding system prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat Input
if prompt := st.chat_input("How can I help you code today?"):
    # Check for API Key
    if not api_key:
        st.warning("⚠️ Please enter your OpenRouter API Key in the sidebar to continue.")
        st.stop()

    # Add user message to state and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"An error occurred: {e}")
            full_response = "I encountered an error. Please check your API key and try again."

    # Add assistant message to state
    st.session_state.messages.append({"role": "assistant", "content": full_response})
