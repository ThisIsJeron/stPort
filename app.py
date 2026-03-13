import base64

import streamlit as st
import requests

RESUME_FILE = "Jeron Wong Resume 2026-3.pdf"
GITHUB_USERNAME = "ThisIsJeron"

# ── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Jeron Wong | DevOps / Platform Engineer",
    page_icon="💻",
    layout="wide",
)

# ── Shared CSS ───────────────────────────────────────────────────────────────

SHARED_CSS = """
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    /* Force equal-height columns */
    [data-testid="stHorizontalBlock"] {
        align-items: stretch !important;
    }
    [data-testid="stColumn"] > div,
    [data-testid="stColumn"] > div > div,
    [data-testid="stColumn"] > div > div > div {
        height: 100%;
    }

    .card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1.2rem;
        height: 100%;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }
    .card-link {
        text-decoration: none;
        color: inherit;
        display: block;
        height: 100%;
    }
    .card-link:hover .card {
        border-color: #4FC3F7;
    }
    .badge {
        display: inline-block;
        background-color: #1F2937;
        border: 1px solid #30363D;
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        font-size: 0.85rem;
        color: #E6EDF3;
    }
    .hero-name {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        margin-bottom: 0 !important;
        line-height: 1.2 !important;
    }
    .hero-subtitle {
        font-size: 1.3rem !important;
        text-align: center !important;
        color: #8B949E !important;
        margin-top: 0 !important;
    }
    .hero-location {
        text-align: center !important;
        color: #8B949E !important;
    }
    .timeline-item {
        border-left: 2px solid #4FC3F7;
        padding-left: 1.2rem;
        margin-bottom: 1.5rem;
    }
    a { color: #4FC3F7; }
</style>
"""

# ── GitHub API ───────────────────────────────────────────────────────────────


@st.cache_data(ttl=3600)
def fetch_github_data():
    """Fetch GitHub profile and top repos. Returns (profile, repos) or fallbacks."""
    profile = None
    repos = []
    try:
        resp = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}",
            timeout=10,
        )
        if resp.status_code == 200:
            profile = resp.json()

        resp = requests.get(
            f"https://api.github.com/users/{GITHUB_USERNAME}/repos",
            params={"per_page": 100},
            timeout=10,
        )
        if resp.status_code == 200:
            all_repos = resp.json()
            repos = sorted(all_repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:6]
    except requests.RequestException:
        pass
    return profile, repos


# ── Resume Page (/resume) ────────────────────────────────────────────────────


