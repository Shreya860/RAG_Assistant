import os
import re
import requests
from dotenv import load_dotenv
load_dotenv()
GITHUB_API_BASE = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
def _headers():
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return headers

def parse_repo_url(url_or_slug: str):
    """Accepts 'owner/repo' or a full GitHub URL -> (owner, repo)."""
    match = re.search(r"github\.com/([^/]+)/([^/]+)", url_or_slug.strip())
    owner, repo = match.groups() if match else url_or_slug.strip().split("/", 1)
    return owner, repo.removesuffix(".git").rstrip("/")

def _get(url, params=None):
    response = requests.get(url, headers=_headers(), params=params, timeout=10)
    if response.status_code == 202:
        return None  # GitHub is still computing this (e.g. commit stats) — retry later
    if response.status_code == 403 and "rate limit" in response.text.lower():
        raise RuntimeError("GitHub API rate limit hit. Set GITHUB_TOKEN in .env.")
    response.raise_for_status()
    return response.json()

def _issue_count(owner: str, repo: str, state: str) -> int:
    result = _get(
        f"{GITHUB_API_BASE}/search/issues",
        params={"q": f"repo:{owner}/{repo} type:issue state:{state}"},
    )
    return result.get("total_count", 0)

def _commits_last_30_days(owner: str, repo: str):
    """None means GitHub is still computing stats — try again shortly."""
    weeks = _get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/stats/commit_activity")
    if weeks is None:
        return None
    return sum(w.get("total", 0) for w in weeks[-4:])

def _recent_releases(owner: str, repo: str, limit: int = 3):
    releases = _get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}/releases", params={"per_page": limit})
    return [
        {"tag": r.get("tag_name", "unknown"), "published_at": r.get("published_at", "unknown"),
         "notes": (r.get("body") or "").strip()[:400]}
        for r in releases
    ]

def fetch_repo_metrics(owner_or_slug: str, repo: str = None) -> dict:
    """
    fetch_repo_metrics("numpy", "numpy") / ("numpy/numpy") / ("https://github.com/numpy/numpy")
    """
    owner, repo = (owner_or_slug, repo) if repo else parse_repo_url(owner_or_slug)
    repo_data = _get(f"{GITHUB_API_BASE}/repos/{owner}/{repo}")

    return {
        "full_name": repo_data.get("full_name"),
        "stars": repo_data.get("stargazers_count", 0),
        "forks": repo_data.get("forks_count", 0),
        "open_issues": _issue_count(owner, repo, "open"),
        "closed_issues": _issue_count(owner, repo, "closed"),
        "commits_last_30_days": _commits_last_30_days(owner, repo),
        "recent_releases": _recent_releases(owner, repo),
        # Free fields already present on repo_data — no extra API call —
        # and the strongest maintenance-health signals available.
        "archived": repo_data.get("archived", False),
        "last_pushed": repo_data.get("pushed_at"),
    }

def _metrics_rows(metrics: dict):
    """Single source of truth for the flat metric list — used by both formatters below."""
    commits = metrics["commits_last_30_days"]
    return [
        ("Repository", metrics["full_name"]),
        ("Stars", metrics["stars"]),
        ("Forks", metrics["forks"]),
        ("Open Issues", metrics["open_issues"]),
        ("Closed Issues", metrics["closed_issues"]),
        ("Commits (last 30d)", commits if commits is not None else "Pending"),
        ("Last Pushed", metrics["last_pushed"] or "Unknown"),
        ("Archived", "Yes" if metrics["archived"] else "No"),
    ]

def format_metrics_as_text(metrics: dict) -> str:
    """Feed straight into GeminiAssistant.generate_report(github_info=...)."""
    lines = [f"{label}: {value}" for label, value in _metrics_rows(metrics)]
    releases = "\n".join(
        f"- {r['tag']} ({r['published_at']}): {r['notes'] or 'No notes provided.'}"
        for r in metrics["recent_releases"]
    ) or "No releases published."
    return "\n".join(lines) + "\n\nRecent Releases:\n" + releases

def format_metrics_as_dataframe(metrics: dict):
    """One table for st.dataframe(...) covering every requested metric."""
    import pandas as pd
    latest_release = metrics["recent_releases"][0]["tag"] if metrics["recent_releases"] else "None"
    rows = _metrics_rows(metrics) + [("Latest Release", latest_release)]
    return pd.DataFrame(rows, columns=["Metric", "Value"])

def render_github_section(owner_or_slug: str, repo: str = None) -> str:
    """
    Drop-in Streamlit section:
        from github_metrics import render_github_section
        github_context_text = render_github_section("numpy/numpy")
    Returns the text block for GeminiAssistant.generate_report(github_info=...).
    """
    import streamlit as st
    metrics = fetch_repo_metrics(owner_or_slug, repo)
    st.subheader(f" GitHub Telemetry — {metrics['full_name']}")
    st.dataframe(format_metrics_as_dataframe(metrics), use_container_width=True)
    if metrics["recent_releases"]:
        st.caption("Recent release notes")
        for r in metrics["recent_releases"]:
            st.write(f"**{r['tag']}** ({r['published_at']}): {r['notes'][:200]}")
    return format_metrics_as_text(metrics)
if __name__ == "__main__":
    m = fetch_repo_metrics("numpy/numpy")
    print(format_metrics_as_text(m))