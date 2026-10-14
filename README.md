# Hyderabad Seniors' Corner

A simple Streamlit app for senior citizens in Hyderabad: one place for the day's news and plain-language tips on the topics that matter most after 60. It follows the same layout as [finance-faqs](https://github.com/chennab12/finance-faqs): a sidebar menu, one page per topic, previous/next buttons and a small visual memory cue.

Pages: Home, Emergency numbers, Today's news (Hyderabad, Telangana, India and senior-citizen headlines with short summaries), Health, Money, Safety and scams, Government benefits, Getting around Hyderabad, Phone and digital help, Active and happy living, Simple money tools (FD growth, monthly interest income, life certificate dates) and Sources. Text is large by default, with an extra-large option.

News comes from Google News RSS feeds, refreshed about every 30 minutes, using only the Python standard library. No API key is needed. Tips are general information, not medical, legal or financial advice; each topic links to the official Indian government or regulator website.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Run the tests with `pip install pytest && python -m pytest -q`. GitHub Actions runs them on every push. Tests stub out news fetching so they work offline.

For Streamlit Community Cloud, deploy this repository with `app.py` as the entry point.
