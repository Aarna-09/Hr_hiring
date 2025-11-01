# import streamlit as st
# from resume_parser import extract_text_from_file
# from ranker import Ranker

# st.set_page_config(page_title='AI HR Hiring Agent', layout='wide')

# st.title('AI-Powered HR Hiring Agent — Starter')

# # 🧭 Sidebar
# with st.sidebar:
#     st.header('Upload')
#     uploaded_jd = st.file_uploader(
#         'Upload Job Description (TXT or PDF)', type=['pdf', 'txt']
#     )
#     uploaded_resumes = st.file_uploader(
#         'Upload Resumes (multiple) — PDF or TXT',
#         accept_multiple_files=True,
#         type=['pdf', 'txt']
#     )
#     top_k = st.slider('Top K results', min_value=1, max_value=10, value=5)

# # 🧠 Main logic
# if uploaded_jd is None:
#     st.info('Upload a job description (PDF or TXT) to start. Example: "Data Scientist with Python, SQL, NLP"')
# else:
#     jd_text = extract_text_from_file(uploaded_jd)
#     st.subheader('Job Description')
#     st.write(jd_text)

#     if len(uploaded_resumes) == 0:
#         st.warning('Upload one or more resumes to match against the JD')
#     else:
#         st.info('Parsing resumes...')
#         resumes = []
#         for f in uploaded_resumes:
#             text = extract_text_from_file(f)
#             resumes.append({'filename': f.name, 'text': text})

#         ranker = Ranker()
#         results = ranker.rank_resumes(jd_text, resumes, top_k=top_k)

#         st.subheader('Top Matches')
#         for i, r in enumerate(results, start=1):
#             st.markdown(f"**{i}. {r['filename']} — Score: {r['score']:.3f}**")
#             preview = r['text'][:500].replace('\n', '  \\\n')
#             st.write(preview)
#             st.write('---')

# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from resume_parser import extract_text_from_file
# from ranker import Ranker
# from keybert import KeyBERT

# # ----------------- PAGE CONFIG -----------------
# st.set_page_config(
#     page_title="AI HR Hiring Agent",
#     layout="wide",
#     page_icon="🤖",
# )

# # ----------------- CUSTOM STYLES -----------------
# st.markdown("""
#     <style>
#         .main {background-color: #F8F9FA;}
#         h1, h2, h3 {color: #2C3E50;}
#         .stButton>button {
#             background-color: #007bff;
#             color: white;
#             border-radius: 8px;
#             height: 3em;
#             width: 100%;
#         }
#         .stProgress > div > div > div > div {
#             background-color: #28a745;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # ----------------- HEADER -----------------
# st.title("🤖 AI-Powered HR Hiring Agent")
# st.write("Analyze, Rank, and Shortlist Candidates Automatically using NLP and Semantic Matching!")

# # ----------------- SIDEBAR -----------------
# with st.sidebar:
#     st.header("📂 Upload Files")
#     uploaded_jd = st.file_uploader("Job Description (TXT or PDF)", type=["pdf", "txt"])
#     uploaded_resumes = st.file_uploader(
#         "Upload Multiple Resumes (TXT or PDF)",
#         type=["pdf", "txt"],
#         accept_multiple_files=True,
#     )
#     top_k = st.slider("Top K Results", 1, 10, 5)
#     st.markdown("---")
#     st.markdown("💡 **Tip:** Upload a technical job description and a few resumes to start ranking candidates!")

# # ----------------- MAIN LOGIC -----------------
# if uploaded_jd is None:
#     st.info("⬅️ Upload a Job Description to begin analysis.")
# else:
#     jd_text = extract_text_from_file(uploaded_jd)
#     st.subheader("📋 Job Description")
#     st.write(jd_text)

#     if len(uploaded_resumes) == 0:
#         st.warning("Please upload one or more resumes for comparison.")
#     else:
#         st.info("🧠 Processing resumes...")

#         resumes = []
#         for f in uploaded_resumes:
#             text = extract_text_from_file(f)
#             resumes.append({"filename": f.name, "text": text})

#         # Initialize ranker
#         ranker = Ranker()
#         results = ranker.rank_resumes(jd_text, resumes, top_k=top_k)

#         # ----------------- DISPLAY RESULTS -----------------
#         st.subheader("🏆 Top Candidate Matches")
#         scores, names = [], []

