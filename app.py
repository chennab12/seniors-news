"""Hyderabad Seniors' Corner: one simple place for news, health, money and daily-life tips."""
from zoneinfo import ZoneInfo

import streamlit as st

import news
from calculations import fd_maturity, inr, interest_payout, life_certificate_window
from content import FEEDS, HELPLINES, SOURCES, TOPICS
from visuals import large_text, show

st.set_page_config(page_title="Hyderabad Seniors' Corner", page_icon="🌼", layout="wide")

HOME = "🏠 Home"
EMERGENCY = "🚨 Emergency numbers"
TOOLS = "🧮 Simple money tools"
ABOUT = "📚 Sources and about"
TOPIC_NAMES = [f"{t['icon']} {t['title']}" for t in TOPICS]
SECTIONS = [HOME, EMERGENCY] + TOPIC_NAMES + [TOOLS, ABOUT]
NEWS_CHOICES = ["Hyderabad", "Telangana", "India", "For senior citizens"]
TEXT_SIZES = {"Large": 19, "Extra large": 23}
IST = ZoneInfo("Asia/Kolkata")

st.session_state.setdefault("section", HOME)


def go_to(section):
    st.session_state.section = section


@st.cache_data(ttl=1800, show_spinner="Getting the latest news…")
def headlines(feed, limit):
    return news.fetch_headlines(FEEDS[feed], limit)


with st.sidebar:
    st.title("🌼 Seniors' Corner")
    # Only the selected section runs on each rerun, so the page stays fast.
    st.radio("Choose a topic", SECTIONS, key="section")
    text_size = st.radio("Text size", list(TEXT_SIZES), horizontal=True)
    st.markdown("**Emergency: 112** · Ambulance: 108 · Cyber fraud: 1930 · Elder Line: 14567")

large_text(TEXT_SIZES[text_size])
st.title("🌼 Hyderabad Seniors' Corner")
st.caption("News, health, money and everyday help for senior citizens in Hyderabad, in simple words.")
section = st.session_state.section


def show_news(feed, limit=5):
    try:
        stories = headlines(feed, limit)
    except Exception:
        stories = None
    if not stories:
        st.warning("News could not be loaded right now. Please try again in a few minutes.")
        return
    for story in stories:
        with st.container(border=True):
            st.markdown(f"#### {story['title']}")
            if story["summary"]:
                st.write(story["summary"])
            when = story["date"].astimezone(IST).strftime("%d %b, %I:%M %p") if story["date"] else ""
            meta = " · ".join(x for x in [story["source"], when] if x)
            if story["link"]:
                meta += f" · [Read full story ↗]({story['link']})"
            st.caption(meta)


def render_home():
    st.header("🏠 Welcome")
    st.write("Pick a topic below or from the menu on the left. Each topic has the latest news and a few simple tips.")
    cols = st.columns(2)
    for i, (name, topic) in enumerate(zip(TOPIC_NAMES, TOPICS)):
        with cols[i % 2].container(border=True):
            st.markdown(f"### {name}")
            st.write(topic["takeaway"])
            st.button("Open", key="open_" + name, on_click=go_to, args=(name,), use_container_width=True)
    st.error("**In an emergency call 112.** For an ambulance call 108. If you lose money to a fraud call, dial 1930 at once.")
    st.button("See all emergency numbers →", on_click=go_to, args=(EMERGENCY,), type="primary")


def render_emergency():
    st.header("🚨 Emergency and help numbers")
    st.write("These numbers are free and work from any phone in India. Save them in your phone and write them near your door.")
    for name, number in HELPLINES:
        with st.container(border=True):
            left, right = st.columns([3, 1])
            left.markdown(f"### {name}")
            right.markdown(f"## [{number}](tel:{number})")
    st.info("Tip: write your own family doctor's, neighbour's and nearest hospital's numbers on a card and keep it by the phone.")
    st.markdown(f"[Elder Line 14567 ↗]({SOURCES['Elder Line 14567']}) · [Report cyber fraud online ↗]({SOURCES['Cyber crime portal']})")


