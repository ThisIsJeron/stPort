import streamlit as st
import requests

# ── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Jeron Wong | DevOps Engineer",
    page_icon="💻",
    layout="wide",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────

st.markdown("""
<style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    .card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1.2rem;
        height: 100%;
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
    .metric-card {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    .metric-card h2 { color: #4FC3F7; margin: 0; }
    .metric-card p { color: #8B949E; margin: 0; }
    .timeline-item {
        border-left: 2px solid #4FC3F7;
        padding-left: 1.2rem;
        margin-bottom: 1.5rem;
    }
    a { color: #4FC3F7; }
</style>
""", unsafe_allow_html=True)

# ── GitHub API ───────────────────────────────────────────────────────────────

GITHUB_USERNAME = "ThisIsJeron"


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


profile, top_repos = fetch_github_data()

# ── 1. Hero ──────────────────────────────────────────────────────────────────

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# Jeron Wong")
    st.markdown("### DevOps Engineer")
    st.markdown("📍 New York, NY")
    link_col1, link_col2, _ = st.columns([1, 1, 3])
    with link_col1:
        st.link_button("GitHub", f"https://github.com/{GITHUB_USERNAME}")
    with link_col2:
        st.link_button("LinkedIn", "https://www.linkedin.com/in/jeronwong/")
with col2:
    if profile and profile.get("avatar_url"):
        st.image(profile["avatar_url"], width=180)

st.divider()

# ── 2. About ─────────────────────────────────────────────────────────────────

st.markdown("## About")
st.markdown(
    "DevOps Engineer with experience building and scaling CI/CD pipelines, cloud infrastructure, "
    "and developer tooling across startups and enterprise. Passionate about automation, observability, "
    "and shipping reliable systems."
)

mcol1, mcol2, mcol3 = st.columns(3)
public_repos = profile.get("public_repos", "—") if profile else "—"
followers = profile.get("followers", "—") if profile else "—"
top_stars = top_repos[0].get("stargazers_count", "—") if top_repos else "—"

with mcol1:
    st.markdown(f'<div class="metric-card"><h2>{public_repos}</h2><p>Public Repos</p></div>', unsafe_allow_html=True)
with mcol2:
    st.markdown(f'<div class="metric-card"><h2>⭐ {top_stars}</h2><p>Top Repo Stars</p></div>', unsafe_allow_html=True)
with mcol3:
    st.markdown(f'<div class="metric-card"><h2>{followers}</h2><p>Followers</p></div>', unsafe_allow_html=True)

st.divider()

# ── 3. Experience ─────────────────────────────────────────────────────────────

st.markdown("## Experience")

experiences = [
    {
        "title": "DevOps Engineer",
        "company": "Reality Defender",
        "date": "Oct 2024 – Present",
        "location": "New York, NY",
        "bullets": [
            "Architected CI/CD pipelines with GitHub Actions, Docker, and Helm for Kubernetes deployments",
            "Managed AWS infrastructure with Terraform, improving deployment reliability and reducing provisioning time",
            "Implemented monitoring and alerting with Datadog, increasing system observability across production services",
        ],
    },
    {
        "title": "DevOps Engineer",
        "company": "Capital Rx",
        "date": "Jan 2023 – Oct 2024",
        "location": "New York, NY",
        "bullets": [
            "Built and maintained CI/CD pipelines using Azure DevOps and GitHub Actions for microservices architecture",
            "Automated infrastructure provisioning with Terraform across Azure cloud environments",
            "Developed internal CLI tooling in Go to streamline developer workflows and reduce onboarding time",
        ],
    },
    {
        "title": "DevOps Engineer",
        "company": "Synopsys",
        "date": "Jun 2021 – Jan 2023",
        "location": "Mountain View, CA",
        "bullets": [
            "Managed Kubernetes clusters and Helm charts for production workloads",
            "Implemented infrastructure-as-code practices with Terraform and Ansible",
            "Built automated testing and deployment pipelines reducing release cycle time",
        ],
    },
    {
        "title": "Software Engineer Intern",
        "company": "HouseKeys",
        "date": "Jun 2020 – Aug 2020",
        "location": "San Jose, CA",
        "bullets": [
            "Developed full-stack features using Python and React for affordable housing platform",
            "Integrated third-party APIs and improved application performance",
        ],
    },
]