#         kw_model = KeyBERT()
#         jd_keywords = [kw[0] for kw in kw_model.extract_keywords(jd_text, stop_words='english', top_n=10)]

#         for i, r in enumerate(results, start=1):
#             st.markdown(f"### {i}. {r['filename']}")
#             st.progress(r["score"])
#             st.markdown(f"**Match Score:** {r['score']:.2f}")
#             scores.append(r["score"])
#             names.append(r["filename"])

#             # Extract keywords
#             resume_keywords = [kw[0] for kw in kw_model.extract_keywords(r["text"], stop_words='english', top_n=10)]
#             common_skills = set(jd_keywords).intersection(set(resume_keywords))

#             st.markdown(f"**🧩 Matching Skills:** {', '.join(common_skills) if common_skills else 'None'}")

#             preview = r["text"][:400].replace("\n", "  \\\n")
#             with st.expander("📄 View Resume Snippet"):
#                 st.write(preview)
#             st.markdown("---")

#         # ----------------- VISUALIZE SCORES -----------------
#         st.subheader("📊 Candidate Comparison Chart")
#         df = pd.DataFrame({"Resume": names, "Score": scores})
#         fig = px.bar(df, x="Resume", y="Score", text="Score", color="Score", range_y=[0, 1])
#         st.plotly_chart(fig, use_container_width=True)

#         # ----------------- DOWNLOAD RESULTS -----------------
#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button(
#             label="📥 Download Ranking Results (CSV)",
#             data=csv,
#             file_name="candidate_ranking.csv",
#             mime="text/csv",
#         )

#         st.success("✅ Analysis Complete!")

# # ----------------- FOOTER -----------------
# st.markdown("---")
# st.caption("💼 Built with ❤️ using Streamlit, Sentence Transformers, and KeyBERT.")

import streamlit as st
import pandas as pd
import plotly.express as px
from resume_parser import extract_text_from_file
from ranker import Ranker
from keybert import KeyBERT
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="AI HR Hiring Agent", page_icon="🤖", layout="wide")

