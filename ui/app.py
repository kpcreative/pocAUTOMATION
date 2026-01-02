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
# 🔥 ABSOLUTE HARD RESET + FIXED UI
# =================================================
st.markdown(
    """
<style>

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
    color: rgba(234,234,240,0.75) !important;
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

/* 🔥 FORCE MESSAGE TEXT FULL BRIGHT */
.stChatMessage p,
.stChatMessage span,
.stChatMessage div {
    color: #EAEAF0 !important;
    opacity: 1 !important;
}

/* ================= INPUT BAR ================= */
section[data-testid="stChatInput"] {
    background: linear-gradient(
        180deg,
        rgba(11,15,26,0.95),
        rgba(11,15,26,1)
    );
    border-top: 1px solid rgba(255,255,255,0.12);
    backdrop-filter: blur(24px);
    padding: 18px 0 8px 0;
}

/* ================= TEXTAREA FIX (CRITICAL) ================= */
textarea {
    background: rgba(15,23,42,0.98) !important;
    border-radius: 999px !important;
    padding: 16px 24px !important;
    font-size: 15px !important;

    /* 🔥 THIS IS THE REAL FIX */
    color: #EAEAF0 !important;
    -webkit-text-fill-color: #EAEAF0 !important;
    caret-color: #00C6FF !important;

    opacity: 1 !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
}

/* Placeholder */
textarea::placeholder {
    color: rgba(15,23,42,0.98) !important;
    -webkit-text-fill-color: rgba(234,234,240,0.55) !important;
}

/* Focus ring FIX */
textarea:focus,
textarea:focus-visible {
    outline: none !important;
    border-color: rgba(0,198,255,0.8) !important;
    box-shadow:
        0 0 0 2px rgba(0,198,255,0.3),
        0 0 35px rgba(106,90,205,0.55) !important;
}

/* Kill browser / Streamlit outlines */
*:focus {
    outline: none !important;
}

/* ================= REMOVE FOOTER ================= */
footer {
    display: none !important;
}

/* ================= SCROLLBAR ================= */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: rgba(255,255,255,0.22);
    border-radius: 4px;
}
/* ================= REMOVE RED VALIDATION OUTLINE ================= */

/* Kill outline on chat input wrapper */
section[data-testid="stChatInput"],
section[data-testid="stChatInput"] * {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Kill browser validation ring */
form:has(textarea),
div:has(textarea) {
    outline: none !important;
    box-shadow: none !important;
    border: none !important;
}

/* Safari / Chrome autofill & validation */
textarea:-webkit-autofill,
textarea:-webkit-autofill:focus {
    -webkit-box-shadow: 0 0 0px 1000px rgba(15,23,42,0.98) inset !important;
    -webkit-text-fill-color: #EAEAF0 !important;
}

/* Absolute nuclear option */
*:focus-visible {
    outline: none !important;
}
/* =========================================================
   REMOVE LEFT EMPTY / ROUNDED AREA (REAL FIX)
========================================================= */

/* Outer wrapper of chat input */
section[data-testid="stChatInput"] > div {
    padding-left: 0 !important;
    padding-right: 0 !important;
    background: transparent !important;
}

/* Inner wrapper */
section[data-testid="stChatInput"] > div > div {
    padding-left: 0 !important;
    background: transparent !important;
}

/* Force textarea to start from extreme left */
section[data-testid="stChatInput"] textarea {
    margin-left: 0 !important;
    width: 100% !important;
}

/* Remove any min-width or inset spacing */
section[data-testid="stChatInput"] * {
    box-sizing: border-box !important;
}

/* =========================================================
   FIX 1 — KILL WHITE AREA BELOW CHAT INPUT
========================================================= */

/* Section itself */
section[data-testid="stChatInput"] {
    background: linear-gradient(
        180deg,
        rgba(11,15,26,0.95),
        rgba(11,15,26,1)
    ) !important;
}

/* Immediate Streamlit wrapper */
section[data-testid="stChatInput"] > div {
    background: linear-gradient(
        180deg,
        rgba(11,15,26,0.95),
        rgba(11,15,26,1)
    ) !important;
    padding-bottom: 0 !important;
}

/* Form wrapper */
section[data-testid="stChatInput"] form {
    background: transparent !important;
    padding-bottom: 0 !important;
}

/* Inner layout div */
section[data-testid="stChatInput"] form > div {
    background: transparent !important;
}

/* Absolute bottom safety (kills Safari white bleed) */
section[data-testid="stChatInput"]::after {
    content: "";
    display: block;
    height: 8px;
    background: linear-gradient(
        180deg,
        rgba(11,15,26,1),
        rgba(11,15,26,1)
    );
}


/* =========================================================
   FIX 2 — PERFECT SEND ARROW ALIGNMENT
========================================================= */

/* Button wrapper */
section[data-testid="stChatInput"] button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    height: 100% !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

/* SVG icon itself */
section[data-testid="stChatInput"] button svg {
    display: block !important;
    margin: auto !important;
    vertical-align: middle !important;
}
/* =========================================================
   🔥 FINAL FINAL FIX — REMOVE INPUT AREA WHITE STRIP
========================================================= */

/* Kill Streamlit white block behind input */
section.main {
    background: transparent !important;
}

/* MAIN CULPRIT */
section.main > div.block-container {
    background: transparent !important;
    padding-bottom: 0 !important;
}

/* Ensure dark bg continues till bottom */
div[data-testid="stAppViewContainer"] {
    background: radial-gradient(
        circle at top,
        #111827 0%,
        #0B0F1A 45%,
        #020617 100%
    ) !important;
}

/* Chat input wrapper blend */
section[data-testid="stChatInput"] {
    background: linear-gradient(
        180deg,
        rgba(11,15,26,0.98),
        rgba(11,15,26,1)
    ) !important;
    margin-bottom: 0 !important;
}

/* Safety for extreme bottom (Windows + Chrome) */
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