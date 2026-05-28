import streamlit as st
import streamlit.components.v1 as components
from google import genai
import pandas as pd
import os
from datetime import time

# =========================
# GEMINI API
# =========================

client = genai.Client(
    api_key="YOUR_GEMINI_API_KEY"
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="StudyBuddy Match",
    page_icon="📚",
    layout="wide"
)

# =========================
# DARK / LIGHT MODE
# =========================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# =========================
# CUSTOM CSS
# =========================

if st.session_state.dark_mode:

    background_color = "#0E1117"
    text_color = "white"
    sidebar_color = "#1E1E1E"

else:

    background_color = "white"
    text_color = "black"
    sidebar_color = "white"

st.markdown(f"""
<style>

.stApp {{
    background-color: {background_color};
    color: {text_color};
}}

[data-testid="stSidebar"] {{
    background-color: {sidebar_color};
}}

.search-box {{
    background-color: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 30px;
}}

.profile-card {{
    background-color: rgba(255,255,255,0.85);
    padding: 15px;
    border-radius: 15px;
    margin-top: 20px;
}}

.bottom-menu {{
    position: fixed;
    bottom: 20px;
    left: 20px;
    width: 250px;
}}

</style>
""", unsafe_allow_html=True)

# =========================
# DATABASE
# =========================

FILE_NAME = "students.csv"

if not os.path.exists(FILE_NAME):

    df = pd.DataFrame(columns=[
        "Name",
        "School",
        "Course",
        "Subject",
        "Study Style",
        "Available Time",
        "Preferred Gender",
        "Email"
    ])

    df.to_csv(FILE_NAME, index=False)

students_df = pd.read_csv(FILE_NAME)

# =========================
# SIDEBAR
# =========================

with st.sidebar:

    st.title("📚 StudyBuddy")

    menu = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "👤 Register",
            "🔍 Find Partners",
            "🤖 AI Tutor",
            "⚙ Settings"
        ]
    )

# =========================
# HOME PAGE
# =========================

if menu == "🏠 Home":

    st.title("StudyBuddy Match")

    st.subheader("Find Your Perfect Study Partner")

    # =========================
    # SEARCH PANEL
    # =========================

    with st.expander("🔍 Search Study Partners", expanded=True):

        school = st.selectbox(
            "School",
            [
                "Taylor's University",
                "Sunway University",
                "Monash University Malaysia",
                "APU",
                "INTI",
                "MMU",
                "UTAR",
                "Other"
            ]
        )

        course = st.text_input("Course")

        subject = st.text_input("Subject")

        study_style = st.selectbox(
            "Study Style",
            [
                "Quiet Study",
                "Discussion Based",
                "Group Study",
                "Online Study",
                "Exam Practice"
            ]
        )

        available_time = st.time_input(
            "Available Time",
            value=time(18, 0)
        )

        preferred_gender = st.selectbox(
            "Preferred Gender",
            [
                "No Preference",
                "Male",
                "Female"
            ]
        )

        search_button = st.button("Find Matches")

    # =========================
    # MATCHING SYSTEM
    # =========================

    if search_button:

        matches = students_df[
            (students_df["School"] == school) &
            (students_df["Subject"].str.lower() == subject.lower())
        ]

        if len(matches) > 0:

            st.success(f"Found {len(matches)} study partners!")

            for index, row in matches.iterrows():

                # Prevent matching with self
                if row["Email"] != st.session_state.get("current_user", ""):

                    st.markdown("---")

                    st.markdown(f"""
                    <div class="profile-card">

                    <h3>👤 {row['Name']}</h3>

                    <p>🏫 School: {row['School']}</p>

                    <p>📘 Course: {row['Course']}</p>

                    <p>📚 Subject: {row['Subject']}</p>

                    <p>🧠 Study Style: {row['Study Style']}</p>

                    <p>⏰ Available Time: {row['Available Time']}</p>

                    <p>📧 Email: {row['Email']}</p>

                    </div>
                    """, unsafe_allow_html=True)

        else:

            st.error("No matching students found.")

# =========================
# REGISTER PAGE
# =========================

elif menu == "👤 Register":

    st.title("Student Registration")

    with st.form("register_form"):

        name = st.text_input("Full Name")

        school = st.selectbox(
            "School",
            [
                "Taylor's University",
                "Sunway University",
                "Monash University Malaysia",
                "APU",
                "INTI",
                "MMU",
                "UTAR",
                "Other"
            ]
        )

        course = st.text_input("Course")

        subject = st.text_input("Subject")

        study_style = st.selectbox(
            "Study Style",
            [
                "Quiet Study",
                "Discussion Based",
                "Group Study",
                "Online Study",
                "Exam Practice"
            ]
        )

        available_time = st.time_input(
            "Available Time",
            value=time(18, 0)
        )

        preferred_gender = st.selectbox(
            "Preferred Gender",
            [
                "Male",
                "Female",
                "No Preference"
            ]
        )

        email = st.text_input("Google / Apple / Outlook Email")

        submitted = st.form_submit_button("Register")

        if submitted:

            new_student = {
                "Name": name,
                "School": school,
                "Course": course,
                "Subject": subject,
                "Study Style": study_style,
                "Available Time": str(available_time),
                "Preferred Gender": preferred_gender,
                "Email": email
            }

            students_df.loc[len(students_df)] = new_student

            students_df.to_csv(FILE_NAME, index=False)

            # Save current user
            st.session_state.current_user = email

            st.success("Registration Successful!")

            st.balloons()

# =========================
# AI TUTOR
# =========================

elif menu == "🤖 AI Tutor":

    st.title("Real AI Study Tutor")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.write(message["content"])

    prompt = st.chat_input("Ask your AI tutor...")

    if prompt:

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })

        with st.chat_message("user"):

            st.write(prompt)

        try:

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )

            ai_reply = response.text

        except Exception as e:

            ai_reply = str(e)

        with st.chat_message("assistant"):

            st.write(ai_reply)

        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_reply
        })

# =========================
# SETTINGS
# =========================

elif menu == "⚙ Settings":

    st.title("Settings")

    dark_mode = st.toggle(
        "Enable Dark Mode",
        value=st.session_state.dark_mode
    )

    st.session_state.dark_mode = dark_mode

    privacy = st.selectbox(
        "Privacy Setting",
        [
            "Public",
            "Friends Only",
            "Private"
        ]
    )

    if st.button("Save Settings"):

        st.success("Settings Saved!")

    if st.button("Logout"):

        st.session_state.clear()

        st.warning("Logged Out")

# =========================
# USER BASIC INFO
# =========================

if "current_user" in st.session_state:

    current_email = st.session_state.current_user

    current_user_data = students_df[
        students_df["Email"] == current_email
    ]

    if not current_user_data.empty:

        row = current_user_data.iloc[0]

        st.sidebar.markdown("---")

        st.sidebar.subheader("👤 My Profile")

        st.sidebar.write(f"Name: {row['Name']}")

        st.sidebar.write(f"School: {row['School']}")

        st.sidebar.write(f"Subject: {row['Subject']}")

        st.sidebar.write(f"Email: {row['Email']}")