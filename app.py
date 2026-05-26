import streamlit as st
import pandas as pd
import os

# ----------------------------
# PAGE CONFIG
# ----------------------------

st.set_page_config(
    page_title="StudyBuddy Match",
    page_icon="📚",
    layout="wide"
)

# ----------------------------
# TITLE
# ----------------------------

st.title("📚 StudyBuddy Match")
st.subheader("Find Your Perfect Study Partner")

st.write(
    "Helping students connect, study together, and succeed in exams."
)

# ----------------------------
# FILE SETUP
# ----------------------------

FILE_NAME = "students.csv"

# Create file if it doesn't exist
if not os.path.exists(FILE_NAME):
    df = pd.DataFrame(columns=[
        "Name",
        "Age",
        "Course",
        "Subject",
        "Study Style",
        "Available Time",
        "Goal",
        "Contact"
    ])

    df.to_csv(FILE_NAME, index=False)

# Load existing data
students_df = pd.read_csv(FILE_NAME)

# ----------------------------
# SIDEBAR MENU
# ----------------------------

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Register",
        "Find Study Partners",
        "Study Groups",
        "All Students"
    ]
)

# ----------------------------
# HOME PAGE
# ----------------------------

if menu == "Home":

    st.header("🏠 Welcome")

    st.write(
        "StudyBuddy Match helps students automatically find compatible study partners."
    )

    st.markdown("""
    ### How It Works

    1. Register your details
    2. Choose your subject and study preferences
    3. Get matched with similar students
    4. Form study groups and discuss assignments
    5. Prepare for exams together
    """)

# ----------------------------
# REGISTER PAGE
# ----------------------------

elif menu == "Register":

    st.header("📝 Student Registration")

    with st.form("registration_form"):

        name = st.text_input("Full Name")

        age = st.number_input(
            "Age",
            min_value=15,
            max_value=50,
            step=1
        )

        course = st.selectbox(
            "Course",
            [
                "Computer Science",
                "Business",
                "Engineering",
                "Medicine",
                "Multimedia",
                "Accounting",
                "Other"
            ]
        )

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

        available_time = st.selectbox(
            "Available Time",
            [
                "Morning",
                "Afternoon",
                "Evening",
                "Night",
                "Weekend"
            ]
        )

        goal = st.text_area(
            "What is your study goal?"
        )

        contact = st.text_input(
            "Contact (Email / Instagram / Discord)"
        )

        submitted = st.form_submit_button("Register")

        if submitted:

            new_student = {
                "Name": name,
                "Age": age,
                "Course": course,
                "Subject": subject,
                "Study Style": study_style,
                "Available Time": available_time,
                "Goal": goal,
                "Contact": contact
            }

            students_df.loc[len(students_df)] = new_student

            students_df.to_csv(FILE_NAME, index=False)

            st.success("✅ Registration Successful!")
            st.balloons()

# ----------------------------
# FIND STUDY PARTNERS
# ----------------------------

elif menu == "Find Study Partners":

    st.header("🔍 Find Study Partners")

    if students_df.empty:
        st.warning("No students registered yet.")

    else:

        search_subject = st.text_input(
            "Enter subject to find study partners"
        )

        if st.button("Find Matches"):

            matches = students_df[
                students_df["Subject"].str.lower() == search_subject.lower()
            ]

            if len(matches) > 0:

                st.success(f"Found {len(matches)} study partner(s)!")

                for index, row in matches.iterrows():

                    st.markdown("---")

                    st.subheader(f"👤 {row['Name']}")

                    st.write(f"📘 Course: {row['Course']}")
                    st.write(f"📚 Subject: {row['Subject']}")
                    st.write(f"🧠 Study Style: {row['Study Style']}")
                    st.write(f"⏰ Available Time: {row['Available Time']}")
                    st.write(f"🎯 Goal: {row['Goal']}")
                    st.write(f"📱 Contact: {row['Contact']}")

            else:
                st.error("No matching students found.")

# ----------------------------
# STUDY GROUPS PAGE
# ----------------------------

elif menu == "Study Groups":

    st.header("👥 Study Groups")

    if students_df.empty:
        st.warning("No students registered yet.")

    else:

        grouped = students_df.groupby("Subject")

        for subject, members in grouped:

            st.markdown("---")
            st.subheader(f"📚 {subject} Group")

            st.write(
                f"Total Members: {len(members)}"
            )

            st.dataframe(
                members[
                    [
                        "Name",
                        "Course",
                        "Study Style",
                        "Available Time"
                    ]
                ]
            )

# ----------------------------
# ALL STUDENTS PAGE
# ----------------------------

elif menu == "All Students":

    st.header("📋 Registered Students")

    if students_df.empty:
        st.warning("No students registered yet.")

    else:
        st.dataframe(students_df)