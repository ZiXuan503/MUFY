import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["AIzaSyB5_Fo9R367Iw1DkxwddWkonayJLn7lTQE"])

st.set_page_config(page_title="StudyBuddy Match", page_icon="📚", layout="wide")

with open("studybuddy.html", "r", encoding="utf-8") as f:
    html_src = f.read()

# ── Patch 1: inject the API key so the HTML can call Gemini directly ──
# Replace the empty key initialisation with the real key from secrets
html_src = html_src.replace(
    'let geminiApiKey = localStorage.getItem("gemini_api_key") || "";',
    f'let geminiApiKey = "{st.secrets["AIzaSyB5_Fo9R367Iw1DkxwddWkonayJLn7lTQE"]}";'
)

# ── Patch 2: upgrade model to gemini-2.5-flash (higher free quota) ──
html_src = html_src.replace(
    "gemini-2.0-flash",
    "gemini-2.5-flash"
)

# ── Patch 3: hide the API key banner entirely (key is baked in) ──
html_src = html_src.replace(
    "// Show API key banner if key not set\n  const banner=document.getElementById(\"api-key-banner\");\n  banner.classList.toggle(\"visible\", !geminiApiKey);",
    "document.getElementById(\"api-key-banner\").classList.remove(\"visible\");"
)

# ── Patch 4: skip the key-check gate in the send handler ──
html_src = html_src.replace(
    '    // Gemini tutor\n    if(!geminiApiKey){\n      document.getElementById("api-key-banner").classList.add("visible");\n      chatInput.value=txt; chatSend.disabled=false; return;\n    }\n    tutorMessages.push({role:"user",text:txt});',
    '    // Gemini tutor (key injected server-side)\n    tutorMessages.push({role:"user",text:txt});'
)

st.components.v1.html(html_src, height=900, scrolling=True)