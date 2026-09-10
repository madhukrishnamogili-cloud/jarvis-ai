import streamlit as st
from datetime import datetime
from google import genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import json


# =====================================
# PAGE SETTINGS
# =====================================

st.set_page_config(
    page_title="JARVIS AI",
    page_icon="🤖",
    layout="wide"
)


# =====================================
# GEMINI AI CONNECTION
# =====================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

except Exception:

    st.error(
        "❌ GEMINI_API_KEY not found. Check Streamlit Secrets."
    )

    st.stop()


# =====================================
# JARVIS UI DESIGN
# =====================================

st.markdown("""
<style>

.stApp {
    background: radial-gradient(
        circle at top,
        #10243d,
        #030712 70%
    );
}

.jarvis-title {
    text-align: center;
    font-size: 60px;
    font-weight: bold;
    color: #00d9ff;
    text-shadow:
        0 0 10px #00d9ff,
        0 0 30px #00d9ff;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #a0aec0;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# CHAT MEMORY
# =====================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# =====================================
# JARVIS VOICE OUTPUT
# =====================================

def speak(text):

    clean_text = json.dumps(text)

    components.html(

        f"""
        <script>

        const speech = new SpeechSynthesisUtterance(
            {clean_text}
        );

        speech.rate = 1;
        speech.pitch = 1;

        window.speechSynthesis.cancel();

        window.speechSynthesis.speak(
            speech
        );

        </script>
        """,

        height=0,

    )


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.title("🤖 JARVIS")

    st.write("### Personal AI Assistant")

    st.divider()


    if st.button("🗑️ Clear Chat"):

        st.session_state.messages = []

        st.rerun()


    st.divider()


    st.success("🟢 JARVIS ONLINE")

    st.write("🧠 AI Brain: Gemini")

    st.write("🎤 Voice Input: Active")

    st.write("🔊 Voice Output: Active")

    st.write("🧠 Memory: Chat Session")


# =====================================
# MAIN TITLE
# =====================================

st.markdown(

    '<div class="jarvis-title">🤖 JARVIS</div>',

    unsafe_allow_html=True

)


st.markdown(

    '<div class="subtitle">'
    'Your Personal AI Assistant'
    '</div>',

    unsafe_allow_html=True

)


# =====================================
# SYSTEM TIME
# =====================================

current_time = datetime.now().strftime(
    "%I:%M %p"
)


st.markdown(

    f'<div class="subtitle">'
    f'System Time: {current_time}'
    f'</div>',

    unsafe_allow_html=True

)


st.divider()


# =====================================
# SHOW CHAT HISTORY
# =====================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# =====================================
# VOICE INPUT
# =====================================

st.markdown("### 🎤 Speak to JARVIS")

voice_text = speech_to_text(

    language="en",

    start_prompt="🎤 Start Speaking",

    stop_prompt="⏹️ Stop",

    just_once=True,

    use_container_width=True,

    key="jarvis_voice"

)


# =====================================
# TEXT INPUT
# =====================================

text_input = st.chat_input(

    "Type your message to JARVIS..."

)


# =====================================
# SELECT USER INPUT
# =====================================

user_input = None


if voice_text:

    user_input = voice_text


elif text_input:

    user_input = text_input


# =====================================
# JARVIS RESPONSE
# =====================================

if user_input:


    # -----------------------------
    # SAVE USER MESSAGE
    # -----------------------------

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_input

        }

    )


    # -----------------------------
    # DISPLAY USER MESSAGE
    # -----------------------------

    with st.chat_message("user"):

        st.markdown(
            user_input
        )


    # -----------------------------
    # JARVIS THINKING
    # -----------------------------

    with st.chat_message("assistant"):


        with st.spinner(

            "JARVIS is thinking... 🤖"

        ):


            try:


                prompt = f"""

You are JARVIS, a futuristic AI assistant.

Your personality:

- Friendly
- Intelligent
- Helpful
- Professional
- Speak Telugu when the user speaks Telugu
- Speak English when the user speaks English
- You may naturally call the user "bro"
- Explain difficult topics simply
- Give clear and useful answers
- Your name is JARVIS

Keep responses natural and conversational.

User:

{user_input}

"""


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=prompt

                )


                answer = response.text


            except Exception as e:


                answer = (

                    "⚠️ JARVIS Error:\n\n"

                    + str(e)

                )


        # -----------------------------
        # DISPLAY ANSWER
        # -----------------------------

        st.markdown(
            answer
        )


        # -----------------------------
        # VOICE OUTPUT
        # -----------------------------

        speak(answer)


    # -----------------------------
    # SAVE JARVIS RESPONSE
    # -----------------------------

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer

        }

    )
