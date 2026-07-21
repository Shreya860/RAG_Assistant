"""
AI Research Assistant — Intelligent Open-Source & Dependency Auditing Dashboard
Owner of this file's UI sections: Member 1 (Frontend Architect & UI Lead)

WHAT THIS FILE DOES (your role):
  - Overall page layout / app flow
  - Sidebar with password-style inputs for API keys (GitHub, Serper, Gemini)
  - Cached resource loading so the app doesn't re-init the RAG pipeline on every rerun
  - Spinners / status updates while the backend does its work
  - Chat-style conversation UI

WHAT'S A PLACEHOLDER (your teammates fill these in):
  - load_rag_index()      -> teammate building LlamaIndex + local HF embeddings
  - query_github_api()    -> teammate building GitHub metrics fetch
  - query_web_search()    -> teammate building Serper search / scraping
  - synthesize_with_gemini() -> teammate building the Gemini synthesis call

Run with:  streamlit run app.py
"""

import streamlit as st
import time

# --- Real teammate imports (confirmed) ---
from rag.loader import load_documents
from rag.storage_manager import get_or_create_index
from rag.retriever import get_retriever
from rag.ai_assistant import GeminiAssistant
try:
    from search_engine import run_serper_search, scrape_documentation_url
    _search_engine_import_error = None
except ImportError as e:
    _search_engine_import_error = str(e)
    def run_serper_search(query, key):
        return "(search_engine.py not working yet — placeholder result)"
    def scrape_documentation_url(url):
        return []

# NOTE: no GitHub metrics function exists in the repo yet (stars/issues/forks).
# query_github_api() below stays a stub until a teammate builds that piece.


# ---------------------------------------------------------------------------
# PAGE CONFIG — must be the first Streamlit call in the script
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="OSS Dependency Auditor",
    page_icon="🔎",
    layout="wide",
)

if _search_engine_import_error:
    st.warning(
        f"search_engine.py couldn't be imported yet ({_search_engine_import_error}). "
        f"Web search will show placeholder text until it's fixed."
    )

