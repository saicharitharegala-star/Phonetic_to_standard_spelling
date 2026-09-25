"""Streamlit UI for Hinglish spelling normalization."""

import streamlit as st

from normalize import ServerBusyError, normalize, normalize_audio

st.set_page_config(page_title="Hinglish Language Workbench", page_icon="📝")

st.markdown("### Hinglish Language Workbench")
st.caption("Type or speak messy Hinglish and get standardized Roman + Devanagari output.")

# Set by the "Try again" button (via on_click, so it survives the rerun that button triggers).
retry_requested = st.session_state.pop("retry_requested", False)


def request_retry() -> None:
    st.session_state.retry_requested = True


def run_and_show(fn, *args) -> None:
    """Call a normalize function, showing retry notices and errors, then render the result."""
    retry_notice = st.empty()

    def show_retry(attempt: int, delay: int, backup: bool) -> None:
        key = "backup key" if backup else "server"
        retry_notice.info(f"{key.capitalize()} busy, retrying in {delay}s... (retry {attempt})")

    def show_fallback() -> None:
        retry_notice.warning("Primary key still busy. Trying backup key...")

    with st.spinner("Normalizing..."):
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
            # Emphasize the primary input/output area: show original and cleaned text
            st.markdown("**Original input → Cleaned output**")

            cleaned = result["cleaned"]
            devanagari = result["devanagari"]

            # If original text was passed through args (text mode), show side-by-side
            original = None
            if args:
                # For normalize(text) the first arg is the text; for audio it's bytes
                if isinstance(args[0], str):
                    original = args[0]

            if original:
                cols = st.columns([1, 1])
                with cols[0]:
                    st.write("**Original**")
                    st.code(original)
                with cols[1]:
                    st.write("**Cleaned (Roman)**")
                    st.code(cleaned)
                st.write("**Devanagari (Hindi)**")
                st.code(devanagari)
            else:
                # Audio mode or no original string available — stack outputs with emphasis
                st.subheader("Cleaned (Roman)")
                st.code(cleaned)
                st.subheader("Devanagari (Hindi)")
                st.code(devanagari)


mode = st.radio("Input method", ["Text", "Voice"], horizontal=True)

if mode == "Text":
    # A form makes Ctrl+Enter (Cmd+Enter on Mac) in the text area submit, same as clicking Normalize.
    with st.form("text_form", border=False):
        st.write("\n")
        st.info("Example: bhai kal milte h, plz tym bta dena")
        text = st.text_area("Hinglish input", placeholder="bhai kal milte h, plz tym bta dena", height=160)
        submitted = st.form_submit_button("Normalize", type="primary")
    if submitted or retry_requested:
        if not text.strip():
            st.warning("Enter some text first.")
        else:
            run_and_show(normalize, text)
else:
    audio = st.audio_input("Record Hinglish speech")
    # Runs on every rerun while a recording exists, so "Try again" re-sends the same audio.
    if audio is not None:
        run_and_show(normalize_audio, audio.getvalue(), audio.type or "audio/wav")
