import streamlit as st
import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

# ── PAGE CONFIG ─────────────────────────────────────────

st.set_page_config(
page_title="ResearchMind AI",
page_icon="⚡",
layout="wide"
)

# ── CSS (AI PLAYGROUND UI) ─────────────────────────────

st.markdown("""

<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=Inter:wght@300;400;500&display=swap');

html, body {
    background: #050507;
    color: white;
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 10%, rgba(255,120,40,0.15), transparent 40%),
        radial-gradient(circle at 80% 90%, rgba(255,50,20,0.1), transparent 40%),
        #050507;
}

#MainMenu, footer, header { visibility: hidden; }

/* HERO */
.hero {
    text-align: center;
    margin-top: 8vh;
}
.hero h1 {
    font-family: 'Syne';
    font-size: 64px;
}
.hero span {
    color: #ff7a1a;
    text-shadow: 0 0 20px rgba(255,120,40,0.7);
}

/* INPUT */
.input-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,120,40,0.2);
    border-radius: 16px;
    padding: 20px;
    backdrop-filter: blur(10px);
}

.stTextInput input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,120,40,0.3) !important;
    color: white !important;
    border-radius: 10px !important;
}

.stButton button {
    background: linear-gradient(135deg,#ff7a1a,#ff3c00);
    color: black !important;
    border-radius: 10px;
    font-weight: 700;
}

/* PANELS */
.left-panel, .right-panel {
    background: rgba(255,255,255,0.02);
    border-radius: 14px;
    padding: 18px;
    height: 80vh;
    overflow-y: auto;
}

.right-panel {
    border: 1px solid rgba(255,120,40,0.2);
}

/* CHAT */
.chat {
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.bot { background: rgba(255,255,255,0.05); }
.user { background: rgba(255,120,40,0.2); text-align:right; }

/* HOLOGRAPHIC CARD */
.card {
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 12px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s;
}
.card:hover {
    box-shadow: 0 0 20px rgba(255,120,40,0.3);
    transform: translateY(-3px);
}
</style>

""", unsafe_allow_html=True)

# ── STATE ──────────────────────────────────────────────

for key in ("results", "running", "done"):
    if key not in st.session_state:
        st.session_state[key] = {} if key == "results" else False

# ── HERO ───────────────────────────────────────────────

if not st.session_state.results:
    st.markdown(""" <div class="hero"> <h1>Research<span>Mind</span></h1> <p>AI Agents that search, read, write & critique research</p> </div>
""", unsafe_allow_html=True)

# ── INPUT ──────────────────────────────────────────────

topic = st.text_input("Enter topic", placeholder="e.g AI in Healthcare")

run = st.button("⚡ Run Research")

# ── RUN PIPELINE ───────────────────────────────────────

if run:
    if not topic:
        st.warning("Enter topic")
    else:
        st.session_state.results = {}
        st.session_state.running = True
        st.session_state.done = False
        st.session_state.topic = topic
        st.rerun()

if st.session_state.running and not st.session_state.done:
    topic_val = st.session_state.topic
    results = {}

    # SEARCH
    with st.spinner("Searching..."):
        search_agent = build_search_agent()
        sr = search_agent.invoke({
            "messages": [("user", f"Find info about {topic_val}")]
        })
        results["search"] = sr["messages"][-1].content
        st.session_state.results = dict(results)

    # READER
    with st.spinner("Reading..."):
        reader_agent = build_reader_agent()
        rr = reader_agent.invoke({
            "messages": [("user", f"Analyze:\n{results['search'][:500]}")]
        })
        results["reader"] = rr["messages"][-1].content
        st.session_state.results = dict(results)

    # WRITER
    with st.spinner("Writing..."):
        combined = f"{results['search']}\n\n{results['reader']}"
        results["writer"] = writer_chain.invoke({
            "topic": topic_val,
            "research": combined
        })
        st.session_state.results = dict(results)

    # CRITIC
    with st.spinner("Reviewing..."):
        results["critic"] = critic_chain.invoke({
            "report": results["writer"]
        })
        st.session_state.results = dict(results)

    st.session_state.running = False
    st.session_state.done = True
    st.rerun()

# ── PLAYGROUND UI AFTER RUN ────────────────────────────

r = st.session_state.results

if r:
    left, right = st.columns([3,5])

    # LEFT SIDE (CHAT + AGENTS)
    with left:
        st.markdown('<div class="left-panel">', unsafe_allow_html=True)

        st.markdown("### 🤖 Agents")

        if "search" in r:
            st.markdown('<div class="card">🔍 Search Agent Completed</div>', unsafe_allow_html=True)

        if "reader" in r:
            st.markdown('<div class="card">📄 Reader Extracted Data</div>', unsafe_allow_html=True)

        if "writer" in r:
            st.markdown('<div class="card">✍️ Report Generated</div>', unsafe_allow_html=True)

        if "critic" in r:
            st.markdown('<div class="card">🧐 Critic Review Done</div>', unsafe_allow_html=True)

        st.markdown("### 💬 Chat")

        st.markdown(f'<div class="chat user">{st.session_state.topic}</div>', unsafe_allow_html=True)

        if "search" in r:
            st.markdown('<div class="chat bot">Search completed</div>', unsafe_allow_html=True)

        if "reader" in r:
            st.markdown('<div class="chat bot">Content analyzed</div>', unsafe_allow_html=True)

        if "writer" in r:
            st.markdown('<div class="chat bot">Report ready</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT SIDE (REPORT)
    with right:
        st.markdown('<div class="right-panel">', unsafe_allow_html=True)

        if "writer" in r:
            st.markdown("## 📄 Research Report")
            st.markdown(r["writer"])

        if "critic" in r:
            st.markdown("---")
            st.markdown("## 🧐 Feedback")
            st.markdown(r["critic"])

        st.markdown('</div>', unsafe_allow_html=True)
