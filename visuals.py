"""Large, calm step cues with reduced-motion, dark-mode and narrow-screen support."""
from html import escape

import streamlit as st

# Rendered inline with st.html (no iframe), so every class is prefixed to avoid clashing with Streamlit's own CSS.
STYLE = """
.cue-wrap{--bg1:#eef6fb;--bg2:#fff8e6;--card:#fff;--line:#b9c9d6;--ink:#1d3d55;--accent:#1f6f9f;
  border:1px solid var(--line);border-radius:16px;background:linear-gradient(110deg,var(--bg1),var(--bg2));padding:16px;font-family:system-ui,Arial,sans-serif}
@media(prefers-color-scheme:dark){.cue-wrap{--bg1:#16232b;--bg2:#2a2618;--card:#1d2a33;--line:#3d5466;--ink:#dbe9f3;--accent:#7cc4ee}}
.cue-title{font-size:20px;font-weight:750;color:var(--ink);margin:0 0 12px}
.cue-steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.cue-card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 14px;animation:cue-glow 6s infinite}
.cue-num{font-size:18px;font-weight:800;color:var(--accent)}
.cue-label{font-size:19px;font-weight:650;color:var(--ink)}
.cue-c1{animation-delay:1.5s}.cue-c2{animation-delay:3s}.cue-c3{animation-delay:4.5s}
@keyframes cue-glow{20%{box-shadow:0 4px 10px var(--accent)}}
@media(prefers-reduced-motion:reduce){.cue-card{animation:none}}
"""


def show(title, stages):
    """Render a numbered step cue that wraps on narrow screens."""
    cards = "".join(
        f'<div class="cue-card cue-c{i}"><div class="cue-num">{i + 1}</div><div class="cue-label">{escape(label)}</div></div>'
        for i, label in enumerate(stages)
    )
    st.html(
        f"<style>{STYLE}</style>"
        f'<div class="cue-wrap" role="img" aria-label="{escape(title)}: {escape(" then ".join(stages))}">'
        f'<p class="cue-title">{escape(title)}: remember in 4 steps</p><div class="cue-steps">{cards}</div></div>'
    )


def large_text(size_px):
    """Make all app text bigger for easier reading."""
    st.html(
        "<style>"
        f"html, body, [data-testid='stAppViewContainer'] p, [data-testid='stAppViewContainer'] li, "
        f"[data-testid='stSidebar'] p, label, button {{font-size:{size_px}px !important; line-height:1.6}}"
        "</style>"
    )
