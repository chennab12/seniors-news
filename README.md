# Hyderabad Seniors' Corner

A simple Streamlit app for senior citizens in Hyderabad: one place for the day's news and plain-language tips on the topics that matter most after 60. It follows the same layout as [finance-faqs](https://github.com/chennab12/finance-faqs): a sidebar menu, one page per topic, previous/next buttons and a small visual memory cue.

Helpful tools (all in English and Telugu):

- 🔊 **Read aloud** on every topic, the tip of the day and AI answers, using the phone's own voice.
- 🕵️ **Scam checker**: paste a message and get a red, amber or green warning with the reasons.
- 🪪 **My emergency card**: fill in medicines, blood group and family numbers, then download a large-print card. Nothing is stored.
- 🌤️ **Hyderabad weather, heat and air-quality advice** on Home (Open-Meteo, no key).
- 🏥 **Hospitals and medicines**: government hospitals with map links, and Jan Aushadhi generic medicine stores near you.
- 📅 **Important dates**: pension, tax and seasonal health reminders, with a calendar file that repeats every year.
- ✅ **Check-up schedule** by age, with ticks for what is done this year.
- 💡 **Tip of the day** with a WhatsApp share button.
- 🧾 **Bills and city services** topic: paying TGSPDCL, HMWSSB and GHMC bills safely.
- 💬 **Ask a question**: shows matching tips from the app; with an API key it also gives an AI answer.

Pages: Home, Emergency numbers, Today's news (Hyderabad, Telangana, India and senior-citizen headlines with short summaries), Health, Money, Safety and scams, Government benefits, Getting around Hyderabad, Phone and digital help, Active and happy living, Simple money tools (FD growth, monthly interest income, life certificate dates) and Sources. Text is large by default, with an extra-large option. **English** and **తెలుగు** buttons at the top switch every page, including the news feeds, to that language.

News comes from Google News RSS feeds, refreshed about every 30 minutes, using only the Python standard library. No API key is needed. Tips are general information, not medical, legal or financial advice; each topic links to the official Indian government or regulator website.

Telugu text lives in `i18n.py`, next to the English text in `content.py`. When you add or change a tip in one, change the other too; a test checks that both have the same topics and the same number of tips.

## Turning on AI answers (optional)

The Ask a question page works without a key by showing matching tips. To add AI answers, put an Anthropic API key in the app's secrets. On Streamlit Community Cloud: app ⋮ menu → Settings → Secrets, then add

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Each question costs roughly 2 US cents (under ₹2). Answers are short, in the reader's language, and based on the app's own tips.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the tests with `pip install pytest && python -m pytest -q`. GitHub Actions runs them on every push. Tests stub out news fetching so they work offline.

For Streamlit Community Cloud, deploy this repository with `app.py` as the entry point.
