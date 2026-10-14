"""Optional AI helper: answers questions using the app's own tips. Needs ANTHROPIC_API_KEY in Streamlit secrets."""
import anthropic

MODEL = "claude-opus-5-5"

SYSTEM = (
    "You help senior citizens in Hyderabad, India. Answer in {language}, in short, simple sentences a 75-year-old can follow, "
    "at most 120 words. Prefer the app's tips below and mention the official website or helpline when one fits. "
    "For anything urgent, say to call 112 (emergency), 108 (ambulance) or 1930 (money lost to online fraud). "
    "Never ask for or accept OTPs, PINs, passwords or account numbers. For medicines or diagnoses, say to ask a doctor. "
    "If you are not sure, say so.\n\nApp tips:\n{tips}"
)


def ask(question, tips_text, language, api_key):
    client = anthropic.Anthropic(api_key=api_key, timeout=60)
    response = client.beta.messages.create(
        model=MODEL,
        max_tokens=2000,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM.format(language=language, tips=tips_text),
        messages=[{"role": "user", "content": question}],
    )
    if response.stop_reason == "refusal":
        return None
    return "".join(block.text for block in response.content if block.type == "text").strip() or None
