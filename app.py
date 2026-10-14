"""Hyderabad Seniors' Corner: one simple place for news, health, money and daily-life tips, in English or Telugu."""
from zoneinfo import ZoneInfo

import streamlit as st

import news
from calculations import fd_maturity, inr, interest_payout, life_certificate_window
from content import FEEDS, HELPLINES, SOURCES, TOPICS
from i18n import FEEDS_TE, HELPLINES_TE, LANGUAGES, TOPICS_TE, UI
from visuals import large_text, show

st.set_page_config(page_title="Hyderabad Seniors' Corner", page_icon="🌼", layout="wide")

# Section keys stay in English; only their labels are translated.
HOME = "🏠 Home"
EMERGENCY = "🚨 Emergency numbers"
TOOLS = "🧮 Simple money tools"
ABOUT = "📚 Sources and about"
TOPIC_NAMES = [f"{t['icon']} {t['title']}" for t in TOPICS]
SECTIONS = [HOME, EMERGENCY] + TOPIC_NAMES + [TOOLS, ABOUT]
NEWS_CHOICES = ["Hyderabad", "Telangana", "India", "For senior citizens"]
TOOL_KEYS = ["fd", "income", "life"]
TEXT_SIZES = {"Large": 19, "Extra large": 23}
IST = ZoneInfo("Asia/Kolkata")

st.session_state.setdefault("section", HOME)
st.session_state.setdefault("lang", "en")
lang = st.session_state.lang
ui = UI[lang]


def go_to(section):
    st.session_state.section = section


def set_lang(code):
    st.session_state.lang = code


def topic(index):
    """The topic in the chosen language; links and icons are shared."""
    base = TOPICS[index]
    return {**base, **TOPICS_TE[base["title"]]} if lang == "te" else base


def section_label(section):
    icon, name = section.split(" ", 1)
    if lang == "te":
        name = TOPICS_TE[name]["title"] if name in TOPICS_TE else ui[name]
    return f"{icon} {name}"


@st.cache_data(ttl=1800, show_spinner="…")
def headlines(url, limit):
    return news.fetch_headlines(url, limit)


with st.sidebar:
    st.title(ui["sidebar_title"])
    # Only the selected section runs on each rerun, so the page stays fast.
    st.radio(ui["choose_topic"], SECTIONS, key="section", format_func=section_label)
    text_size = st.radio(ui["text_size"], list(TEXT_SIZES), horizontal=True, format_func=ui["sizes"].get)
    st.markdown(ui["sidebar_emergency"])

large_text(TEXT_SIZES[text_size])
title_col, en_col, te_col = st.columns([6, 1, 1], vertical_alignment="center")
title_col.title(ui["title"])
for col, (label, code) in zip([en_col, te_col], LANGUAGES.items()):
    col.button(label, on_click=set_lang, args=(code,), type="primary" if lang == code else "secondary", use_container_width=True)
st.caption(ui["caption"])
section = st.session_state.section


def show_news(feed, limit=5):
    url = (FEEDS_TE if lang == "te" else FEEDS)[feed]
    try:
        stories = headlines(url, limit)
    except Exception:
        stories = None
    if not stories:
        st.warning(ui["news_error"])
        return
    for story in stories:
        with st.container(border=True):
            st.markdown(f"#### {story['title']}")
            if story["summary"]:
                st.write(story["summary"])
            when = story["date"].astimezone(IST).strftime(ui["date_format"]) if story["date"] else ""
            meta = " · ".join(x for x in [story["source"], when] if x)
            if story["link"]:
                meta += f" · [{ui['read_full']}]({story['link']})"
            st.caption(meta)


def render_home():
    st.header(ui["welcome"])
    st.write(ui["welcome_text"])
    cols = st.columns(2)
    for i, name in enumerate(TOPIC_NAMES):
        with cols[i % 2].container(border=True):
            st.markdown(f"### {section_label(name)}")
            st.write(topic(i)["takeaway"])
            st.button(ui["open"], key="open_" + name, on_click=go_to, args=(name,), use_container_width=True)
    st.error(ui["home_emergency"])
    st.button(ui["see_emergency"], on_click=go_to, args=(EMERGENCY,), type="primary")


