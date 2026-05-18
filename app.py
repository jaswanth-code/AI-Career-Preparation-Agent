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
# FUTURISTIC UI DESIGN
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

    h1, h2, h3 {
        color: white;
        font-weight: bold;
    }

    .main-title {
        font-size: 60px;
        font-weight: 800;
        background: linear-gradient(
            90deg,
            #38bdf8,
            #8b5cf6
        );
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-top: 30px;
    }

    .subtitle {
        font-size: 22px;
        color: #cbd5e1;
        margin-bottom: 30px;
    }

    .feature-card {
        background-color: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0px 0px 20px rgba(59,130,246,0.2);
        text-align: center;
        height: 180px;
    }

    .feature-title {
        font-size: 22px;
        font-weight: bold;
        color: #38bdf8;
    }

    .feature-text {
        color: #cbd5e1;
        margin-top: 10px;
    }

    .stButton>button {
        background: linear-gradient(
            90deg,
            #2563eb,
            #9333ea
        );
        color: white;
        border-radius: 12px;
        height: 3.2em;
        width: 100%;
        font-size: 18px;
        font-weight: bold;
        border: none;
    }

    .stButton>button:hover {
        background: linear-gradient(
            90deg,
            #1d4ed8,
            #7e22ce
        );
    }

    section[data-testid="stSidebar"] {
        background-color: #020617;
    }

    .footer {
        position: fixed;
        bottom: 20px;
        left: 20px;
        width: auto;
        background-color: rgba(255,255,255,0.08);
        color: white;
        padding: 10px 18px;
        border-radius: 12px;
        font-size: 14px;
        backdrop-filter: blur(10px);
        box-shadow: 0px 0px 20px rgba(59,130,246,0.3);
        z-index: 100;
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
            Upload your resume and get personalized AI-powered
            career guidance, ATS analysis, roadmap generation,
            and interview preparation.
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:

    st.image(
        "ai_banner.png",
        use_container_width=True
    )

# =========================
# FEATURE CARDS
# =========================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                ATS Score
            </div>

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
            <div class="feature-title">
                Missing Skills
            </div>

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
            <div class="feature-title">
                Roadmap
            </div>

            <div class="feature-text">
                Get strategic personalized learning paths.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-title">
                AI Projects
            </div>

            <div class="feature-text">
                Generate JD-based project recommendations.
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
        You are an expert AI Career Preparation Agent.

        Analyze the resume against the job description.

        Return ONLY valid JSON.

        {{
          "ats_score": 0,
          "matching_skills": [],
          "missing_skills": [],
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

                    for item in roadmap[phase]["focus"]:
                        st.write(f"• {item}")

                    st.success(
                        roadmap[phase]["project"]
                    )

            # =========================
            # PROJECTS
            # =========================

            st.subheader("Suggested Projects")

            for project in data["projects"]:

                st.markdown(
                    f"### {project['title']}"
                )

                st.write(
                    f"Difficulty: {project['difficulty']}"
                )

                st.write(project["description"])

                st.write("Skills Gained:")

                for skill in project["skills_gained"]:
                    st.write(f"• {skill}")

                st.divider()

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
    <div class="footer">
        🚀 Created by Jaswanth
    </div>
    """,
    unsafe_allow_html=True
)
