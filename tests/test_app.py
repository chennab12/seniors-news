"""Smoke tests: every section renders without exceptions, with news fetching stubbed out."""
from unittest.mock import patch

import streamlit as st
from streamlit.testing.v1 import AppTest

from content import TOPICS

WEATHER = {"temp": 31.0, "feels_like": 36.0, "max": 33.0, "min": 22.0, "rain_chance": 60, "aqi": 120}
STORY = {"title": "Metro adds lifts at more stations", "summary": "Lifts open this week.", "source": "Test", "link": "https://example.com", "date": None}


def run(section=None, stories=(STORY,), lang="en"):
    at = AppTest.from_file("../app.py", default_timeout=30)
    at.session_state["lang"] = lang
    if section is not None:
        at.session_state["section"] = section
    with patch("news.fetch_headlines", return_value=list(stories)), patch("weather.fetch_weather", return_value=WEATHER):
        at.run()
    assert not at.exception, at.exception
    return at


def test_every_section_renders():
    at = run()
    for section in at.sidebar.radio[0].options:
        run(section)


def test_every_section_renders_in_telugu():
    for section in run().sidebar.radio[0].options:
        at = run(section, lang="te")
        assert "తెలుగు" in [b.label for b in at.button]


def test_language_buttons_switch_text():
    at = run(f"{TOPICS[1]['icon']} {TOPICS[1]['title']}")
    assert at.header[0].value == "🩺 Health"
    [b for b in at.button if b.label == "తెలుగు"][0].click().run()
    assert at.session_state["lang"] == "te"
    assert at.header[0].value == "🩺 ఆరోగ్యం"
    [b for b in at.button if b.label == "English"][0].click().run()
    assert at.header[0].value == "🩺 Health"


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
    for option in ["fd", "income", "life"]:
        at.button_group[0].set_value(option).run()
        assert not at.exception, at.exception


def test_home_shows_weather_advice_and_tip():
    st.cache_data.clear()
    at = run()
    assert any("Hot" in w.value for w in at.warning)
    assert any("Rain is likely" in i.value for i in at.info)
    assert any("Tip of the day" in m.value for m in at.markdown)


def test_scam_checker_flags_example():
    at = run("🕵️ Scam checker")
    at.text_area[0].input("This is CBI. You are under digital arrest. Share the OTP now.").run()
    assert not at.exception, at.exception
    assert any("SCAM" in e.value for e in at.error)


def test_scam_checker_in_telugu():
    at = run("🕵️ Scam checker", lang="te")
    at.text_area[0].input("మీ ఖాతా ఈ రోజే బ్లాక్ అవుతుంది. వెంటనే OTP చెప్పండి").run()
    assert any("మోసమే" in e.value for e in at.error)


def test_emergency_card_offers_download_once_named():
    at = run("🪪 My emergency card")
    assert len(at.get("download_button")) == 0
    at.text_input[0].input("Lakshmi").run()
    assert not at.exception, at.exception
    assert len(at.get("download_button")) == 1


def test_ask_without_key_shows_matching_tips(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    at = run("💬 Ask a question")
    at.text_input[0].input("How do I give my life certificate?")
    at.button[-1].click().run()
    assert not at.exception, at.exception
    assert any("not switched on" in i.value for i in at.info)
    assert any("Jeevan Pramaan" in m.value or "life certificate" in m.value for m in at.markdown)