def render_emergency():
    st.header(ui["emergency_header"])
    st.write(ui["emergency_text"])
    names = HELPLINES_TE if lang == "te" else [name for name, _ in HELPLINES]
    for name, (_, number) in zip(names, HELPLINES):
        with st.container(border=True):
            left, right = st.columns([3, 1])
            left.markdown(f"### {name}")
            right.markdown(f"## [{number}](tel:{number})")
    st.info(ui["emergency_tip"])
    st.markdown(f"[{ui['elder_line_link']}]({SOURCES['Elder Line 14567']}) · [{ui['cyber_link']}]({SOURCES['Cyber crime portal']})")


def render_topic(index):
    t = topic(index)
    st.header(f"{t['icon']} {t['title']}")
    st.info(t["takeaway"])

    if index == 0:
        feed = st.segmented_control(ui["show_news_for"], NEWS_CHOICES, default=NEWS_CHOICES[0], format_func=ui["news_choices"].get)
        show_news(feed or NEWS_CHOICES[0], limit=8)
    elif t["feed"]:
        st.subheader(ui["latest_news"])
        show_news(t["feed"])

    st.subheader(ui["simple_tips"])
    for tip in t["tips"]:
        st.markdown(f"- {tip}")
    do_col, dont_col = st.columns(2)
    do_col.success(f"**{ui['do']}:** {t['do']}")
    dont_col.error(f"**{ui['dont']}:** {t['dont']}")

    st.subheader(ui["official_sites"])
    st.markdown(" · ".join(f"[{name} ↗]({SOURCES[name]})" for name in t["links"]))
    show(ui["cue_title"].format(title=t["title"]), t["cue"])

    prev_col, next_col = st.columns(2)
    if index > 0:
        prev_col.button(ui["prev_topic"], on_click=go_to, args=(TOPIC_NAMES[index - 1],), use_container_width=True)
    if index + 1 < len(TOPICS):
        next_col.button(ui["next_topic"], on_click=go_to, args=(TOPIC_NAMES[index + 1],), type="primary", use_container_width=True)
    else:
        next_col.button(ui["try_tools"], on_click=go_to, args=(TOOLS,), type="primary", use_container_width=True)


def render_tools():
    st.header(ui["tools_header"])
    st.caption(ui["tools_caption"])
    tool = st.segmented_control(ui["choose_tool"], TOOL_KEYS, default="fd", format_func=ui["tools"].get)
    if tool == "fd":
        amount = st.number_input(ui["deposit_amount"], min_value=0, value=500000, step=10000)
        rate = st.number_input(ui["rate"], min_value=0.0, max_value=15.0, value=7.5, step=0.25)
        years = st.slider(ui["years"], 1, 10, 5)
        final = fd_maturity(amount, rate, years)
        a, b = st.columns(2)
        a.metric(ui["get_back"], inr(final))
        b.metric(ui["interest_earned"], inr(final - amount))
        st.caption(ui["fd_caption"])
    elif tool == "income":
        amount = st.number_input(ui["deposit_amount"], min_value=0, value=1000000, step=10000)
        rate = st.number_input(ui["rate"], min_value=0.0, max_value=15.0, value=8.0, step=0.25)
        a, b = st.columns(2)
        a.metric(ui["every_month"], inr(interest_payout(amount, rate, 12)))
        b.metric(ui["every_quarter"], inr(interest_payout(amount, rate, 4)))
        st.caption(ui["income_caption"])
    elif tool == "life":
        age = st.number_input(ui["your_age"], min_value=55, max_value=110, value=72)
        window = life_certificate_window(age)
        st.metric(ui["submit_between"], ui.get("windows", {}).get(window, window))
        st.caption(ui["life_caption"])
        st.markdown(f"[{ui['jeevan_link']}]({SOURCES['Jeevan Pramaan (life certificate)']})")
    else:
        st.info(ui["pick_tool"])


def render_about():
    st.header(ui["about_header"])
    st.write(ui["about_text"])
    st.dataframe(
        [{ui["website"]: name, ui["link"]: url} for name, url in SOURCES.items()],
        hide_index=True,
        use_container_width=True,
        column_config={ui["link"]: st.column_config.LinkColumn(ui["link"])},
    )
    st.caption(ui["about_caption"])


if section == HOME:
    render_home()
elif section == EMERGENCY:
    render_emergency()
elif section in TOPIC_NAMES:
    render_topic(TOPIC_NAMES.index(section))
elif section == TOOLS:
    render_tools()
else:
    render_about()
