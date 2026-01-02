import sys
import os

# =================================================
# FIX PYTHON PATH (CRITICAL FOR STREAMLIT)
# =================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from agent.agent import run_agent
# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="SAP MM AI Assistant",
    page_icon="📦",
    layout="centered",
)

# =================================================
# GLOBAL STYLES
# =================================================
st.markdown(
    """
<style>
/* =====================================================
   STREAMLIT TOP HEADER — DARK GRADIENT BLUE
===================================================== */

/* Main toolbar */
div[data-testid="stToolbar"] {
    background: linear-gradient(
        135deg,
        #0B1E3A 0%,
        #0F2A4F 45%,
        #0B1E3A 100%
    ) !important;

    border-bottom: 1px solid rgba(56,189,248,0.25) !important;
    box-shadow: 0 10px 30px rgba(0,0,0,0.55) !important;
}

/* Inner wrapper safety */
div[data-testid="stToolbar"] > div {
    background: transparent !important;
}

/* Deploy button */
div[data-testid="stAppDeployButton"] button {
    background: linear-gradient(
        135deg,
        rgba(56,189,248,0.25),
        rgba(99,102,241,0.25)
    ) !important;

    border: 1px solid rgba(56,189,248,0.4) !important;
    color: #EAEAF0 !important;
    border-radius: 10px !important;
    backdrop-filter: blur(12px);
}

/* Deploy button hover */
div[data-testid="stAppDeployButton"] button:hover {
    background: linear-gradient(
        135deg,
        rgba(56,189,248,0.4),
        rgba(99,102,241,0.4)
    ) !important;
}

/* Three-dot menu button */
span[data-testid="stMainMenu"] button {
    color: #EAEAF0 !important;
}

/* Icons inside header */
div[data-testid="stToolbar"] svg {
    fill: #EAEAF0 !important;
    opacity: 0.9;
}

/* Remove default Streamlit grey */
.stAppToolbar {
    background: transparent !important;
}

/* ================= HARD RESET ================= */
html, body, * {
    opacity: 1 !important;
    filter: none !important;
}

/* ================= APP BACKGROUND ================= */
.stApp {
    background: radial-gradient(
        circle at top,
        #111827 0%,
        #0B0F1A 45%,
        #020617 100%
    );
    font-family: Inter, Segoe UI, sans-serif;
    color: #EAEAF0 !important;
}

/* ================= HEADER ================= */
h1 {
    text-align: center;
    font-weight: 700;
    color: #EAEAF0 !important;
}

.subtitle {
    text-align: center;
    color: rgba(234,234,240,0.75);
    margin-bottom: 40px;
}

/* ================= CHAT MESSAGES ================= */
.stChatMessage {
    background: transparent !important;
}

/* ---- USER ---- */
.stChatMessage.user {
    display: flex;
    justify-content: flex-end;
}

.stChatMessage.user > div {
    background: linear-gradient(
        135deg,
        rgba(106,90,205,0.45),
        rgba(0,198,255,0.35)
    );
    border: 1px solid rgba(106,90,205,0.6);
    backdrop-filter: blur(12px);
    color: #EAEAF0 !important;
    border-radius: 22px;
    padding: 14px 18px;
    max-width: 75%;
    box-shadow: 0 0 30px rgba(106,90,205,0.45);
}

/* ---- ASSISTANT ---- */
.stChatMessage.assistant {
    display: flex;
    justify-content: flex-start;
}

.stChatMessage.assistant > div {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.14),
        rgba(255,255,255,0.06)
    );
    border: 1px solid rgba(255,255,255,0.18);
    backdrop-filter: blur(18px);
    color: #EAEAF0 !important;
    border-radius: 22px;
    padding: 14px 18px;
    max-width: 75%;
    box-shadow: 0 14px 40px rgba(0,0,0,0.6);
}

/* Force text brightness */
.stChatMessage * {
    color: #EAEAF0 !important;
}

/* =====================================================
   INPUT AREA — LIGHT DARK GREY (FINAL)
===================================================== */

/* Chat input bar */
section[data-testid="stChatInput"] {
    background: linear-gradient(
        180deg,
        #1F2937,
        #111827
    ) !important;
    border-top: 1px solid rgba(255,255,255,0.12);
    padding: 16px 0 10px 0;
}

/* Remove inner white wrappers */
section[data-testid="stChatInput"] > div,
section[data-testid="stChatInput"] form,
section[data-testid="stChatInput"] form > div {
    background: transparent !important;
    padding-bottom: 0 !important;
}

/* TEXTAREA */
section[data-testid="stChatInput"] textarea {
    background: #2A3344 !important;   /* LIGHT DARK GREY */
    border-radius: 999px !important;
    padding: 16px 24px !important;
    font-size: 15px !important;

    color: #EAEAF0 !important;
    -webkit-text-fill-color: #EAEAF0 !important;
    caret-color: #38BDF8 !important;

    border: 1px solid rgba(255,255,255,0.25) !important;
    width: 100% !important;
}

/* Placeholder */
section[data-testid="stChatInput"] textarea::placeholder {
    color: rgba(234,234,240,0.55) !important;
}

/* Focus */
section[data-testid="stChatInput"] textarea:focus {
    outline: none !important;
    border-color: rgba(56,189,248,0.8) !important;
    box-shadow:
        0 0 0 2px rgba(56,189,248,0.3),
        0 0 30px rgba(106,90,205,0.4);
}

/* SEND BUTTON ALIGNMENT */
section[data-testid="stChatInput"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* REMOVE FOOTER */
footer {
    display: none !important;
}

/* NO WHITE STRIP */
section.main,
section.main > div.block-container {
    background: transparent !important;
    padding-bottom: 0 !important;
}

html, body {
    background: #020617 !important;
}

</style>
""",
    unsafe_allow_html=True
)

# =================================================
# HEADER
# =================================================
st.markdown("<h1>📦 SAP MM AI Assistant</h1>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Intelligent PO, GR & Supplier Analysis Assistant</div>",
    unsafe_allow_html=True
)

# =================================================
# SESSION STATE
# =================================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "👋 **Hey! How can I help you today with PO, GR & Supplier analysis?**"
        }
    ]

# =================================================
# CHAT HISTORY
# =================================================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =================================================
# INPUT
# =================================================
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing SAP MM data..."):
            try:
                response = run_agent(user_input)
            except Exception as e:
                response = f"❌ **Error:** {e}"

            st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )