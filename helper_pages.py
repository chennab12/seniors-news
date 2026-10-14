"""The helper pages and Home cards: weather, tip of the day, scam checker, emergency card,
hospitals, important dates, check-ups and questions. Each takes the language's UI strings."""
import os
from datetime import date
from urllib.parse import quote

import streamlit as st

import assistant
import weather
from content import SOURCES
from extras_content import BLOOD_GROUPS, CHECKUPS, HOSPITALS, JAN_AUSHADHI, NEAR_ME, maps_link
from i18n import UI
from features import aqi_level, build_ics, emergency_card_html, heat_level, scam_check, search_tips, tip_of_the_day, upcoming_dates
from visuals import read_aloud


@st.cache_data(ttl=3600, show_spinner=False)
def _weather():
    return weather.fetch_weather()


def weather_card(ui):
    with st.container(border=True):
        st.markdown(f"### {ui['weather_title']}")
        try:
            w = _weather()
        except Exception:
            st.caption(ui["weather_error"])
            return
        cols = st.columns(4)
        cols[0].metric(ui["temp"], f"{w['temp']:.0f}°C")
        cols[1].metric(ui["feels"], f"{w['feels_like']:.0f}°C")
        cols[2].metric(ui["high_low"], f"{w['max']:.0f}° / {w['min']:.0f}°")
        if w["aqi"] is not None:
            cols[3].metric(ui["aqi"], ui["aqi_levels"][aqi_level(w["aqi"])], help=f"US AQI {w['aqi']:.0f}")
        else:
            cols[3].metric(ui["rain"], f"{w['rain_chance']:.0f}%")
        heat = heat_level(w["feels_like"])
        (st.error if heat == "danger" else st.warning if heat == "caution" else st.success)(ui["heat"][heat])
        if w["aqi"] is not None and aqi_level(w["aqi"]) in ("sensitive", "unhealthy"):
            st.warning(ui["aqi_advice"])
        if w["rain_chance"] >= 50:
            st.info(ui["rain_advice"])
        st.caption(ui["weather_source"])


def tip_card(ui, lang, topics, icons):
    topic, tip = tip_of_the_day(topics, date.today())
    icon = icons[topic["_key"]][topic["tips"].index(tip)]
    with st.container(border=True):
        st.markdown(f"### {ui['tip_title']}")
        st.markdown(f"#### {icon} {tip}")
        st.caption(f"{topic['icon']} {topic['title']}")
        read_aloud(tip, lang, (ui["read_aloud"], ui["stop"]))
        share = f"{icon} {tip}\n\n— {ui['title']}"
        st.link_button(ui["share_whatsapp"], "https://wa.me/?text=" + quote(share), use_container_width=True)


def render_scam(ui, lang):
    st.header(ui["scam_header"])
    st.write(ui["scam_intro"])
    examples = ui["scam_example_texts"]
    with st.expander(ui["scam_examples"]):
        for i, text in enumerate(examples):
            if st.button(f"📩 {text[:60]}…", key=f"scam_example_{i}", use_container_width=True):
                st.session_state.scam_text = text
    message = st.text_area(ui["scam_input"], key="scam_text", height=150)
    if st.button(ui["scam_check"], type="primary", use_container_width=True) or message:
        if not message.strip():
            st.info(ui["scam_empty"])
            return
        level, reasons = scam_check(message)
        {"red": st.error, "amber": st.warning, "green": st.success}[level](ui["scam_result"][level])
        if reasons:
            st.markdown(f"**{ui['scam_reasons']}**")
            for en, te in reasons:
                st.markdown(f"- {te if lang == 'te' else en}")
        st.info(ui["scam_lost"])
    st.markdown(f"[🌐 cybercrime.gov.in ↗]({SOURCES['Cyber crime portal']}) · [📞 1930](tel:1930)")


def render_card(ui, lang):
    st.header(ui["card_header"])
    st.write(ui["card_intro"])
    f = ui["card_fields"]
    values = {}
    left, right = st.columns(2)
    values["name"] = left.text_input(f["name"])
    values["age"] = right.text_input(f["age"])
    values["blood"] = left.selectbox(f["blood"], BLOOD_GROUPS, format_func=lambda g: g or "—")
    values["address"] = right.text_input(f["address"])
    values["conditions"] = st.text_input(f["conditions"])
    values["medicines"] = st.text_area(f["medicines"], height=100)
    values["allergies"] = st.text_input(f["allergies"])
    values["doctor"] = st.text_input(f["doctor"])
    left, right = st.columns(2)
    values["contact1"] = left.text_input(f["contact1"])
    values["contact2"] = right.text_input(f["contact2"])
    if not values["name"].strip():
        st.info(ui["card_empty"])
        return
    rows = [(f[key], value.strip()) for key, value in values.items()]
    html = emergency_card_html(ui["card_title"], rows, ui["card_footer"])
    st.download_button(ui["card_download"], html, file_name="emergency-card.html", mime="text/html", type="primary", use_container_width=True)
    st.caption(ui["card_tip"])
    with st.expander(ui["card_preview"], expanded=True):
        st.html(html.split("<body>", 1)[1].split("</body>", 1)[0].replace("<h1>", "<h3>").replace("</h1>", "</h3>"))


