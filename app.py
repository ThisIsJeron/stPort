import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from streamlit_lottie import st_lottie

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
    html { scroll-behavior: smooth; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }

    .card-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1.2rem;
        box-sizing: border-box;
        display: flex;
        flex-direction: column;
    }
    .card-link {
        text-decoration: none;
        color: inherit;
        display: flex;
    }
    .card-link:hover .card {
        border-color: #4FC3F7;
    }
    .card-link .card {
        flex: 1;
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
    .badge-link {
        text-decoration: none;
    }
    .badge-link:hover .badge {
        border-color: #4FC3F7;
        color: #4FC3F7;
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

    /* ── Section Navigation ── */
    .section-nav {
        position: fixed;
        top: 3.5rem;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        display: flex;
        gap: 0.4rem;
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid #30363D;
        border-radius: 25px;
        padding: 0.4rem 0.8rem;
    }
    .section-nav a {
        color: #8B949E;
        text-decoration: none;
        font-size: 0.8rem;
        padding: 0.3rem 0.7rem;
        border-radius: 15px;
        transition: all 0.2s ease;
        white-space: nowrap;
    }
    .section-nav a:hover {
        color: #E6EDF3;
        background: rgba(79, 195, 247, 0.15);
    }
</style>
"""

# ── Section Navigation HTML ──────────────────────────────────────────────────

SECTION_NAV = """
<div class="section-nav">
    <a href="#skills">Skills</a>
    <a href="#about">About</a>
    <a href="#experience">Experience</a>
    <a href="#repos">Repos</a>
    <a href="#activity">Activity</a>
    <a href="#projects">Projects</a>
    <a href="#education">Education</a>
    <a href="#contact">Contact</a>
</div>
"""

# ── Lottie Helper ────────────────────────────────────────────────────────────

LOTTIE_CODING_URL = "https://assets2.lottiefiles.com/packages/lf20_fcfjwiyb.json"


@st.cache_data(ttl=86400)
def load_lottie_url(url: str):
    """Fetch a Lottie animation JSON from a URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except requests.RequestException:
        pass
    return None


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


@st.cache_data(ttl=3600)
def fetch_github_activity():
    """Fetch recent GitHub push events and group by date (last 30 days)."""
    events = []
    try:
        for page in range(1, 4):
            resp = requests.get(
                f"https://api.github.com/users/{GITHUB_USERNAME}/events",
                params={"per_page": 100, "page": page},
                timeout=10,
            )
            if resp.status_code != 200:
                break
            batch = resp.json()
            if not batch:
                break
            events.extend(batch)
    except requests.RequestException:
        pass

    cutoff = datetime.utcnow() - timedelta(days=30)
    push_counts = {}
    for ev in events:
        if ev.get("type") != "PushEvent":
            continue
        created = ev.get("created_at", "")
        try:
            dt = datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue
        if dt < cutoff:
            continue
        day = dt.strftime("%Y-%m-%d")
        push_counts[day] = push_counts.get(day, 0) + 1

    if not push_counts:
        return None

    today = datetime.utcnow().date()
    all_days = [(today - timedelta(days=i)).isoformat() for i in range(29, -1, -1)]
    df = pd.DataFrame({
        "Date": all_days,
        "Pushes": [push_counts.get(d, 0) for d in all_days],
    })
    df["Date"] = pd.to_datetime(df["Date"])
    return df


# ── Project Detail Dialogs ───────────────────────────────────────────────────

HACKATHON_PROJECTS = [
    {
        "name": "FluffyDuck — Restaurant AI Agent",
        "award": "Finalist · ElevenLabs Worldwide Hackathon",
        "desc": "Multi-channel AI agent system for restaurant marketing using ElevenLabs, fal.ai, and Supabase. Autonomous agents spanning social, email, and phone channels.",
        "tech": ["ElevenLabs", "fal.ai", "Supabase", "Python"],
        "winner": True,
        "link": "https://devpost.com/software/fluffyduck-restaurant-marketing-and-reservations-ai-agent",
    },
    {
        "name": "LINC — LGBTQ In Need of Chatbot",
        "award": "Winner · Best Conversational AI · MHacks 11",
        "desc": "Conversational AI chatbot providing support for LGBTQ individuals via SMS and voice calls. Built with Clinc AI, Twilio, and Google Cloud Platform.",
        "tech": ["Clinc AI", "Twilio", "GCP", "Python"],
        "winner": True,
        "link": "https://devpost.com/software/linc",
    },
    {
        "name": "BasicSloth — Encrypted Radio Comms",
        "award": "Winner · Innovative Use of Speech · YHack 2015",
        "desc": "Encrypted communications over software-defined radio with speech-to-text integration. PGP encryption via GnuRadio and Nuance speech API.",
        "tech": ["GnuRadio", "PGP", "Nuance API", "Python"],
        "winner": True,
        "link": "https://devpost.com/software/basicsloth",
    },
    {
        "name": "ToneFolio — Stock Sentiment Analyzer",
        "award": "Winner · BlackRock Challenge · Cal Hacks 3.0",
        "desc": "Predicts if your stock portfolio is bullish or bearish using IBM Watson Tone Analyzer on financial news, integrated with BlackRock's Aladdin API.",
        "tech": ["IBM Watson", "BlackRock Aladdin API", "Python"],
        "winner": True,
        "link": "https://devpost.com/software/tonefolio",
    },
    {
        "name": "CEEDR — Energy Data Visualization",
        "award": "Winner · Best Use of OSISoft API · HackDavis 2017",
        "desc": "Visualized and predicted UC Davis energy consumption patterns with R/Shiny dashboards and an Amazon Alexa skill for voice-activated data queries.",
        "tech": ["R/Shiny", "OSISoft API", "Amazon Alexa", "AWS Lambda"],
        "winner": True,
        "link": "https://devpost.com/software/ceedr",
    },
    {
        "name": "Emoji Pasta Generator",
        "award": "Winner",
        "desc": "Text transformation tool for generating emoji-enriched content.",
        "tech": ["Python", "NLP"],
        "winner": True,
        "link": "https://devpost.com/software/emojipasta-generator",
    },
    {
        "name": "SummaryGPT — Twitter Bot",
        "award": "10,000+ uses in first month",
        "desc": "Twitter bot leveraging OpenAI API on GCP. When mentioned, replies with an AI-generated summary of the referenced tweet thread.",
        "tech": ["OpenAI API", "GCP", "Twitter API", "Python"],
        "winner": False,
        "link": "https://github.com/ThisIsJeron/SummaryGPT",
    },
]


def _make_project_dialog(proj):
    """Create a dialog function for a specific project."""
    @st.dialog(proj["name"])
    def _dialog():
        icon = "🏆" if proj["winner"] else "🤖"
        st.markdown(f"**{icon} {proj['award']}**")
        st.markdown(proj["desc"])
        st.markdown("**Tech Stack**")
        badges_html = " ".join(f'<span class="badge">{t}</span>' for t in proj["tech"])
        st.markdown(badges_html, unsafe_allow_html=True)
        st.divider()
        st.link_button("View on Devpost / GitHub", proj["link"], use_container_width=True)
    return _dialog


# ── Resume Page (/resume) ────────────────────────────────────────────────────


def resume_page():
    st.markdown("# Jeron Wong — Resume")
    try:
        with open(RESUME_FILE, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="📄 Download Resume (PDF)",
            data=pdf_bytes,
            file_name="Jeron_Wong_Resume.pdf",
            mime="application/pdf",
            type="primary",
        )
    except FileNotFoundError:
        st.error("Resume file not found.")
    st.link_button("← Back to portfolio", "/")


# ── Main Portfolio Page ──────────────────────────────────────────────────────


def main_page():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.html(SECTION_NAV)

    profile, top_repos = fetch_github_data()

    # ── 1. Hero ──────────────────────────────────────────────────────────────

    hero_left, hero_right = st.columns([3, 1])
    with hero_left:
        st.markdown('<p class="hero-name">Jeron Wong</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-subtitle">DevOps / Platform Engineer</p>', unsafe_allow_html=True)
        st.markdown('<p class="hero-location">Berkeley, CA</p>', unsafe_allow_html=True)
    with hero_right:
        lottie_data = load_lottie_url(LOTTIE_CODING_URL)
        if lottie_data:
            st_lottie(lottie_data, height=150, key="hero_lottie")

    _, link_col1, link_col2, _ = st.columns([2, 1, 1, 2])
    with link_col1:
        st.link_button("GitHub", f"https://github.com/{GITHUB_USERNAME}", use_container_width=True)
    with link_col2:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/jeronw/", use_container_width=True)

    st.divider()

    # ── 2. Skills ────────────────────────────────────────────────────────────

    st.markdown('<h2 id="skills">Skills</h2>', unsafe_allow_html=True)

    skill_categories = {
        "Programming Languages": [
            ("Python", "https://www.python.org/"),
            ("Go", "https://go.dev/"),
            ("Rust", "https://www.rust-lang.org/"),
        ],
        "Tools & Libraries": [
            ("Docker", "https://www.docker.com/"),
            ("Kubernetes", "https://kubernetes.io/"),
            ("Terraform", "https://www.terraform.io/"),
            ("Helm", "https://helm.sh/"),
            ("Prometheus", "https://prometheus.io/"),
            ("Grafana", "https://grafana.com/"),
            ("InfluxDB", "https://www.influxdata.com/"),
        ],
        "AI/ML Infrastructure": [
            ("AWS Bedrock", "https://aws.amazon.com/bedrock/"),
            ("SageMaker", "https://aws.amazon.com/sagemaker/"),
            ("RAG Pipelines", None),
            ("ElevenLabs", "https://elevenlabs.io/"),
            ("OpenAI API", "https://platform.openai.com/"),
        ],
        "Environments & Services": [
            ("AWS", "https://aws.amazon.com/"),
            ("Azure", "https://azure.microsoft.com/"),
            ("GitHub", "https://github.com/"),
            ("Linux", "https://www.kernel.org/"),
            ("Datadog", "https://www.datadoghq.com/"),
        ],
        "World Languages": [
            ("English", None),
            ("Mandarin Chinese", None),
        ],
    }

    def _render_skill_badges(categories):
        html = ""
        for category, skills in categories.items():
            badges = ""
            for name, url in skills:
                if url:
                    badges += f'<a href="{url}" target="_blank" class="badge-link"><span class="badge">{name}</span></a>'
                else:
                    badges += f'<span class="badge">{name}</span>'
            html += f'<div><strong>{category}</strong><br><br>{badges}</div>'
        return html

    row1 = {"Programming Languages": skill_categories["Programming Languages"],
            "Tools & Libraries": skill_categories["Tools & Libraries"],
            "AI/ML Infrastructure": skill_categories["AI/ML Infrastructure"]}
    row2 = {"Environments & Services": skill_categories["Environments & Services"],
            "World Languages": skill_categories["World Languages"]}

    st.markdown(
        f'<div class="card-grid" style="grid-template-columns: repeat(3, 1fr);">{_render_skill_badges(row1)}</div>'
        f'<div class="card-grid" style="grid-template-columns: repeat(3, 1fr); margin-top: 1.5rem;">{_render_skill_badges(row2)}</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    # ── 3. About ─────────────────────────────────────────────────────────────

    st.markdown('<h2 id="about">About</h2>', unsafe_allow_html=True)
    st.markdown(
        "DevOps / Platform Engineer with experience building and scaling CI/CD pipelines, cloud infrastructure, "
        "and developer tooling across startups and enterprise. Passionate about automation, observability, "
        "and shipping reliable systems."
    )

    st.divider()

    # ── 4. Experience ────────────────────────────────────────────────────────

    st.markdown('<h2 id="experience">Experience</h2>', unsafe_allow_html=True)

    experiences = [
        {
            "title": "Senior DevOps Engineer",
            "company": "Reality Defender",
            "url": "https://realitydefender.ai/",
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
            "url": "https://www.capitalrx.com/",
            "date": "Feb 2024 – Feb 2025",
            "bullets": [
                "Architected AI infrastructure from the ground up: founding infrastructure engineer for the AI team; stood up Bedrock/SageMaker pipelines powering a RAG chatbot and voice agents serving 50+ staff",
                "Drove 25% latency reduction: deployed Zipkin distributed tracing across 26 microservices and Lambda functions, accelerating root-cause analysis and incident resolution",
            ],
        },
        {
            "title": "Software Engineer — DevOps",
            "company": "Synopsys",
            "url": "https://www.synopsys.com/",
            "date": "Nov 2020 – Feb 2024",
            "bullets": [
                "Spearheaded CI/CD migration to AKS: containerized ARM and PowerPC toolchains and migrated thousands of nightly regressions to Azure Kubernetes Service",
                "Engineered mission-critical observability platform for 4,000+ engineers: built a Telegraf, InfluxDB, and Grafana stack that became the primary source of truth for incident response",
            ],
        },
        {
            "title": "Full Stack Software Engineer",
            "company": "HouseKeys",
            "url": "https://www.housekeys.org/",
            "date": "Aug 2017 – Aug 2019",
            "bullets": [
                "Overhauled analytics infrastructure: replaced legacy Excel-based calculators with R/Shiny dashboards, halving data processing times",
                "Engineered NLP-driven housing discovery pipeline: built Python pipelines that surfaced affordable-housing applications across 30+ Bay Area municipal sites, increasing inventory coverage ~40%",
            ],
        },
    ]

    for exp in experiences:
        company_link = f'<a href="{exp["url"]}" target="_blank">{exp["company"]}</a>'
        st.markdown(f"""
<div class="timeline-item">
    <strong>{exp['title']}</strong> · {company_link}<br>
    <small style="color:#8B949E">{exp['date']}</small>
    <ul>{"".join(f"<li>{b}</li>" for b in exp['bullets'])}</ul>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 5. GitHub Repos ──────────────────────────────────────────────────────

    st.markdown('<h2 id="repos">GitHub Repos</h2>', unsafe_allow_html=True)

    if top_repos:
        cards_html = '<div class="card-grid">'
        for repo in top_repos:
            lang = repo.get("language") or ""
            stars = repo.get("stargazers_count", 0)
            desc = repo.get("description") or "No description"
            url = repo["html_url"]
            cards_html += f"""
<a href="{url}" target="_blank" class="card-link">
<div class="card">
    <strong>{repo['name']}</strong><br>
    <small style="color:#8B949E">{desc}</small>
    <span style="margin-top:auto"><span class="badge">{lang}</span> ⭐ {stars}</span>
</div>
</a>"""
        cards_html += "</div>"
        st.markdown(cards_html, unsafe_allow_html=True)
    else:
        st.info("GitHub repos could not be loaded. Visit my profile directly:")
        st.link_button("GitHub Profile", f"https://github.com/{GITHUB_USERNAME}")

    st.divider()

    # ── 5b. GitHub Activity Chart ────────────────────────────────────────────

    st.markdown('<h2 id="activity">GitHub Activity</h2>', unsafe_allow_html=True)

    activity_df = fetch_github_activity()
    if activity_df is not None:
        st.caption("Push events — last 30 days")
        st.bar_chart(activity_df, x="Date", y="Pushes", color="#4FC3F7")
    else:
        st.info("No recent GitHub activity to display.")

    st.divider()

    # ── 6. Projects & Awards ─────────────────────────────────────────────────

    st.markdown('<h2 id="projects">Projects & Awards</h2>', unsafe_allow_html=True)

    # Build dialog functions once
    dialogs = [_make_project_dialog(p) for p in HACKATHON_PROJECTS]

    # Render project cards as columns with buttons to trigger dialogs
    for row_start in range(0, len(HACKATHON_PROJECTS), 3):
        row_projects = HACKATHON_PROJECTS[row_start:row_start + 3]
        row_dialogs = dialogs[row_start:row_start + 3]
        cols = st.columns(3)
        for idx, (proj, dialog_fn) in enumerate(zip(row_projects, row_dialogs)):
            with cols[idx]:
                icon = "🏆" if proj["winner"] else "🤖"
                st.markdown(f"""
<div class="card">
    <strong>{icon} {proj['name']}</strong><br>
    <small style="color:#4FC3F7">{proj['award']}</small><br><br>
    <span style="color:#8B949E">{proj['desc']}</span>
</div>
""", unsafe_allow_html=True)
                if st.button("View Details", key=f"proj_{row_start + idx}", use_container_width=True):
                    dialog_fn()

    st.link_button("View all projects on Devpost", "https://devpost.com/ThisIsJeron")

    st.divider()

    # ── 7. Education ─────────────────────────────────────────────────────────

    st.markdown('<h2 id="education">Education</h2>', unsafe_allow_html=True)
    st.markdown("""
<div class="card">
    <strong>University of Illinois at Urbana-Champaign</strong><br>
    B.S. Computer Science and Anthropology<br>
    <small style="color:#8B949E">Champaign, IL</small>
</div>
""", unsafe_allow_html=True)

    st.divider()

    # ── 8. Contact ───────────────────────────────────────────────────────────

    st.markdown('<h2 id="contact">Contact</h2>', unsafe_allow_html=True)

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
