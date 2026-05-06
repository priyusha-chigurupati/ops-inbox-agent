import streamlit as st

from src.ops_inbox.core.classifier import classify_messages
from src.ops_inbox.config import APP_NAME
from src.ops_inbox.data.inbox_repository import load_sample_messages


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
    messages = load_sample_messages()
    classified = classify_messages(messages)
    critical_count = sum(1 for _, result in classified if result.priority == "critical")
    high_count = sum(1 for _, result in classified if result.priority == "high")

    metric_cols = st.columns(4)
    metric_cols[0].metric("Inbox items", len(classified))
    metric_cols[1].metric("Critical", critical_count)
    metric_cols[2].metric("High priority", high_count)
    metric_cols[3].metric("Categories", len({result.category for _, result in classified}))

    st.subheader("Review Queue")
    st.caption("Sample messages are classified with deterministic rules so results are explainable and testable.")

    for message, result in classified:
        with st.container(border=True):
            cols = st.columns([2.3, 1, 1, 1])
            cols[0].markdown(f"**{message.subject}**")
            cols[0].caption(f"{message.sender_name} · {message.sender_company}")
            cols[1].badge(result.category.replace("_", " ").title(), color="blue")
            cols[2].badge(result.priority.title(), color=_priority_color(result.priority))
            cols[3].markdown(f"**{result.owner}**")
            st.write(message.preview)
            st.caption(
                f"Confidence: {int(result.confidence * 100)}% · Signals: "
                f"{', '.join(result.matched_terms) or 'fallback'}"
            )


def _priority_color(priority: str) -> str:
    return {
        "critical": "red",
        "high": "orange",
        "medium": "yellow",
        "low": "green",
    }.get(priority, "gray")


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
