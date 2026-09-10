import streamlit as st
from google import genai
from streamlit_mic_recorder import speech_to_text
import streamlit.components.v1 as components
import json


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="JARVIS AI",
    page_icon="🤖",
    layout="centered"
)


# ==========================================
# GEMINI CONNECTION
# ==========================================

try:
    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

except Exception:
    st.error("❌ GEMINI_API_KEY not found. Check Streamlit Secrets.")
    st.stop()


# ==========================================
# CUSTOM UI
# ==========================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top, #102a43, #020617 65%);
    color: white;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}


/* TITLE */

.jarvis-title {
    text-align: center;
    font-size: 52px;
    font-weight: 800;
    color: #00e5ff;
    text-shadow:
        0px 0px 10px #00e5ff,
        0px 0px 30px #00e5ff;
}

.jarvis-subtitle {
    text-align: center;
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 30px;
}


/* CHAT MESSAGE */

.stChatMessage {
    border-radius: 15px;
}


/* BUTTON */

.stButton > button {

    width: 100%;

    border-radius: 12px;

    border: 1px solid #00d9ff;

}


/* INPUT */

.stChatInput input {

    border-radius: 15px;

}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION MEMORY
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# LANGUAGE DETECTION
# ==========================================

def detect_language(text):

    for char in text:

        if "\u0C00" <= char <= "\u0C7F":

            return "te-IN"

    return "en-US"


# ==========================================
# VOICE OUTPUT
# ==========================================

def speak(text):

    language = detect_language(text)

    clean_text = json.dumps(text)

    components.html(

        f"""

        <script>

        window.speechSynthesis.cancel();

        const speech =
        new SpeechSynthesisUtterance({clean_text});

        speech.lang = "{language}";

        speech.rate = 1;

        speech.pitch = 1;

        window.speechSynthesis.speak(speech);

        </script>

        """,

        height=0

    )


# ==========================================
# HEADER
# ==========================================

st.markdown(

    '<div class="jarvis-title">🤖 JARVIS</div>',

    unsafe_allow_html=True

)


st.markdown(

    '<div class="jarvis-subtitle">Your Personal AI Assistant ⚡</div>',

    unsafe_allow_html=True

)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🤖 JARVIS")

    st.divider()

    st.write("🟢 System Online")

    st.write("🧠 AI: Gemini")

    st.write("🎤 Voice: Telugu + English")

    st.write("🔊 Voice Response: ON")

    st.divider()


    if st.button("🗑️ Clear Conversation"):

        st.session_state.messages = []

        st.rerun()


# ==========================================
# CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])


# ==========================================
# VOICE INPUT
# ==========================================

with st.expander("🎤 Talk to JARVIS"):

    language_choice = st.selectbox(

        "Voice Language",

        [

            "Telugu 🇮🇳",

            "English 🇺🇸"

        ]

    )


    if language_choice == "Telugu 🇮🇳":

        language_code = "te-IN"

    else:

        language_code = "en-US"


    voice_text = speech_to_text(

        language=language_code,

        start_prompt="🎤 Start Speaking",

        stop_prompt="⏹️ Stop",

        just_once=True,

        use_container_width=True,

        key="jarvis_voice"

    )


# ==========================================
# TEXT INPUT
# ==========================================

text_input = st.chat_input(

    "Ask anything to JARVIS..."

)


# ==========================================
# GET USER INPUT
# ==========================================

user_input = None


if voice_text:

    user_input = voice_text


elif text_input:

    user_input = text_input


# ==========================================
# PROCESS REQUEST
# ==========================================

if user_input:


    # SAVE USER MESSAGE

    st.session_state.messages.append(

        {

            "role": "user",

            "content": user_input

        }

    )


    # SHOW USER MESSAGE

    with st.chat_message("user"):

        st.markdown(user_input)


    # JARVIS RESPONSE

    with st.chat_message("assistant"):


        with st.spinner("🤖 JARVIS is thinking..."):


            try:


                system_prompt = f"""

You are JARVIS, an advanced personal AI assistant.

PERSONALITY:

You are:

- Friendly
- Intelligent
- Helpful
- Modern
- Clear

LANGUAGE RULES:

- If the user writes Telugu, respond in Telugu.
- If the user writes English, respond in English.
- If Telugu and English are mixed, naturally respond in Telugu mixed with English.
- Use simple language.
- Explain things clearly.

IMPORTANT:

You are called JARVIS.

You are a helpful personal AI assistant.

USER MESSAGE:

{user_input}

"""


                response = client.models.generate_content(

                    model="gemini-3.6-flash",

                    contents=system_prompt

                )


                answer = response.text


            except Exception as e:


                answer = (

                    "⚠️ JARVIS Error:\n\n"

                    + str(e)

                )


        # SHOW ANSWER

        st.markdown(answer)


        # SPEAK ANSWER

        speak(answer)


    # SAVE AI RESPONSE

    st.session_state.messages.append(

        {

            "role": "assistant",

            "content": answer

        }

    )
