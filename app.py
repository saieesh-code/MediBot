import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# ----------------------------
# LOAD ENV
# ----------------------------
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="MediBot AI Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ----------------------------
# CUSTOM CSS
# ----------------------------
st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(56,189,248,0.12), transparent 25%),
        radial-gradient(circle at bottom right, rgba(99,102,241,0.10), transparent 25%),
        linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
}

.hero {
    padding: 3rem;
    border-radius: 30px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(18px);
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 2rem;
    box-shadow: 0 10px 40px rgba(0,0,0,0.35);
}

.hero-title {
    font-size: 4rem;
    font-weight: 700;
    color: white;
    margin-bottom: 0.5rem;
}

.gradient-text {
    background: linear-gradient(90deg,#38bdf8,#60a5fa,#818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1.1rem;
}

.feature-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 1rem;
    border-radius: 20px;
    text-align: center;
    transition: 0.3s;
}

.feature-card:hover {
    transform: translateY(-4px);
    border: 1px solid #38bdf8;
}

.stChatMessage {
    background: rgba(255,255,255,0.05);
    border-radius: 18px;
    padding: 14px;
    border: 1px solid rgba(255,255,255,0.06);
}

.stChatInputContainer {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

.stButton > button {
    background-color: #1e293b !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
}

.stButton > button:hover {
    border: 1px solid #38bdf8 !important;
    color: #38bdf8 !important;
}

.block-container {
    padding-top: 2rem;
    max-width: 1200px;
}

.badge {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(56,189,248,0.15);
    color: #38bdf8;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.footer {
    text-align: center;
    color: #94a3b8;
    padding-top: 2rem;
}

</style>
""",
    unsafe_allow_html=True
)

# ----------------------------
# API CHECK
# ----------------------------
if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file")
    st.stop()

# ----------------------------
# GEMINI MODEL
# ----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.3
)

# ----------------------------
# PROMPT
# ----------------------------
prompt = ChatPromptTemplate.from_template(
    """
You are MediBot, a professional AI hospital assistant.

Responsibilities:
- Answer hospital-related questions
- Help patients understand symptoms
- Suggest suitable medical departments
- Provide appointment guidance
- Give healthcare assistance
- Recommend emergency care when needed

Rules:
- Never provide unsafe medical advice
- Recommend professional medical consultation for serious issues
- Keep answers concise, accurate, and supportive
- Respond professionally

User Question:
{question}

Answer:
"""
)

# ----------------------------
# CHAIN
# ----------------------------
chain = prompt | llm

# ----------------------------
# HERO SECTION
# ----------------------------
st.markdown(
    """
<div class="hero">
    <div class="badge">AI-Powered Healthcare Assistant</div>
    <div class="hero-title">
        MediBot <span class="gradient-text">AI</span>
    </div>
    <div class="hero-subtitle">
        Next-generation AI healthcare assistant for hospitals, clinics, patient support, healthcare guidance, appointment assistance, and medical information.
    </div>
</div>
""",
    unsafe_allow_html=True
)

# ----------------------------
# PROFESSIONAL INFO SECTION
# ----------------------------
st.markdown(
    """
    <div style="
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        padding: 1.2rem;
        border-radius: 18px;
        margin-bottom: 1.5rem;
    ">
        <h3 style="margin-top:0;color:white;">AI Healthcare Assistant</h3>
        <p style="color:#cbd5e1;margin-bottom:0;">
            Ask healthcare, hospital, symptom, appointment, or emergency-related questions and receive AI-powered assistance instantly.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# SESSION STATE
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------
# DISPLAY CHAT HISTORY
# ----------------------------
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----------------------------
# CHAT INPUT
# ----------------------------
user_input = st.chat_input(
    "Ask any hospital or healthcare-related question..."
)

# quick_prompt removed to avoid undefined variable issues

# ----------------------------
# AI CHAT
# ----------------------------
if user_input:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing your query..."):

            try:

                response = chain.invoke(
                    {
                        "question": user_input
                    }
                )

                ai_response = response.content

                st.markdown(ai_response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": ai_response
                    }
                )

            except Exception as e:

                st.error(f"Error: {str(e)}")

# ----------------------------
# SIDEBAR INFO
# ----------------------------
with st.sidebar:

    st.header("🏥 MediBot")

    st.markdown("""
    ### Features

    - AI Healthcare Assistant
    - Symptom Guidance
    - Medical Department Suggestions
    - Appointment Help
    - Emergency Support
    - Patient Assistance
    """)

    st.markdown("---")

    st.info(
        "This AI assistant provides general healthcare guidance only and does not replace professional medical consultation."
    )

# ----------------------------
# FOOTER
# ----------------------------
st.markdown(
    """
    <div class="footer">
        Powered by Streamlit • LangChain • Gemini 2.5 Flash
    </div>
    """,
    unsafe_allow_html=True
)