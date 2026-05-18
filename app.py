import streamlit as st
from groq import Groq
import os
import json
import re

from dotenv import load_dotenv
from utils.pdf_reader import extract_text_from_pdf

# Load environment variables
load_dotenv()

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Streamlit Page Config
st.set_page_config(
    page_title="AI Career Preparation Agent",
    layout="wide"
)

# Title
st.title("AI Career Preparation Agent")

st.write("Upload your Resume and Paste Job Description")

# Sidebar
st.sidebar.title("AI Career Coach")

st.sidebar.info(
    """
    Features:
    - ATS Match Score
    - Missing Skills
    - Personalized Roadmap
    - JD-Based Project Suggestions
    - Interview Questions
    """
)

# Upload Resume
uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

# Job Description
job_description = st.text_area(
    "Paste Job Description"
)

# Analyze Button
if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        # Extract Resume Text
        resume_text = extract_text_from_pdf(uploaded_file)

        # Prompt
        prompt = f"""
        You are an expert AI Career Preparation Agent.

        Carefully analyze the candidate's resume against the job description.

        You MUST identify:
        - skills present in both resume and JD
        - skills missing from the resume but required in the JD
        - important technologies not mentioned in the resume
        - weak areas affecting ATS score

        Return ONLY valid JSON.

        Important Instructions:

        1. Suggested projects MUST be NEW.
        2. Do NOT repeat projects already mentioned in the resume.
        3. Generate projects based on:
            - missing skills
            - technologies in the job description
            - industry expectations
            - interview trends

        4. missing_skills must contain:
            - technologies present in JD but absent in resume
            - frameworks missing from resume
            - deployment/cloud tools missing
            - APIs/backend skills missing
            - AI/ML tools missing

        5. Do NOT leave missing_skills empty unless resume fully matches JD.

        6. ATS score should realistically reflect:
            - matching technical skills
            - project relevance
            - missing technologies
            - deployment experience
            - AI/ML exposure

        7. Roadmap should be strategic and realistic.

        JSON format:

        {{
          "ats_score": 0,

          "matching_skills": [],

          "missing_skills": [
            "skill name"
          ],

          "resume_improvements": [],

          "important_topics": [],

          "projects": [
            {{
              "title": "",
              "difficulty": "",
              "description": "",
              "skills_gained": []
            }}
          ],

          "interview_questions": [],

          "roadmap": {{
              "phase1": {{
                  "title": "",
                  "focus": [],
                  "project": ""
              }},
              "phase2": {{
                  "title": "",
                  "focus": [],
                  "project": ""
              }},
              "phase3": {{
                  "title": "",
                  "focus": [],
                  "project": ""
              }},
              "phase4": {{
                  "title": "",
                  "focus": [],
                  "project": ""
              }}
          }}
        }}

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """

        try:

            # AI Response
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            result = response.choices[0].message.content

            # Clean JSON
            result = re.sub(r"```json", "", result)
            result = re.sub(r"```", "", result)

            # Convert JSON to dictionary
            data = json.loads(result)

            # =========================
            # ATS SCORE
            # =========================

            st.subheader("ATS Match Score")

            ats_score = data["ats_score"]

            st.progress(ats_score / 100)

            if ats_score >= 80:
                st.success(f"Excellent Match: {ats_score}%")

            elif ats_score >= 60:
                st.warning(f"Good Match: {ats_score}%")

            else:
                st.error(f"Low Match: {ats_score}%")

            # =========================
            # SKILLS SECTION
            # =========================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Matching Skills")

                for skill in data["matching_skills"]:
                    st.success(skill)

            with col2:

                st.subheader("Missing Skills")

                if data["missing_skills"]:

                    for skill in data["missing_skills"]:
                        st.error(skill)

                else:
                    st.success("No major missing skills detected.")

            # =========================
            # RESUME IMPROVEMENTS
            # =========================

            st.subheader("Resume Improvement Suggestions")

            for item in data["resume_improvements"]:
                st.write(f"• {item}")

            # =========================
            # IMPORTANT TOPICS
            # =========================

            st.subheader("Important Topics To Learn")

            for topic in data["important_topics"]:
                st.write(f"• {topic}")

            # =========================
            # PROJECTS SECTION
            # =========================

            st.subheader("Personalized JD-Based Project Suggestions")

            for project in data["projects"]:

                st.markdown(f"### {project['title']}")

                st.write(
                    f"Difficulty: {project['difficulty']}"
                )

                st.write(project["description"])

                st.write("Skills Gained:")

                for skill in project["skills_gained"]:
                    st.write(f"• {skill}")

                st.divider()

            # =========================
            # ROADMAP SECTION
            # =========================

            st.subheader("Strategic Career Roadmap")

            roadmap = data["roadmap"]

            phase_cols = st.columns(4)

            phases = [
                "phase1",
                "phase2",
                "phase3",
                "phase4"
            ]

            for i, phase in enumerate(phases):

                with phase_cols[i]:

                    st.markdown(
                        f"### {roadmap[phase]['title']}"
                    )

                    st.write("Focus Areas:")

                    for item in roadmap[phase]["focus"]:
                        st.write(f"• {item}")

                    st.write("Recommended Project:")

                    st.success(
                        roadmap[phase]["project"]
                    )

            # =========================
            # INTERVIEW QUESTIONS
            # =========================

            st.subheader("Interview Questions")

            for question in data["interview_questions"]:
                st.write(f"• {question}")

        except Exception as e:

            st.error("Error Processing Response")

            st.write(str(e))

    else:
        st.warning(
            "Please upload resume and paste job description."
        )

# =========================
# FLOATING FOOTER
# =========================

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: auto;
        background-color: #111;
        color: white;
        padding: 10px 18px;
        border-radius: 12px;
        font-size: 14px;
        box-shadow: 0px 0px 10px rgba(0,0,0,0.4);
        z-index: 100;
    }
    </style>

    <div class="footer">
        🚀 Created by Jaswanth
    </div>
    """,
    unsafe_allow_html=True
)