def resume_page():
    st.markdown("## Downloading Resume...")
    try:
        with open(RESUME_FILE, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        st.markdown(
            f'<meta http-equiv="refresh" content="3;url=/">'
            f'<a id="dl" href="data:application/pdf;base64,{b64}" '
            f'download="Jeron_Wong_Resume.pdf">Click here if download does not start</a>'
            f'<script>document.getElementById("dl").click();</script>',
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error("Resume file not found.")


# ── Main Portfolio Page ──────────────────────────────────────────────────────


def main_page():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)

    profile, top_repos = fetch_github_data()

    # ── 1. Hero ──────────────────────────────────────────────────────────────

    st.markdown('<p class="hero-name">Jeron Wong</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">DevOps / Platform Engineer</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-location">Berkeley, CA</p>', unsafe_allow_html=True)

    _, link_col1, link_col2, _ = st.columns([2, 1, 1, 2])
    with link_col1:
        st.link_button("GitHub", f"https://github.com/{GITHUB_USERNAME}", use_container_width=True)
    with link_col2:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/jeronw/", use_container_width=True)

    st.divider()

    # ── 2. Skills ────────────────────────────────────────────────────────────

    st.markdown("## Skills")

    skill_categories = {
        "Languages": ["Python", "Go", "Rust"],
        "Tools & Infrastructure": ["Docker", "Kubernetes", "Terraform", "Helm", "GitHub Actions"],
        "Cloud & Monitoring": ["AWS", "Azure", "Datadog", "Linux"],
    }

    scols = st.columns(3)
    for i, (category, skills) in enumerate(skill_categories.items()):
        with scols[i]:
            st.markdown(f"**{category}**")
            badges = "".join(f'<span class="badge">{s}</span>' for s in skills)
            st.markdown(badges, unsafe_allow_html=True)

    st.divider()

    # ── 3. About ─────────────────────────────────────────────────────────────

    st.markdown("## About")
    st.markdown(
        "DevOps / Platform Engineer with experience building and scaling CI/CD pipelines, cloud infrastructure, "
        "and developer tooling across startups and enterprise. Passionate about automation, observability, "
        "and shipping reliable systems."
    )

    st.divider()

    # ── 4. Experience ────────────────────────────────────────────────────────

    st.markdown("## Experience")

    experiences = [
        {
            "title": "Senior DevOps Engineer",
            "company": "Reality Defender",
            "date": "Feb 2025 – Present",
            "bullets": [
                "Architected agentic CI/CD pipelines: designed and deployed AI-driven CI/CD workflows that autonomously detect build failures, triage root causes, and trigger corrective actions",
                "Engineered agentic observability platform: built self-configuring dashboards using Prometheus and Datadog that automatically surface anomalies and correlate alerts across multi-region EKS clusters",
                "Slashed GPU spend ~30%: authored reusable Terraform module library and automated shutdown of idle GPU nodes",
            ],
        },
        {
            "title": "Senior DevOps Engineer",
            "company": "Capital Rx",
            "date": "Feb 2024 – Feb 2025",
            "bullets": [
                "Architected AI infrastructure from the ground up: founding infrastructure engineer for the AI team; stood up Bedrock/SageMaker pipelines powering a RAG chatbot and voice agents serving 50+ staff",
                "Drove 25% latency reduction: deployed Zipkin distributed tracing across 26 microservices and Lambda functions, accelerating root-cause analysis and incident resolution",
            ],
        },
        {
            "title": "Software Engineer — DevOps",
            "company": "Synopsys",
            "date": "Nov 2020 – Feb 2024",
            "bullets": [
                "Spearheaded CI/CD migration to AKS: containerized ARM and PowerPC toolchains and migrated thousands of nightly regressions to Azure Kubernetes Service",
                "Engineered mission-critical observability platform for 4,000+ engineers: built a Telegraf, InfluxDB, and Grafana stack that became the primary source of truth for incident response",
            ],
        },
        {
            "title": "Full Stack Software Engineer",
            "company": "HouseKeys",
            "date": "Aug 2017 – Aug 2019",
            "bullets": [
                "Overhauled analytics infrastructure: replaced legacy Excel-based calculators with R/Shiny dashboards, halving data processing times",
                "Engineered NLP-driven housing discovery pipeline: built Python pipelines that surfaced affordable-housing applications across 30+ Bay Area municipal sites, increasing inventory coverage ~40%",
            ],
        },
    ]

    for exp in experiences:
        st.markdown(f"""
<div class="timeline-item">
    <strong>{exp['title']}</strong> · {exp['company']}<br>
    <small style="color:#8B949E">{exp['date']}</small>
    <ul>{"".join(f"<li>{b}</li>" for b in exp['bullets'])}</ul>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 5. GitHub Repos ──────────────────────────────────────────────────────

    st.markdown("## GitHub Repos")

    if top_repos:
        for row_start in range(0, len(top_repos), 3):
            cols = st.columns(3)
            for j, col in enumerate(cols):
                idx = row_start + j
                if idx >= len(top_repos):
                    break
                repo = top_repos[idx]
                with col:
                    with st.container():
                        lang = repo.get("language") or ""
                        stars = repo.get("stargazers_count", 0)
                        desc = repo.get("description") or "No description"
                        url = repo["html_url"]
                        st.markdown(f"""
<a href="{url}" target="_blank" class="card-link">
<div class="card">
    <strong>{repo['name']}</strong><br>
    <small style="color:#8B949E">{desc}</small><br><br>
    <span style="margin-top:auto"><span class="badge">{lang}</span> ⭐ {stars}</span>
</div>
</a>
""", unsafe_allow_html=True)
    else:
        st.info("GitHub repos could not be loaded. Visit my profile directly:")
        st.link_button("GitHub Profile", f"https://github.com/{GITHUB_USERNAME}")

    st.divider()

    # ── 6. Projects & Awards ─────────────────────────────────────────────────

    st.markdown("## Projects & Awards")

    hackathon_projects = [
        {
            "name": "FluffyDuck — Restaurant AI Agent",
            "award": "Finalist · ElevenLabs Worldwide Hackathon",
            "desc": "Multi-channel AI agent system for restaurant marketing using ElevenLabs, fal.ai, and Supabase. Autonomous agents spanning social, email, and phone channels.",
            "winner": True,
            "link": "https://devpost.com/software/fluffyduck-restaurant-marketing-and-reservations-ai-agent",
        },
        {
            "name": "LINC — LGBTQ In Need of Chatbot",
            "award": "Winner · Best Conversational AI · MHacks 11",
            "desc": "Conversational AI chatbot providing support for LGBTQ individuals via SMS and voice calls. Built with Clinc AI, Twilio, and Google Cloud Platform.",
            "winner": True,
            "link": "https://devpost.com/software/linc",
        },
        {
            "name": "BasicSloth — Encrypted Radio Comms",
            "award": "Winner · Innovative Use of Speech · YHack 2015",
            "desc": "Encrypted communications over software-defined radio with speech-to-text integration. PGP encryption via GnuRadio and Nuance speech API.",
            "winner": True,
            "link": "https://devpost.com/software/basicsloth",
        },
        {
            "name": "ToneFolio — Stock Sentiment Analyzer",
            "award": "Winner · BlackRock Challenge · Cal Hacks 3.0",
            "desc": "Predicts if your stock portfolio is bullish or bearish using IBM Watson Tone Analyzer on financial news, integrated with BlackRock's Aladdin API.",
            "winner": True,
            "link": "https://devpost.com/software/tonefolio",
        },
        {
            "name": "CEEDR — Energy Data Visualization",
            "award": "Winner · Best Use of OSISoft API · HackDavis 2017",
            "desc": "Visualized and predicted UC Davis energy consumption patterns with R/Shiny dashboards and an Amazon Alexa skill for voice-activated data queries.",
            "winner": True,
            "link": "https://devpost.com/software/ceedr",
        },
        {
            "name": "Emoji Pasta Generator",
            "award": "Winner",
            "desc": "Text transformation tool for generating emoji-enriched content.",
            "winner": True,
            "link": "https://devpost.com/software/emojipasta-generator",
        },
        {
            "name": "SummaryGPT — Twitter Bot",
            "award": "10,000+ uses in first month",
            "desc": "Twitter bot leveraging OpenAI API on GCP. When mentioned, replies with an AI-generated summary of the referenced tweet thread.",
            "winner": False,
            "link": "https://github.com/ThisIsJeron/SummaryGPT",
        },
    ]

    for row_start in range(0, len(hackathon_projects), 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            idx = row_start + j
            if idx >= len(hackathon_projects):
                break
            proj = hackathon_projects[idx]
            icon = "🏆" if proj["winner"] else "🤖"
            with col:
                with st.container():
                    st.markdown(f"""
<a href="{proj['link']}" target="_blank" class="card-link">
<div class="card">
    <strong>{icon} {proj['name']}</strong><br>
    <small style="color:#4FC3F7">{proj['award']}</small><br><br>
    <span style="color:#8B949E">{proj['desc']}</span>
</div>
</a>
""", unsafe_allow_html=True)

    st.link_button("View all projects on Devpost", "https://devpost.com/ThisIsJeron")

    st.divider()

    # ── 7. Education ─────────────────────────────────────────────────────────

    st.markdown("## Education")
    st.markdown("""
<div class="card">
    <strong>University of Illinois at Urbana-Champaign</strong><br>
    B.S. Computer Science and Anthropology<br>
    <small style="color:#8B949E">Champaign, IL</small>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 8. Contact ───────────────────────────────────────────────────────────

    st.markdown("## Contact")

    ccol1, ccol2, ccol3 = st.columns(3)
    with ccol1:
        st.markdown("""
<div class="card">
    <strong>LinkedIn</strong><br>
    <small style="color:#8B949E">Connect with me</small>
</div>
""", unsafe_allow_html=True)
        st.link_button("Open LinkedIn", "https://www.linkedin.com/in/jeronw/", use_container_width=True)
    with ccol2:
        st.markdown("""
<div class="card">
    <strong>GitHub</strong><br>
    <small style="color:#8B949E">Check out my code</small>
</div>
""", unsafe_allow_html=True)
        st.link_button("Open GitHub", f"https://github.com/{GITHUB_USERNAME}", use_container_width=True)
    with ccol3:
        st.markdown("""
<div class="card">
    <strong>Email</strong><br>
    <small style="color:#8B949E">jeronwong@gmail.com</small>
</div>
""", unsafe_allow_html=True)
        st.link_button("Send Email", "mailto:jeronwong@gmail.com", use_container_width=True)

    st.divider()

    # ── 9. Resume Download ───────────────────────────────────────────────────

    st.markdown("## Resume")

    try:
        with open(RESUME_FILE, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📄 Download Resume",
            data=pdf_bytes,
            file_name="Jeron_Wong_Resume.pdf",
            mime="application/pdf",
        )
    except FileNotFoundError:
        st.warning("Resume file not found.")


# ── Navigation (handles /resume path) ────────────────────────────────────────

pg = st.navigation(
    [
        st.Page(main_page, title="Home", url_path="", default=True),
        st.Page(resume_page, title="Resume", url_path="resume"),
    ],
    position="hidden",
)
pg.run()