# ---------- GLOBAL STYLE ----------
st.markdown("""
<style>
    body {background-color: #f8f9fa;}
    .big-title {font-size: 2.5em; font-weight: 700; color: #2C3E50;}
    .muted {color: #6c757d; font-size: 1.1em;}
    .stProgress > div > div > div > div {background-color: #28a745;}
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        height: 3em;
        font-weight: 600;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SESSION INIT ----------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "resumes" not in st.session_state:
    st.session_state.resumes = []
if "results" not in st.session_state:
    st.session_state.results = []
if "ranking_df" not in st.session_state:
    st.session_state.ranking_df = pd.DataFrame()

# ---------- NAVIGATION ----------
def goto(page_name: str):
    st.session_state.page = page_name

# ---------- HEADER ----------
def render_header():
    c1, c2 = st.columns([4, 1])
    with c1:
        st.markdown('<div class="big-title">🤖 AI HR Hiring Agent</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">Smart resume matching — semantic ranking, skill insights, and automatic shortlisting.</div>', unsafe_allow_html=True)
    with c2:
        if st.button("🏠 Home", key="home_top_button"):
            goto("home")

# ---------- HOME PAGE ----------
def page_home():
    render_header()
    st.markdown("### Welcome to the Future of Hiring 🚀")
    st.markdown("""
    This AI-powered agent helps you **automatically rank resumes** against a given **job description** using Natural Language Processing (NLP) and Semantic Matching.
    """)
    st.markdown("""
    **Capabilities:**
    - 📊 Intelligent resume scoring
    - 🧠 Matching skill extraction (via KeyBERT)
    - 📈 Visual score comparison
    - 💾 CSV report download
    """)
    st.image("https://cdn-icons-png.flaticon.com/512/2721/2721296.png", width=150)
    if st.button("🚀 Start — Upload Job & Resumes", key="start_upload"):
        goto("upload")

# ---------- UPLOAD PAGE ----------
def page_upload():
    render_header()
    st.subheader("📂 Upload Job Description & Resumes")

    jd = st.file_uploader("Upload Job Description (PDF or TXT)", type=["pdf", "txt"], key="jd_upload")
    resumes = st.file_uploader(
        "Upload Resumes (multiple files — PDF or TXT)",
        type=["pdf", "txt"],
        accept_multiple_files=True,
        key="resumes_upload"
    )

    st.session_state.top_k = st.slider("Top K Results", 1, 10, 5, key="slider_top_k")

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("← Back", key="back_from_upload"):
            goto("home")
    with col2:
        if st.button("Save & Continue →", key="continue_to_processing"):
            if jd is None or len(resumes) == 0:
                st.warning("Please upload both a job description and at least one resume.")
            else:
                st.session_state.jd_text = extract_text_from_file(jd)
                parsed = []
                for f in resumes:
                    parsed.append({"filename": f.name, "text": extract_text_from_file(f)})
                st.session_state.resumes = parsed
                goto("processing")
    # with col3:
    #     if st.button("🧹 Clear Inputs", key="clear_inputs"):
    #         st.session_state.jd_text = ""
    #         st.session_state.resumes = []
    #         st.rerun()

# ---------- PROCESSING PAGE ----------
def page_processing():
    render_header()
    st.subheader("⚙️ Processing & Analyzing Resumes")

    with st.spinner("Running NLP pipeline and semantic analysis..."):
        time.sleep(2)
        ranker = Ranker()
        results = ranker.rank_resumes(
            st.session_state.jd_text,
            st.session_state.resumes,
            top_k=st.session_state.top_k
        )
        st.session_state.results = results
        st.session_state.ranking_df = pd.DataFrame(results)
        time.sleep(1)

    st.success("✅ Analysis Complete! Click below to view ranked candidates.")
    if st.button("📊 View Results", key="view_results"):
        goto("results")
    if st.button("← Back", key="back_to_upload"):
        goto("upload")

# ---------- RESULTS PAGE ----------
def page_results():
    render_header()
    st.subheader("🏆 Candidate Ranking Results")

    results = st.session_state.results
    if not results:
        st.warning("No results found. Please upload data and run processing.")
        if st.button("← Back to Upload", key="back_no_results"):
            goto("upload")
        return

    scores, names = [], []
    kw_model = KeyBERT()
    jd_keywords = [kw[0] for kw in kw_model.extract_keywords(st.session_state.jd_text, stop_words='english', top_n=10)]

    for i, r in enumerate(results, start=1):
        st.markdown(f"### {i}. {r['filename']}")
        st.progress(r["score"])
        st.markdown(f"**Match Score:** {r['score']:.2f}")
        scores.append(r["score"])
        names.append(r["filename"])

        resume_keywords = [kw[0] for kw in kw_model.extract_keywords(r["text"], stop_words='english', top_n=10)]
        common_skills = set(jd_keywords).intersection(set(resume_keywords))
        # st.markdown(f"**🧩 Matching Skills:** {', '.join(common_skills) if common_skills else 'None'}")
        if r["matching_skills"]:
            st.success(f"**🧩 Matching Skills:** {', '.join(r['matching_skills'])}")
        else:
            st.error("**🧩 Matching Skills:** None")


        preview = r["text"][:400].replace("\n", "  \\\n")
        with st.expander("📄 View Resume Snippet", expanded=False):
            st.write(preview)
        st.markdown("---")

    # Chart
    df = pd.DataFrame({"Resume": names, "Score": scores})
    fig = px.bar(df, x="Resume", y="Score", text="Score", color="Score", range_y=[0, 1])
    st.plotly_chart(fig, use_container_width=True)

    # Download
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Ranking Results (CSV)",
        data=csv,
        file_name="candidate_ranking.csv",
        mime="text/csv",
        key="download_csv"
    )

    # Navigation
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("← Back to Processing", key="back_to_processing"):
            goto("processing")
    with c2:
        if st.button("Analyze New JD", key="analyze_new_jd"):
            st.session_state.jd_text = ""
            st.session_state.resumes = []
            st.session_state.results = []
            st.session_state.ranking_df = pd.DataFrame()
            goto("upload")
    with c3:
        if st.button("🏠 Home", key="home_from_results"):
            goto("home")

# ---------- ROUTER ----------
def router():
    page = st.session_state.page
    if page == "home":
        page_home()
    elif page == "upload":
        page_upload()
    elif page == "processing":
        page_processing()
    elif page == "results":
        page_results()

# ---------- RUN ----------
router()
