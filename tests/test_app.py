"""Smoke tests: every section renders without exceptions, with news fetching stubbed out."""
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

from content import TOPICS

STORY = {"title": "Metro adds lifts at more stations", "summary": "Lifts open this week.", "source": "Test", "link": "https://example.com", "date": None}


def run(section=None, stories=(STORY,)):
    at = AppTest.from_file("../app.py", default_timeout=30)
    if section is not None:
        at.session_state["section"] = section
    with patch("news.fetch_headlines", return_value=list(stories)):
        at.run()
    assert not at.exception, at.exception
    return at


def test_every_section_renders():
    at = run()
    for section in at.sidebar.radio[0].options:
        run(section)


def test_news_failure_shows_friendly_message():
    st.cache_data.clear()  # earlier tests cached stubbed stories
    at = AppTest.from_file("../app.py", default_timeout=30)
    at.session_state["section"] = f"{TOPICS[0]['icon']} {TOPICS[0]['title']}"
    with patch("news.fetch_headlines", side_effect=OSError("offline")):
        at.run()
    assert not at.exception, at.exception
    assert any("could not be loaded" in w.value for w in at.warning)


def test_next_topic_button_advances():
    at = run(f"{TOPICS[0]['icon']} {TOPICS[0]['title']}")
    [b for b in at.button if b.label == "Next topic →"][0].click().run()
    assert at.session_state["section"] == f"{TOPICS[1]['icon']} {TOPICS[1]['title']}"


def test_each_tool_renders():
    at = run("🧮 Simple money tools")
    for option in ["Fixed deposit growth", "Monthly interest income", "Life certificate dates"]:
        at.button_group[0].set_value(option).run()
        assert not at.exception, at.exception
