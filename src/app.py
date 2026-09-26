"""Streamlit UI for Hinglish spelling normalization."""
from __future__ import annotations

import html

import streamlit as st

from normalize import ServerBusyError, normalize, normalize_audio


st.set_page_config(
    page_title="Boli — Hinglish Language Workbench",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
:root { --ink:#18252b; --muted:#6c7b7c; --paper:#f7f8f4; --line:#dfe6df; --teal:#146b68; --teal-dark:#0d4d4c; --teal-soft:#e5f1ed; --coral:#ef7058; --yellow:#f3c85b; }
.stApp { background:radial-gradient(circle at 89% 7%,rgba(243,200,91,.18) 0,rgba(243,200,91,0) 22rem),radial-gradient(circle at 3% 47%,rgba(20,107,104,.07) 0,rgba(20,107,104,0) 25rem),var(--paper); color:var(--ink); }
.stApp,.stApp p,.stApp label,.stApp button,.stApp input,.stApp textarea { font-family:'Manrope',sans-serif; }
.block-container { max-width:1180px; padding:2.4rem 2rem 4rem; }
#MainMenu,footer,header { visibility:hidden; }
.brand-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:3.2rem; }
.brand { display:flex; align-items:center; gap:.7rem; color:var(--ink); font-weight:800; letter-spacing:-.04em; font-size:1.2rem; }
.brand-mark { width:2.15rem; height:2.15rem; display:grid; place-items:center; border-radius:10px 10px 10px 3px; color:#fff; background:var(--teal); box-shadow:5px 5px 0 rgba(239,112,88,.75); font-size:1.1rem; }
.stage-note { color:var(--muted); font-size:.75rem; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.hero { max-width:790px; margin:0 auto 2.6rem; text-align:center; }
.eyebrow { color:var(--teal); font-size:.72rem; font-weight:800; letter-spacing:.16em; text-transform:uppercase; }
.hero h1 { margin:.55rem 0 .85rem; color:var(--ink); font-family:'Playfair Display',Georgia,serif; font-size:clamp(3rem,7vw,5.6rem); font-weight:700; letter-spacing:-.065em; line-height:.98; }
.hero h1 span { color:var(--coral); }
.hero-copy { max-width:580px; margin:0 auto; color:var(--muted); font-size:1.04rem; line-height:1.65; }
.pill-row { display:flex; gap:.55rem; justify-content:center; flex-wrap:wrap; margin-top:1.3rem; }
.pill { display:inline-flex; gap:.38rem; align-items:center; padding:.42rem .72rem; border:1px solid var(--line); border-radius:999px; background:rgba(255,255,255,.7); color:#526365; font-size:.74rem; font-weight:700; }
.pill-dot { width:.42rem; height:.42rem; border-radius:50%; background:var(--teal); }
.section-label { display:flex; align-items:center; gap:.7rem; margin:1.4rem 0 .75rem; color:var(--ink); font-size:.78rem; font-weight:800; letter-spacing:.1em; text-transform:uppercase; }
.section-label:after { content:''; height:1px; flex:1; background:var(--line); }
div[data-testid='stForm'],div[data-testid='stAudioInput'],.output-card,.info-card { border:1px solid var(--line); border-radius:18px; background:rgba(255,255,255,.9); box-shadow:0 14px 35px rgba(24,37,43,.055); }
div[data-testid='stForm'] { padding:1.2rem 1.25rem 1rem; }
textarea { border-radius:12px !important; border:1px solid #ccd9d3 !important; background:#fcfdfb !important; color:var(--ink) !important; font-size:1rem !important; line-height:1.65 !important; }
textarea:focus { border-color:var(--teal) !important; box-shadow:0 0 0 3px rgba(20,107,104,.12) !important; }
div[role='radiogroup'] { gap:.4rem; padding:.3rem; border:1px solid var(--line); border-radius:12px; background:#edf2ee; }
div[role='radiogroup'] label { border-radius:9px; padding:.55rem .9rem; color:var(--muted); font-weight:800; }
div[role='radiogroup'] label:has(input:checked) { background:#fff; color:var(--teal); box-shadow:0 2px 9px rgba(24,37,43,.08); }
.stButton>button,.stFormSubmitButton>button { border-radius:10px; border:0; padding:.68rem 1.1rem; background:var(--teal); color:#fff; font-weight:800; transition:transform .15s ease,box-shadow .15s ease; }
.stButton>button:hover,.stFormSubmitButton>button:hover { border-color:var(--teal); background:var(--teal-dark); box-shadow:0 5px 14px rgba(20,107,104,.2); transform:translateY(-1px); }
.example-label { margin:.75rem 0 .35rem; color:var(--muted); font-size:.74rem; font-weight:800; letter-spacing:.09em; text-transform:uppercase; }
.example-text { padding:.8rem 1rem; border-left:3px solid var(--yellow); border-radius:0 10px 10px 0; background:#fffaf0; color:#586465; font-family:'DM Mono',monospace; font-size:.78rem; line-height:1.55; }
.output-card { padding:1.15rem 1.25rem 1.3rem; }
.output-kicker { color:var(--teal); font-size:.72rem; font-weight:800; letter-spacing:.12em; text-transform:uppercase; }
.output-card h3 { margin:.35rem 0 .9rem; color:var(--ink); font-family:'Playfair Display',Georgia,serif; font-size:1.6rem; }
.output-card code { display:block; padding:.9rem 1rem; border-radius:10px; background:#f3f7f3; color:var(--ink); font-family:'DM Mono',monospace; font-size:.9rem; line-height:1.65; white-space:pre-wrap; }
.output-card.deva code { background:var(--teal); color:#f6fffc; font-family:'Noto Sans Devanagari',sans-serif; font-size:1.2rem; }
.empty-card { min-height:198px; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:1.3rem; border:1px dashed #c7d5cd; border-radius:18px; background:rgba(255,255,255,.38); text-align:center; }
.empty-icon { width:2.6rem; height:2.6rem; display:grid; place-items:center; margin-bottom:.65rem; border-radius:50%; background:var(--teal-soft); color:var(--teal); font-size:1.2rem; }
.empty-card strong { color:var(--ink); font-size:.95rem; }
.empty-card p { max-width:245px; margin:.35rem 0 0; color:var(--muted); font-size:.78rem; line-height:1.5; }
.footer { margin-top:3.5rem; padding-top:1rem; border-top:1px solid var(--line); color:#899595; font-size:.74rem; text-align:center; }
@media (max-width:700px) { .block-container { padding:1.4rem 1rem 3rem; } .brand-row { margin-bottom:2.2rem; } .stage-note { display:none; } .hero h1 { font-size:3.6rem; } }
</style>
""",
    unsafe_allow_html=True,
)

retry_requested = st.session_state.pop("retry_requested", False)


def request_retry() -> None:
    st.session_state.retry_requested = True


def render_empty_state() -> None:
    st.markdown(
        """
        <div class="empty-card"><div class="empty-icon">✦</div>
        <strong>Your polished phrase will appear here</strong>
        <p>We’ll keep your meaning, smooth out the spelling, and add a Devanagari reading.</p></div>
        """,
        unsafe_allow_html=True,
    )


def render_output(original: str | None, result: dict) -> None:
    cleaned = html.escape(result["cleaned"])
    devanagari = html.escape(result["devanagari"])
    st.markdown('<div class="section-label">Your translation</div>', unsafe_allow_html=True)
    if original:
        source_col, clean_col = st.columns(2, gap="medium")
        with source_col:
            st.markdown(f'<div class="output-card"><div class="output-kicker">You wrote</div><h3>Original</h3><code>{html.escape(original)}</code></div>', unsafe_allow_html=True)
        with clean_col:
            st.markdown(f'<div class="output-card"><div class="output-kicker">Standardized Roman</div><h3>Cleaned up</h3><code>{cleaned}</code></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="output-card"><div class="output-kicker">Standardized Roman</div><h3>Cleaned up</h3><code>{cleaned}</code></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-card deva" style="margin-top:1rem"><div class="output-kicker" style="color:#b9e4d5">Native script</div><h3 style="color:#fff">Devanagari</h3><code>{devanagari}</code></div>', unsafe_allow_html=True)


def run_and_show(fn, *args) -> None:
    """Call a normalize function, showing retry notices and errors, then render the result."""
    retry_notice = st.empty()

    def show_retry(attempt: int, delay: int, backup: bool) -> None:
        key = "backup key" if backup else "server"
        retry_notice.info(f"{key.capitalize()} busy, retrying in {delay}s… (retry {attempt})")

    def show_fallback() -> None:
        retry_notice.warning("Primary key is busy. Switching to the backup key…")

    with st.spinner("Giving your words a little polish…"):
        try:
            result = fn(*args, on_retry=show_retry, on_fallback=show_fallback)
        except ServerBusyError as e:
            retry_notice.empty()
            st.error(str(e))
            st.button("Try again", on_click=request_retry)
        except Exception as e:
            retry_notice.empty()
            st.error(f"Something went wrong: {e}")
        else:
            retry_notice.empty()
            original = args[0] if args and isinstance(args[0], str) else None
            render_output(original, result)


st.markdown(
    """
    <div class="brand-row"><div class="brand"><div class="brand-mark">✦</div><span>boli</span></div>
    <div class="stage-note">A language workbench for everyday India</div></div>
    <div class="hero"><div class="eyebrow">From the way you say it · to the way you write it</div>
    <h1>Make your words<br><span>sound like you.</span></h1>
    <p class="hero-copy">Type or speak in natural Hinglish. Boli turns phonetic spelling into clear Roman text and beautiful Devanagari — without losing your voice.</p>
    <div class="pill-row"><div class="pill"><span class="pill-dot"></span> Hinglish aware</div><div class="pill"><span class="pill-dot"></span> Text + voice</div><div class="pill"><span class="pill-dot"></span> Meaning preserved</div></div></div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">Choose your input</div>', unsafe_allow_html=True)
mode = st.radio("Input method", ["Text", "Voice"], horizontal=True, label_visibility="collapsed")

if mode == "Text":
    left, right = st.columns([1.45, 1], gap="large")
    with left:
        with st.form("text_form", border=False):
            st.markdown('<div class="eyebrow" style="margin-bottom:.5rem">Write it as you would say it</div>', unsafe_allow_html=True)
            st.text_area("Hinglish input", key="text_input", label_visibility="collapsed", placeholder="bhai kal milte h, plz tym bta dena", height=155)
            submitted = st.form_submit_button("Normalize  →", type="primary", use_container_width=True)
    with right:
        st.markdown('<div class="example-label">Try this example</div>', unsafe_allow_html=True)
        st.markdown('<div class="example-text">kal raat ko bohot maza aya yaar</div>', unsafe_allow_html=True)
        st.markdown('<div class="example-label" style="margin-top:1.2rem">What you get</div>', unsafe_allow_html=True)
        st.markdown('<div class="example-text" style="border-left-color:#146b68">A natural Roman spelling + a Devanagari reading, side by side.</div>', unsafe_allow_html=True)
    if submitted or retry_requested:
        if not st.session_state.text_input.strip():
            st.warning("Write a phrase first — even a short one works beautifully.")
        else:
            run_and_show(normalize, st.session_state.text_input)
    else:
        st.markdown('<div class="section-label">Preview</div>', unsafe_allow_html=True)
        render_empty_state()
else:
    left, right = st.columns([1.45, 1], gap="large")
    with left:
        st.markdown('<div class="eyebrow" style="margin:1rem 0 .6rem">Speak naturally</div>', unsafe_allow_html=True)
        audio = st.audio_input("Record Hinglish speech", label_visibility="collapsed")
        if audio is None:
            st.caption("Tap the microphone, say a sentence, and Boli will listen for the words — not the spelling.")
    with right:
        st.markdown('<div class="example-label">Voice works best when</div>', unsafe_allow_html=True)
        st.markdown('<div class="example-text">You speak in a quiet place<br>You use your everyday Hinglish<br>You say one thought at a time</div>', unsafe_allow_html=True)
    if audio is not None:
        run_and_show(normalize_audio, audio.getvalue(), audio.type or "audio/wav")
    else:
        st.markdown('<div class="section-label">Preview</div>', unsafe_allow_html=True)
        render_empty_state()

st.markdown('<div class="footer">Built for the way India actually speaks · Boli Language Workbench</div>', unsafe_allow_html=True)
