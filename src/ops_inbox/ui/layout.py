import streamlit as st

from src.ops_inbox.config import APP_NAME


def render_page_shell() -> None:
    st.set_page_config(page_title=APP_NAME, page_icon="📬", layout="wide")
    st.markdown(_styles(), unsafe_allow_html=True)
    st.markdown(
        """
        <section class="hero">
            <div>
                <span class="eyebrow">Operations automation</span>
                <h1>Ops Inbox Agent</h1>
                <p>
                    A review-first inbox workflow for classifying inbound messages,
                    detecting urgency, extracting details, and preparing next actions.
                </p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
    st.info("Project scaffold is ready. Feature implementation starts after approval.")


def _styles() -> str:
    return """
    <style>
    .block-container {
        padding-top: 2rem;
        max-width: 1180px;
    }
    .hero {
        border: 1px solid #d8dee4;
        border-radius: 10px;
        padding: 28px;
        background: #f6f8fa;
        margin-bottom: 18px;
    }
    .eyebrow {
        color: #0969da;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0;
        text-transform: uppercase;
    }
    .hero h1 {
        margin: 6px 0 8px;
        font-size: 2.4rem;
        line-height: 1.05;
    }
    .hero p {
        color: #57606a;
        font-size: 1.04rem;
        margin: 0;
        max-width: 760px;
    }
    </style>
    """
