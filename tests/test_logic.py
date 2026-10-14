import pytest

from calculations import fd_maturity, inr, interest_payout, life_certificate_window
from datetime import date

from content import FEEDS, HELPLINES, SOURCES, TIP_ICONS, TOPICS
from extras_content import CHECKUPS, HOSPITALS, IMPORTANT_DATES
from features import aqi_level, build_ics, emergency_card_html, heat_level, scam_check, search_tips, tip_of_the_day, upcoming_dates
from weather import parse
from i18n import FEEDS_TE, HELPLINES_TE, TOPICS_TE, UI
from news import parse_feed, summarize

RSS = b"""<rss><channel>
<item><title>Free health camp for seniors in Kukatpally - The Hindu</title><source>The Hindu</source>
<link>https://example.com/a</link><pubDate>Tue, 14 Oct 2026 03:30:00 GMT</pubDate>
<description>&lt;p&gt;The GHMC will hold a free camp on Sunday. Eye and BP checks are included. Bring Aadhaar.&lt;/p&gt;</description></item>
<item><title>Metro timings change</title><link>https://example.com/b</link>
<description>&lt;a href="x"&gt;Metro timings change&lt;/a&gt; Source</description></item>
</channel></rss>"""


def test_inr_uses_indian_grouping():
    assert inr(1234567) == "₹12,34,567"
    assert inr(999) == "₹999"
    assert inr(100000) == "₹1,00,000"
    assert inr(-5000) == "-₹5,000"


def test_fd_maturity_quarterly_compounding():
    assert fd_maturity(100000, 8, 1) == pytest.approx(108243.22, abs=0.01)
    assert fd_maturity(100000, 0, 5) == 100000


def test_interest_payout():
    assert interest_payout(1200000, 8, 12) == pytest.approx(8000)
    assert interest_payout(1200000, 8, 4) == pytest.approx(24000)


def test_life_certificate_window():
    assert life_certificate_window(80).startswith("1 October")
    assert life_certificate_window(70).startswith("1 November")


def test_summarize_keeps_two_sentences():
    assert summarize("One. Two. Three.") == "One. Two."


def test_summarize_drops_text_that_repeats_title():
    assert summarize("<a>Big news</a> Source", "Big news") == ""


def test_parse_feed():
    first, second = parse_feed(RSS)
    assert first["title"] == "Free health camp for seniors in Kukatpally"
    assert first["summary"] == "The GHMC will hold a free camp on Sunday. Eye and BP checks are included."
    assert first["date"].year == 2026
    assert second["summary"] == "" and second["date"] is None
    assert len(parse_feed(RSS, limit=1)) == 1


def test_content_links_and_feeds_exist():
    for topic in TOPICS:
        assert topic["feed"] is None or topic["feed"] in FEEDS
        assert all(name in SOURCES for name in topic["links"])
        assert len(topic["cue"]) == 4


def test_telugu_matches_english():
    assert set(TOPICS_TE) == {t["title"] for t in TOPICS}
    for topic in TOPICS:
        te = TOPICS_TE[topic["title"]]
        assert len(te["tips"]) == len(topic["tips"])
        assert len(te["cue"]) == 4 and te["do"] and te["dont"] and te["takeaway"]
    assert len(HELPLINES_TE) == len(HELPLINES)
    assert set(FEEDS_TE) == set(FEEDS)
    assert set(UI["te"]) - {"windows"} == set(UI["en"])
    assert set(UI["te"]["windows"]) == {life_certificate_window(85), life_certificate_window(70)}


def test_tip_icons_match_tips():
    for topic in TOPICS:
        assert len(TIP_ICONS[topic["title"]]) == len(topic["tips"])
    for row in CHECKUPS + HOSPITALS:
        assert all(row)


def test_every_scam_example_is_red_in_both_languages():
    for lang in ("en", "te"):
        for text in UI[lang]["scam_example_texts"]:
            assert scam_check(text)[0] == "red", text


def test_harmless_message_is_green():
    assert scam_check("Hi amma, I will come for lunch at 1 pm.") == ("green", [])


def test_scam_reasons_strongest_first():
    level, reasons = scam_check("Urgent: share your OTP")
    assert level == "red"
    assert "OTP" in reasons[0][0]


def test_tip_of_the_day_changes_daily():
    first = tip_of_the_day(TOPICS, date(2026, 10, 14))
    assert first == tip_of_the_day(TOPICS, date(2026, 10, 14))
    assert first != tip_of_the_day(TOPICS, date(2026, 10, 15))


def test_search_tips_english_and_telugu():
    topic, tip = search_tips("how to give life certificate", TOPICS)[0]
    assert "life certificate" in tip
    te_topics = [{**t, **TOPICS_TE[t["title"]]} for t in TOPICS]
    topic, tip = search_tips("లైఫ్ సర్టిఫికేట్", te_topics)[0]
    assert "లైఫ్ సర్టిఫికేట్" in tip
    assert search_tips("zzzz qqqq", TOPICS) == []


def test_upcoming_dates_wrap_into_next_year():
    items = upcoming_dates(date(2026, 12, 1))
    assert len(items) == len(IMPORTANT_DATES)
    assert items[0][0] == date(2027, 3, 1)
    assert [d for d, *_ in items] == sorted(d for d, *_ in items)
    assert upcoming_dates(date(2026, 11, 30))[0][0] == date(2026, 11, 30)


def test_build_ics():
    ics = build_ics([(date(2027, 4, 1), "Form 15H, bank; now")])
    assert ics.count("BEGIN:VEVENT") == 1
    assert "DTSTART;VALUE=DATE:20270401" in ics and "RRULE:FREQ=YEARLY" in ics
    assert "SUMMARY:Form 15H\\, bank\\; now" in ics
    assert ics.endswith("END:VCALENDAR\r\n")


def test_emergency_card_escapes_and_skips_empty():
    html = emergency_card_html("Card", [("Name", "<b>Ravi</b>"), ("Allergies", "")], "Call 108")
    assert "&lt;b&gt;Ravi" in html and "Allergies" not in html


def test_weather_levels_and_parse():
    assert heat_level(41) == "danger" and heat_level(36) == "caution" and heat_level(30) == "ok"
    assert [aqi_level(x) for x in (40, 90, 140, 200)] == ["good", "moderate", "sensitive", "unhealthy"]
    forecast = {"current": {"temperature_2m": 30, "apparent_temperature": 33}, "daily": {"temperature_2m_max": [34], "temperature_2m_min": [22], "precipitation_probability_max": [None]}}
    assert parse(forecast, None) == {"temp": 30, "feels_like": 33, "max": 34, "min": 22, "rain_chance": 0, "aqi": None}
    assert parse(forecast, {"current": {"us_aqi": 80}})["aqi"] == 80
