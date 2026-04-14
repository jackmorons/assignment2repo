"""
Streamlit Feedback Form Application
====================================
A styled feedback form with conditional messaging,
custom CSS theming, and input validation.
"""

import streamlit as st

# ── Page configuration ──────────────────────────────────────────────
st.set_page_config(
    page_title="Feedback Form",
    page_icon="📝",
    layout="centered",
)

# ── Custom CSS styling ──────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ─────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* ── Root variables ──────────────────────────────────── */
    :root {
        --primary: #6c63ff;
        --primary-light: #a29bfe;
        --accent: #00cec9;
        --bg-dark: #0f0f1a;
        --card-bg: rgba(255, 255, 255, 0.04);
        --card-border: rgba(255, 255, 255, 0.08);
        --text-primary: #f0f0f5;
        --text-muted: #8888a0;
        --success: #00b894;
        --warning: #fdcb6e;
        --danger: #e17055;
    }

    /* ── Hide Streamlit chrome ────────────────────────────── */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu, footer, .stDeployButton {
        display: none !important;
        visibility: hidden !important;
    }

    /* ── Global overrides ────────────────────────────────── */
    .stApp {
        background:
            radial-gradient(ellipse 80% 60% at 15% 20%,  rgba(108, 99, 255, 0.18) 0%, transparent 70%),
            radial-gradient(ellipse 70% 80% at 85% 75%,  rgba(0, 206, 201, 0.14) 0%, transparent 65%),
            radial-gradient(ellipse 90% 50% at 50% 50%,  rgba(162, 155, 254, 0.10) 0%, transparent 60%),
            radial-gradient(ellipse 60% 70% at 75% 15%,  rgba(253, 203, 110, 0.08) 0%, transparent 55%),
            radial-gradient(ellipse 50% 90% at 25% 85%,  rgba(0, 184, 148, 0.10) 0%, transparent 60%),
            #0f0f1a;
        font-family: 'Inter', sans-serif;
    }

    /* Title styling */
    h1 {
        background: linear-gradient(135deg, var(--primary-light), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
        letter-spacing: -0.5px;
    }

    h3 {
        color: var(--text-primary) !important;
        font-weight: 600 !important;
    }

    /* ── Card-like form container ────────────────────────── */
    [data-testid="stForm"] {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 16px;
        padding: 2rem 2rem 1.5rem;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
        transition: box-shadow 0.3s ease;
    }
    [data-testid="stForm"]:hover {
        box-shadow: 0 12px 48px rgba(108, 99, 255, 0.15);
    }

    /* ── Input fields ────────────────────────────────────── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', sans-serif !important;
        transition: border-color 0.25s ease, box-shadow 0.25s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 2px rgba(108, 99, 255, 0.25) !important;
    }

    /* Label styling */
    .stTextInput label, .stTextArea label, .stSlider label {
        color: var(--text-muted) !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.3px;
    }

    /* ── Slider ──────────────────────────────────────────── */
    .stSlider [data-testid="stThumbValue"] {
        color: var(--primary-light) !important;
        font-weight: 700 !important;
    }

    /* ── Submit button ───────────────────────────────────── */
    [data-testid="stForm"] button[kind="formSubmit"] {
        background: linear-gradient(135deg, var(--primary), #5a4fcf) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: 0.4px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stForm"] button[kind="formSubmit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(108, 99, 255, 0.4) !important;
    }
    [data-testid="stForm"] button[kind="formSubmit"]:active {
        transform: translateY(0);
    }

    /* ── Result card ─────────────────────────────────────── */
    .result-card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.8rem 2rem;
        margin-top: 1.2rem;
        backdrop-filter: blur(12px);
    }
    .result-card h4 {
        margin: 0 0 1rem;
        color: var(--accent);
        font-size: 1.1rem;
    }
    .result-card p {
        margin: 0.35rem 0;
        color: var(--text-primary);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .result-card .label {
        color: var(--text-muted);
        font-weight: 500;
    }

    /* ── Stars ───────────────────────────────────────────── */
    .stars {
        font-size: 1.4rem;
        letter-spacing: 2px;
    }

    /* ── Divider ─────────────────────────────────────────── */
    hr {
        border: none;
        border-top: 1px solid var(--card-border);
        margin: 1.5rem 0;
    }

    /* ── Alert boxes (custom) ────────────────────────────── */
    .alert-box {
        border-radius: 12px;
        padding: 1rem 1.4rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    .alert-warning {
        background: rgba(253, 203, 110, 0.12);
        border: 1px solid rgba(253, 203, 110, 0.3);
        color: var(--warning);
    }
    .alert-success {
        background: rgba(0, 184, 148, 0.12);
        border: 1px solid rgba(0, 184, 148, 0.3);
        color: var(--success);
    }
    .alert-neutral {
        background: rgba(162, 155, 254, 0.10);
        border: 1px solid rgba(162, 155, 254, 0.25);
        color: var(--primary-light);
    }

    /* ── Footer / muted text ─────────────────────────────── */
    .footer {
        text-align: center;
        color: var(--text-muted);
        font-size: 0.78rem;
        margin-top: 3rem;
        opacity: 0.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ── Helper: render stars from rating ────────────────────────────────
def _stars(rating: int) -> str:
    """Return a string of filled and empty star emojis."""
    return "★" * rating + "☆" * (5 - rating)


# ── Header ──────────────────────────────────────────────────────────
st.markdown("# 📝 Feedback Form")
st.markdown(
    "<p style='margin-top:-0.8rem; font-size:0.95rem;'>"
    "We value your feedback — let us know how we're doing!</p>",
    unsafe_allow_html=True,
)

# ── Form ────────────────────────────────────────────────────────────
with st.form(key="feedback_form"):
    name = st.text_input(
        "Your name",
        placeholder="e.g. Jane Doe",
        max_chars=100,
    )

    rating = st.slider(
        "How satisfied are you?",
        min_value=1,
        max_value=5,
        value=3,
        help="1 = Very Unsatisfied · 5 = Very Satisfied",
    )

    comments = st.text_area(
        "Additional comments (optional)",
        placeholder="Tell us more about your experience…",
        max_chars=1000,
        height=120,
    )

    submitted = st.form_submit_button("Submit Feedback")

# ── Post-submission logic ───────────────────────────────────────────
if submitted:
    # ── Validation ──────────────────────────────────────────────────
    try:
        stripped_name = name.strip()

        if not stripped_name:
            st.error("⚠️ Please enter your name before submitting.")
            st.stop()

        if not stripped_name.replace(" ", "").isalpha():
            st.error("⚠️ Name should contain only letters and spaces.")
            st.stop()

        # Sanitise comments (strip leading/trailing whitespace)
        clean_comments = comments.strip() if comments else ""

        # ── Display submitted data ──────────────────────────────────
        st.markdown("### 🎉 Thank you for your feedback!")

        st.markdown(
            f"""
            <div class="result-card">
                <h4>Your Submission</h4>
                <p><span class="label">Name:</span> {stripped_name}</p>
                <p><span class="label">Rating:</span>
                   <span class="stars">{_stars(rating)}</span>
                   &nbsp;({rating}/5)
                </p>
                <p><span class="label">Comments:</span>
                   {clean_comments if clean_comments else '<em style="color:#8888a0;">No comments provided.</em>'}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Also display via st.write() as required by the assignment
        st.write("---")
        st.write(f"**Name:** {stripped_name}")
        st.write(f"**Rating:** {rating} / 5")
        st.write(f"**Comments:** {clean_comments if clean_comments else '—'}")

        # ── Conditional messages ────────────────────────────────────
        if rating <= 2:
            st.markdown(
                '<div class="alert-box alert-warning">'
                "⚠️ We're sorry to hear that. We'll work hard to improve your experience!"
                "</div>",
                unsafe_allow_html=True,
            )
            st.warning(
                "Your satisfaction score is low. "
                "We take this seriously and will follow up."
            )
        elif rating >= 4:
            st.markdown(
                '<div class="alert-box alert-success">'
                "🎉 Awesome! We're thrilled you had a great experience!"
                "</div>",
                unsafe_allow_html=True,
            )
            st.success("Thank you for the positive feedback! 🙌")
        else:
            # rating == 3  →  neutral acknowledgement
            st.markdown(
                '<div class="alert-box alert-neutral">'
                "💬 Thanks for sharing. We'd love to know how we can do even better."
                "</div>",
                unsafe_allow_html=True,
            )
            st.info("Your feedback has been recorded.")

    except Exception as exc:
        st.error(f"An unexpected error occurred: {exc}")

# ── Footer ──────────────────────────────────────────────────────────
st.markdown(
    '<p class="footer">Built with Streamlit · © 2026</p>',
    unsafe_allow_html=True,
)
