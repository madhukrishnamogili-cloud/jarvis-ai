import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="JARVIS AI",
    page_icon="🤖",
    layout="wide"
)

# ---------- JARVIS UI ----------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #10243d, #030712 70%);
    color: white;
}

h1 {
    text-align: center;
    font-size: 50px;
}

.jarvis-title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #00d9ff;
    text-shadow: 0 0 20px #00d9ff;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #a0aec0;
}

.user-message {
    background: #1e293b;
    padding: 12px;
    border-radius: 15px;
    margin: 8px;
}

.jarvis-message {
    background: #062a3a;
    border-left: 4px solid #00d9ff;
    padding: 12px;
    border-radius: 15px;
    margin: 8px;
}

div.stButton > button {
    width: 100%;
    border-radius: 12px;
    font-size: 18px;
    height: 50px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SESSION ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🤖 JARVIS")

    st.write("### Personal AI Assistant")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("### System Status")
    st.success("🟢 JARVIS ONLINE")

    st.write("🧠 AI System: Ready")
    st.write("🎤 Voice: Coming Soon")
    st.write("📅 Tasks: Coming Soon")

# ---------- MAIN ----------
st.markdown('<div class="jarvis-title">🤖 JARVIS</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Your Personal AI Assistant</div>',
    unsafe_allow_html=True
)

st.write("")

current_time = datetime.now().strftime("%I:%M %p")

st.markdown(
    f"<div class='subtitle'>System Time: {current_time}</div>",
    unsafe_allow_html=True
)

st.divider()

# ---------- CHAT HISTORY ----------
for message in st.session_state.messages:

    if message["role"] == "user":
        st.markdown(
            f"<div class='user-message'>👤 <b>You:</b><br>{message['content']}</div>",
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            f"<div class='jarvis-message'>🤖 <b>JARVIS:</b><br>{message['content']}</div>",
            unsafe_allow_html=True
        )

# ---------- CHAT INPUT ----------
user_input = st.chat_input("Ask JARVIS anything...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # Temporary response
    response = (
        f"Hello bro! 🤖 You said: '{user_input}'\n\n"
        "My AI brain will be connected soon! 🔥"
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()