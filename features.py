"""Plain logic for the helper pages; no Streamlit here so it is easy to test."""
import re
from datetime import date, timedelta
from html import escape

from extras_content import IMPORTANT_DATES, SCAM_RULES

# Split on spaces and punctuation; \w alone would break Telugu words at vowel signs.
WORD = re.compile(r"[^\s.,:;!?()'\"‘’“”/–—-]+")


def scam_check(message):
    """(level, reasons) where level is 'red', 'amber' or 'green'; reasons are (English, Telugu) pairs."""
    text = (message or "").lower()
    hits = [(weight, en, te) for pattern, weight, en, te in SCAM_RULES if re.search(pattern, text)]
    score = sum(weight for weight, _, _ in hits)
    level = "red" if score >= 4 else "amber" if score >= 2 else "green"
    return level, [(en, te) for _, en, te in sorted(hits, key=lambda h: -h[0])]


def all_tips(topics):
    """Flatten topics into (topic, tip) pairs in order."""
    return [(t, tip) for t in topics for tip in t["tips"]]


def tip_of_the_day(topics, day):
    """The same tip all day, a different one each day."""
    tips = all_tips(topics)
    return tips[day.toordinal() % len(tips)]


def search_tips(question, topics, limit=3):
    """Tips sharing the most words with the question, best first."""
    words = {w for w in WORD.findall(question.lower()) if len(w) > 2}
    scored = []
    for topic, tip in all_tips(topics):
        overlap = len(words & set(WORD.findall((tip + " " + topic["title"]).lower())))
        if overlap:
            scored.append((overlap, topic, tip))
    scored.sort(key=lambda s: -s[0])
    return [(topic, tip) for _, topic, tip in scored[:limit]]


def upcoming_dates(today, extra=()):
    """Reminders as (date, icon, English, Telugu), soonest first, within the next year."""
    items = []
    for month, day, icon, en, te in list(IMPORTANT_DATES) + list(extra):
        when = date(today.year, month, day)
        if when < today:
            when = date(today.year + 1, month, day)
        items.append((when, icon, en, te))
    return sorted(items)


def build_ics(events):
    """A calendar file with yearly all-day reminders; events are (date, title)."""
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Hyderabad Seniors Corner//EN", "CALSCALE:GREGORIAN"]
    for i, (when, title) in enumerate(events):
        title = title.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;")
        lines += [
            "BEGIN:VEVENT",
            f"UID:seniors-corner-{i}-{when:%m%d}@seniors-news",
            "DTSTAMP:20260101T000000Z",
            f"DTSTART;VALUE=DATE:{when:%Y%m%d}",
            f"DTEND;VALUE=DATE:{when + timedelta(days=1):%Y%m%d}",
            "RRULE:FREQ=YEARLY",
            f"SUMMARY:{title}",
            "BEGIN:VALARM",
            "ACTION:DISPLAY",
            f"DESCRIPTION:{title}",
            "TRIGGER:-PT15H",
            "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    return "\r\n".join(lines) + "\r\n"


def emergency_card_html(title, rows, footer):
    """A large-print page to print or keep on the phone; rows are (label, value)."""
    body = "".join(
        f"<tr><th>{escape(label)}</th><td>{escape(value).replace(chr(10), '<br>')}</td></tr>" for label, value in rows if value
    )
    return (
        "<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
        f"<title>{escape(title)}</title><style>"
        "body{font-family:'Noto Sans Telugu',Arial,sans-serif;font-size:22px;margin:16px;color:#111}"
        "h1{font-size:30px;border-bottom:4px solid #c62828;padding-bottom:6px}"
        "table{border-collapse:collapse;width:100%}th,td{border:2px solid #444;padding:10px;text-align:left;vertical-align:top}"
        "th{width:35%;background:#f3f3f3}p{font-size:18px}"
        f"</style></head><body><h1>🆘 {escape(title)}</h1><table>{body}</table><p>{escape(footer)}</p></body></html>"
    )


def heat_level(feels_like_c):
    if feels_like_c >= 40:
        return "danger"
    if feels_like_c >= 35:
        return "caution"
    return "ok"


def aqi_level(us_aqi):
    if us_aqi <= 50:
        return "good"
    if us_aqi <= 100:
        return "moderate"
    if us_aqi <= 150:
        return "sensitive"
    return "unhealthy"