def render_topic(index):
    topic = TOPICS[index]
    st.header(f"{topic['icon']} {topic['title']}")
    st.info(topic["takeaway"])

    if index == 0:
        feed = st.segmented_control("Show news for", NEWS_CHOICES, default=NEWS_CHOICES[0]) or NEWS_CHOICES[0]
        show_news(feed, limit=8)
    elif topic["feed"]:
        st.subheader("🗞️ Latest news")
        show_news(topic["feed"])

    st.subheader("💡 Simple tips")
    for tip in topic["tips"]:
        st.markdown(f"- {tip}")
    do_col, dont_col = st.columns(2)
    do_col.success("**Do:** " + topic["do"])
    dont_col.error("**Don't:** " + topic["dont"])

    st.subheader("🔗 Official websites")
    st.markdown(" · ".join(f"[{name} ↗]({SOURCES[name]})" for name in topic["links"]))
    show(topic["title"], topic["cue"])

    prev_col, next_col = st.columns(2)
    if index > 0:
        prev_col.button("← Previous topic", on_click=go_to, args=(TOPIC_NAMES[index - 1],), use_container_width=True)
    if index + 1 < len(TOPICS):
        next_col.button("Next topic →", on_click=go_to, args=(TOPIC_NAMES[index + 1],), type="primary", use_container_width=True)
    else:
        next_col.button("Try the money tools →", on_click=go_to, args=(TOOLS,), type="primary", use_container_width=True)


def render_tools():
    st.header("🧮 Simple money tools")
    st.caption("Nothing you type here is saved. Do not enter account numbers or passwords. Results are estimates; ask your bank for exact figures.")
    tool = st.segmented_control(
        "Choose a tool", ["Fixed deposit growth", "Monthly interest income", "Life certificate dates"], default="Fixed deposit growth"
    )
    if tool == "Fixed deposit growth":
        amount = st.number_input("Amount you deposit (₹)", min_value=0, value=500000, step=10000)
        rate = st.number_input("Interest rate per year (%)", min_value=0.0, max_value=15.0, value=7.5, step=0.25)
        years = st.slider("Number of years", 1, 10, 5)
        final = fd_maturity(amount, rate, years)
        a, b = st.columns(2)
        a.metric("You get back", inr(final))
        b.metric("Interest earned", inr(final - amount))
        st.caption("Assumes interest is added every three months, as most Indian banks do. Tax on interest is not included.")
    elif tool == "Monthly interest income":
        amount = st.number_input("Amount you deposit (₹)", min_value=0, value=1000000, step=10000)
        rate = st.number_input("Interest rate per year (%)", min_value=0.0, max_value=15.0, value=8.0, step=0.25)
        a, b = st.columns(2)
        a.metric("Every month", inr(interest_payout(amount, rate, 12)))
        b.metric("Every three months (like SCSS)", inr(interest_payout(amount, rate, 4)))
        st.caption("Interest is paid out and not added back, so your deposit stays the same. Check current SCSS and senior FD rates with the post office or your bank.")
    elif tool == "Life certificate dates":
        age = st.number_input("Your age", min_value=55, max_value=110, value=72)
        st.metric("Submit your life certificate between", life_certificate_window(age))
        st.caption("For central government pensioners. Other pension providers may set different dates; check with your bank or pension office.")
        st.markdown(f"[Submit from home with Jeevan Pramaan ↗]({SOURCES['Jeevan Pramaan (life certificate)']})")
    else:
        st.info("Pick a tool above.")


def render_about():
    st.header("📚 Sources and about")
    st.write(
        "Headlines come from Google News and are updated about every 30 minutes. Each summary is the first lines of the story's description. "
        "Tips are general information for senior citizens in Hyderabad, not medical, legal or financial advice. Rules and rates change, "
        "so please check the official websites below or ask your doctor or bank."
    )
    st.dataframe(
        [{"Website": name, "Link": url} for name, url in SOURCES.items()],
        hide_index=True,
        use_container_width=True,
        column_config={"Link": st.column_config.LinkColumn("Link")},
    )
    st.caption("This app does not ask for personal details, save what you type, or connect to any bank account.")


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
