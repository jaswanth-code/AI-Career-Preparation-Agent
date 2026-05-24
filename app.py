import streamlit as st
from groq import Groq
import os
import json
import re

from dotenv import load_dotenv
from utils.pdf_reader import extract_text_from_pdf

# =========================
# LOAD ENV VARIABLES
# =========================

load_dotenv()

# =========================
# GROQ CLIENT
# =========================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Career Preparation Agent",
    layout="wide"
)

# =========================
# CUSTOM UI
# =========================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            to right,
            #020617,
            #0f172a,
            #111827
        );
        color: white;
    }

    .main-title {
        font-size: 65px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #38bdf8,
            #8b5cf6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 20px;
    }

    .subtitle {
        font-size: 22px;
        color: #cbd5e1;
        margin-top: 20px;
        margin-bottom: 30px;
    }

    .footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        background-color: rgba(255,255,255,0.08);
        color: white;
        padding: 10px 18px;
        border-radius: 12px;
        font-size: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 0px 20px rgba(59,130,246,0.3);
        z-index: 100;
    }

    .stButton > button {
        background: linear-gradient(
            90deg,
            #2563eb,
            #9333ea
        );
        color: white;
        border: none;
        border-radius: 12px;
        height: 3.2em;
        font-size: 18px;
        font-weight: bold;
        width: 100%;
        box-shadow: 0px 0px 20px rgba(59,130,246,0.3);
    }

    .stButton > button:hover {
        background: linear-gradient(
            90deg,
            #1d4ed8,
            #7e22ce
        );
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    .stFileUploader label,
    .stTextArea label {
        color: #38bdf8 !important;
        font-size: 20px !important;
        font-weight: bold !important;
    }

    [data-testid="stFileUploader"] {
        background: rgba(255,255,255,0.06);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(56,189,248,0.4);
        box-shadow: 0px 0px 20px rgba(56,189,248,0.15);
    }

    [data-testid="stTextArea"] textarea {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 15px !important;
        border: 1px solid rgba(56,189,248,0.4) !important;
        box-shadow: 0px 0px 15px rgba(56,189,248,0.15);
        font-size: 16px !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #94a3b8 !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        border: 1px solid #38bdf8 !important;
        box-shadow: 0px 0px 20px rgba(56,189,248,0.4) !important;
        color: white !important;
    }

    .feature-card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 18px;
        text-align: left;
        box-shadow: 0px 0px 20px rgba(59,130,246,0.25);
        margin-top: 20px;
    }

    .feature-title {
        font-size: 22px;
        font-weight: bold;
        color: #38bdf8;
        margin-bottom: 10px;
    }

    .feature-text {
        color: #cbd5e1;
        font-size: 15px;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# HERO SECTION
# =========================

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown(
        """
        <div class="main-title">
            AI Career<br>
            Preparation Agent
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="subtitle">
            Upload your resume and get AI-powered ATS analysis,
            missing skills detection, roadmap generation,
            project suggestions, and interview preparation.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.image(
        "ai_banner.png",
        width=400
    )

# =========================
# FEATURE CARDS
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">ATS Score</div>
            <div class="feature-text">
                Analyze resume compatibility instantly.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">Missing Skills</div>
            <div class="feature-text">
                Discover important skills missing in your resume.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">Roadmap</div>
            <div class="feature-text">
                Get personalized learning roadmap.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">AI Projects</div>
            <div class="feature-text">
                Generate JD-based AI project ideas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# INPUT SECTION
# =========================

st.divider()

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze Resume"):

    if uploaded_file and job_description:

        resume_text = extract_text_from_pdf(uploaded_file)

        prompt = f"""
        Analyze the resume against the job description.

        Return ONLY valid JSON.

        {{
          "ats_score": 0,

          "matching_skills": [],

          "missing_skills": [],

          "roadmap": [
            {{
              "step": "",
              "description": ""
            }}
          ],

          "suggested_projects": [
            {{
              "project_name": "",
              "project_description": "",
              "skills_gained": []
            }}
          ],

          "interview_questions": []
        }}

        Rules:
        1. Do NOT return markdown
        2. Do NOT return ```json
        3. Do NOT return explanations outside JSON
        4. suggested_projects must NOT contain braces
        5. roadmap must contain minimum 5 learning steps
        6. skills_gained should contain technical skills learned from project

        Resume:
        {resume_text}

        Job Description:
        {job_description}
        """

        try:

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

            result = re.sub(r"```json", "", result)
            result = re.sub(r"```", "", result)

            data = json.loads(result)

            # =========================
            # ATS SCORE
            # =========================

            st.subheader("ATS Match Score")

            ats_score = data["ats_score"]

            st.progress(ats_score / 100)

            st.success(f"ATS Score: {ats_score}%")

            # =========================
            # SKILLS
            # =========================

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Matching Skills")

                for skill in data["matching_skills"]:
                    st.success(skill)

            with col2:

                st.subheader("Missing Skills")

                for skill in data["missing_skills"]:
                    st.error(skill)

            # =========================
            # ROADMAP
            # =========================

            st.subheader("Learning Roadmap")

            for item in data["roadmap"]:

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <div class="feature-title">
                            {item['step']}
                        </div>

                        <div class="feature-text">
                            {item['description']}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # =========================
            # SUGGESTED PROJECTS
            # =========================

            st.subheader("Suggested Projects")

            for project in data["suggested_projects"]:

                skills_html = ""

                for skill in project["skills_gained"]:

                    skills_html += f"""
                    <li>{skill}</li>
                    """

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <div class="feature-title">
                            {project['project_name']}
                        </div>

                        <div class="feature-text">
                            {project['project_description']}
                        </div>

                        <br>

                        <div style="
                            color:#38bdf8;
                            font-weight:bold;
                            margin-bottom:10px;
                        ">
                            Skills Gained
                        </div>

                        <ul style="
                            color:white;
                            text-align:left;
                        ">
                            {skills_html}
                        </ul>

                    </div>
                    """,
                    unsafe_allow_html=True
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
# FOOTER
# =========================

st.markdown(
    """
    <div class="footer">
        🚀 Created by Jaswanth
    </div>
    """,
    unsafe_allow_html=True
)