def render_hospitals(ui, lang):
    te = lang == "te"
    st.header(ui["hosp_header"])
    st.error(ui["ambulance_note"])
    st.subheader(ui["near_me"])
    cols = st.columns(len(NEAR_ME))
    for col, (icon, en, te_name, query) in zip(cols, NEAR_ME):
        col.link_button(f"{icon} {te_name if te else en}", maps_link(query), use_container_width=True)
    st.caption(ui["map_note"])
    st.subheader(ui["gov_hospitals"])
    for icon, en, te_name, what, te_what, query in HOSPITALS:
        with st.container(border=True):
            left, right = st.columns([3, 1], vertical_alignment="center")
            left.markdown(f"**{icon} {te_name if te else en}**  \n{te_what if te else what}")
            right.link_button(ui["open_map"], maps_link(query), use_container_width=True)
    st.subheader(ui["jan_header"])
    for line in JAN_AUSHADHI[lang]:
        st.markdown(f"- {line}")
    st.markdown(f"[🌐 Jan Aushadhi ↗]({SOURCES['Jan Aushadhi (cheaper medicines)']})")


def render_dates(ui, lang):
    te = lang == "te"
    st.header(ui["dates_header"])
    st.write(ui["dates_intro"])
    birthday = st.date_input(ui["birthday"], value=None, min_value=date(1920, 1, 1), max_value=date.today(), format="DD/MM/YYYY")
    extra = []
    if birthday and (birthday.month, birthday.day) != (2, 29):
        extra.append((birthday.month, birthday.day, "🎂", UI["en"]["birthday_event"], UI["te"]["birthday_event"]))
    today = date.today()
    items = upcoming_dates(today, extra)
    for when, icon, en, te_text in items:
        days = (when - today).days
        left_text = ui["today"] if days == 0 else ui["days_left"].format(n=days)
        with st.container(border=True):
            left, right = st.columns([3, 1], vertical_alignment="center")
            left.markdown(f"**{icon} {te_text if te else en}**")
            right.markdown(f"**{when:%d-%m-%Y}**  \n⏳ {left_text}")
    ics = build_ics([(when, f"{icon} {te_text if te else en}") for when, icon, en, te_text in items])
    st.download_button(ui["add_calendar"], ics, file_name="seniors-reminders.ics", mime="text/calendar", type="primary", use_container_width=True)
    st.caption(ui["calendar_note"])


def render_checkups(ui, lang):
    te = lang == "te"
    st.header(ui["check_header"])
    st.write(ui["check_intro"])
    done = 0
    for i, (icon, test, te_test, often, te_often) in enumerate(CHECKUPS):
        with st.container(border=True):
            left, right = st.columns([3, 1], vertical_alignment="center")
            left.markdown(f"**{icon} {te_test if te else test}**  \n🔁 {ui['how_often']}: {te_often if te else often}")
            done += right.checkbox(ui["done"], key=f"checkup_{i}")
    st.progress(done / len(CHECKUPS), text=ui["check_progress"].format(done=done, total=len(CHECKUPS)))


def _api_key():
    try:
        return st.secrets.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")
    except Exception:  # no secrets file
        return os.environ.get("ANTHROPIC_API_KEY")


def render_ask(ui, lang, topics, icons):
    st.header(ui["ask_header"])
    st.write(ui["ask_intro"])
    with st.form("ask"):
        question = st.text_input(ui["ask_input"])
        asked = st.form_submit_button(ui["ask_button"], type="primary", use_container_width=True)
    if not (asked and question.strip()):
        return
    key = _api_key()
    if key:
        tips_text = "\n".join(f"- [{t['title']}] {tip}" for t in topics for tip in t["tips"])
        with st.spinner("🤖 …"):
            try:
                answer = assistant.ask(question, tips_text, ui["language_name"], key)
            except Exception:
                answer = None
        if answer:
            with st.container(border=True):
                st.markdown(f"### {ui['ask_ai']}")
                st.write(answer)
                read_aloud(answer, lang, (ui["read_aloud"], ui["stop"]))
            st.caption(ui["ask_disclaimer"])
        else:
            st.info(ui["ask_error"])
    else:
        st.info(ui["ask_no_ai"])
    matches = search_tips(question, topics)
    st.subheader(ui["ask_related"])
    if not matches:
        st.write(ui["ask_none"])
    for topic, tip in matches:
        icon = icons[topic["_key"]][topic["tips"].index(tip)]
        st.markdown(f"- {icon} {tip}  \n  _{topic['icon']} {topic['title']}_")
