import pytest

from calculations import fd_maturity, inr, interest_payout, life_certificate_window
from content import FEEDS, SOURCES, TOPICS
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