# ---------------------------------------------------------------------------
# CUSTOM STYLING — simple chat bubble look
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    .chat-bubble-user {
        background-color: #2b6cb0;
        color: white;
        padding: 10px 14px;
        border-radius: 14px;
        margin: 6px 0;
        max-width: 75%;
        margin-left: auto;
        text-align: left;
    }
    .chat-bubble-assistant {
        background-color: #f1f1f1;
        color: #111;
        padding: 10px 14px;
        border-radius: 14px;
        margin: 6px 0;
        max-width: 75%;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE INIT — persists across Streamlit reruns for one user session
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {"role": "user"/"assistant", "content": str}

if "keys_confirmed" not in st.session_state:
    st.session_state.keys_confirmed = False


# ---------------------------------------------------------------------------
# SIDEBAR — API key inputs (secure, password-masked)
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Configuration")
    st.caption("Keys stay in this browser session only — never written to disk.")

    github_token = st.text_input(
        "GitHub API Token", type="password", key="github_token",
        help="Used to fetch repo stars, open issues, forks."
    )
    serper_key = st.text_input(
        "Serper (Google Search) API Key", type="password", key="serper_key",
        help="Used to pull community threat notices / recent discussions."
    )
    gemini_key = st.text_input(
        "Google Gemini API Key", type="password", key="gemini_key",
        help="Used to synthesize the final risk assessment."
    )

    st.divider()

    if st.button("Save & Initialize", use_container_width=True):
        if github_token and serper_key and gemini_key:
            st.session_state.keys_confirmed = True
            st.success("Keys saved for this session.")
        else:
            st.error("Please fill in all three keys before continuing.")

    st.divider()
    st.caption("Local compliance index status:")
    st.info("Not yet built — see `load_rag_index()`", icon="📄")


# ---------------------------------------------------------------------------
# CACHED RESOURCE LOADING
# @st.cache_resource keeps the RAG index / heavy objects in memory across
# reruns, so Streamlit doesn't rebuild them every time the user types.
# Your RAG teammate will replace the body of this function with real
# LlamaIndex + local HuggingFace embedding logic.
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_rag_index():
    """
    Loads (or builds, first run only) the local compliance index.
    Cached so this only runs once per app session, not on every rerun —
    this is what gives sub-second search after the first load.
    """
    return get_or_create_index(load_documents())


@st.cache_resource(show_spinner=False)
def load_retriever(_index):
    """Cached retriever built from the loaded index."""
    return get_retriever()


@st.cache_resource(show_spinner=False)
def load_gemini_assistant(_gemini_key):
    """Cached GeminiAssistant instance (from rag/ai_assistant.py)."""
    return GeminiAssistant(api_key=_gemini_key)


# ---------------------------------------------------------------------------
# BACKEND HOOK PLACEHOLDERS
# These are the functions your teammates are responsible for. Your job is to
# call them correctly and show the results/states nicely — not to implement
# the logic inside them.
# ---------------------------------------------------------------------------
def query_github_api(package_name: str, token: str) -> dict:
    """
    TODO: swap for the real function once search_engine.py is confirmed.
    Expected to return GitHub metrics (stars, open issues, forks, last commit).
    """
    return {"stars": "N/A", "open_issues": "N/A", "forks": "N/A"}


def query_web_search(package_name: str, serper_key: str) -> str:
    """Real call to search_engine.run_serper_search()."""
    return run_serper_search(package_name, serper_key)


def synthesize_with_gemini(package_name: str, retriever, github_data: dict,
                            web_data: str, gemini_key: str) -> str:
    """
    Calls the real GeminiAssistant.generate_report(...) from rag/ai_assistant.py.
    It expects: package_name, documentation, github_info, web_results.
    'documentation' here comes from querying the local retriever for relevant
    compliance/doc context — adjust once we confirm the exact retriever API.
    """
    assistant = load_gemini_assistant(gemini_key)

    # retriever.retrieve(...) is a common LlamaIndex pattern — confirm the
    # exact method name against retriever.py if this errors.
    docs = retriever.retrieve(package_name)
    documentation = "\n".join(getattr(d, "text", str(d)) for d in docs)

    return assistant.generate_report(
        package_name=package_name,
        documentation=documentation,
        github_info=github_data,
        web_results=web_data,
    )


# ---------------------------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------------------------
st.title("🔎 Intelligent Open-Source & Dependency Auditor")
st.caption("Ask about any package to get a live risk assessment against your internal compliance rules.")

if not st.session_state.keys_confirmed:
    st.warning("Enter and save your API keys in the sidebar to get started.")

# Render existing chat history as bubbles
for msg in st.session_state.messages:
    bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-assistant"
    st.markdown(f'<div class="{bubble_class}">{msg["content"]}</div>', unsafe_allow_html=True)

# Chat input box (pinned to bottom by Streamlit automatically)
user_input = st.chat_input("e.g. Is `left-pad` safe to add to our repo?")

if user_input:
    if not st.session_state.keys_confirmed:
        st.error("Please save your API keys in the sidebar first.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f'<div class="chat-bubble-user">{user_input}</div>', unsafe_allow_html=True)

        status_box = st.status("Running audit...", expanded=True)

        with status_box:
            st.write("📁 Loading local compliance index...")
            index = load_rag_index()
            retriever = load_retriever(index)

            st.write("🌐 Fetching GitHub repository metrics...")
            github_data = query_github_api(user_input, github_token)

            st.write("🔍 Searching for community threat notices...")
            web_data = query_web_search(user_input, serper_key)

            st.write("🤖 Synthesizing risk assessment with Gemini...")
            answer = synthesize_with_gemini(user_input, retriever, github_data, web_data, gemini_key)

        status_box.update(label="Audit complete", state="complete", expanded=False)

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.markdown(f'<div class="chat-bubble-assistant">{answer}</div>', unsafe_allow_html=True)