for exp in experiences:
    st.markdown(f"""
<div class="timeline-item">
    <strong>{exp['title']}</strong> · {exp['company']}<br>
    <small style="color:#8B949E">{exp['date']} · {exp['location']}</small>
    <ul>{"".join(f"<li>{b}</li>" for b in exp['bullets'])}</ul>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── 4. Skills ─────────────────────────────────────────────────────────────────

st.markdown("## Skills")

skill_categories = {
    "Languages": ["Python", "Go", "Rust", "Bash", "SQL"],
    "Infrastructure": ["Docker", "Kubernetes", "Terraform", "Helm", "Ansible", "GitHub Actions"],
    "Cloud & Monitoring": ["AWS", "Azure", "Datadog", "Linux", "Nginx", "PostgreSQL"],
}

scols = st.columns(3)
for i, (category, skills) in enumerate(skill_categories.items()):
    with scols[i]:
        st.markdown(f"**{category}**")
        badges = "".join(f'<span class="badge">{s}</span>' for s in skills)
        st.markdown(badges, unsafe_allow_html=True)

st.divider()

# ── 5. GitHub Repos ──────────────────────────────────────────────────────────

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
                lang = repo.get("language") or ""
                stars = repo.get("stargazers_count", 0)
                desc = repo.get("description") or "No description"
                st.markdown(f"""
<div class="card">
    <strong>{repo['name']}</strong><br>
    <small style="color:#8B949E">{desc}</small><br><br>
    <span class="badge">{lang}</span> ⭐ {stars}
</div>
""", unsafe_allow_html=True)
                st.link_button("View Repo", repo["html_url"], use_container_width=True)
else:
    st.info("GitHub repos could not be loaded. Visit my profile directly:")
    st.link_button("GitHub Profile", f"https://github.com/{GITHUB_USERNAME}")

st.divider()

# ── 6. Projects & Awards ─────────────────────────────────────────────────────

st.markdown("## Projects & Awards")

pcol1, pcol2 = st.columns(2)
with pcol1:
    st.markdown("""
<div class="card">
    <strong>🏆 ElevenLabs Hackathon — Finalist</strong><br><br>
    Built an AI-powered application during the ElevenLabs hackathon, selected as a finalist
    among competitive entries.
</div>
""", unsafe_allow_html=True)
with pcol2:
    st.markdown("""
<div class="card">
    <strong>🤖 SummaryGPT — Twitter Bot</strong><br><br>
    Created an automated Twitter bot that uses GPT to summarize trending topics and threads,
    gaining organic followers through useful daily summaries.
</div>
""", unsafe_allow_html=True)

st.divider()

# ── 7. Education ──────────────────────────────────────────────────────────────

st.markdown("## Education")
st.markdown("""
<div class="card">
    <strong>University of Illinois at Urbana-Champaign</strong><br>
    B.S. Computer Science and Anthropology<br>
    <small style="color:#8B949E">Champaign, IL</small>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── 8. Contact ────────────────────────────────────────────────────────────────

st.markdown("## Contact")

ccol1, ccol2, ccol3 = st.columns(3)
with ccol1:
    st.markdown("""
<div class="card">
    <strong>LinkedIn</strong><br>
    <small style="color:#8B949E">Connect with me</small>
</div>
""", unsafe_allow_html=True)
    st.link_button("Open LinkedIn", "https://www.linkedin.com/in/jeronwong/", use_container_width=True)
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

# ── 9. Resume Download ───────────────────────────────────────────────────────

st.markdown("## Resume")

try:
    with open("Jeron Wong Resume 2026-3.pdf", "rb") as f:
        pdf_bytes = f.read()
    st.download_button(
        label="📄 Download Resume",
        data=pdf_bytes,
        file_name="Jeron_Wong_Resume.pdf",
        mime="application/pdf",
    )
except FileNotFoundError:
    st.warning("Resume file not found.")
