import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go

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


def _stars(rating: int) -> str:
    return "★" * rating + "☆" * (5 - rating)

tab1, tab2 = st.tabs(["Feedback Form", "Google Sheet Expander"])

with tab1:
    # ── Header ──────────────────────────────────────────────────────────
    st.markdown("# Feedback Form")
    st.markdown(
        "<p style='color:#8888a0; margin-top:-0.8rem; font-size:0.95rem;'>"
        "We value your feedback — let us know how we're doing!</p>",
        unsafe_allow_html=True,
    )

    # ── Form ────────────────────────────────────────────────────────────
    with st.form(key="feedback_form"):
        name = st.text_input(
            "Your name",
            placeholder="e.g. John Smith",
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

            st.write("---")
            st.write(f"**Name:** {stripped_name}")
            st.write(f"**Rating:** {rating} / 5")
            st.write(f"**Comments:** {clean_comments if clean_comments else '—'}")

            # ── Conditional messages ────────────────────────────────────
            if rating <= 2:
                st.markdown(
                    '<div class="alert-box alert-warning">'
                    "We're sorry to hear that. We'll work hard to improve your experience!"
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("---")
                st.warning(
                    "Your satisfaction score is low. "
                    "We are working on it."
                )
            elif rating >= 4:
                st.markdown(
                    '<div class="alert-box alert-success">'
                    "Awesome! We're thrilled you had a great experience!"
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("---")
                st.success("Thank you for the positive feedback! 🙌")
            else:
                # rating == 3  →  neutral acknowledgement
                st.markdown(
                    '<div class="alert-box alert-neutral">'
                    "Thanks for sharing. We'd love to know how we can do even better."
                    "</div>",
                    unsafe_allow_html=True,
                )
                st.markdown("---")
                st.info("Your feedback has been recorded.")

        except Exception as exc:
            st.error(f"An unexpected error occurred: {exc}")

    # ── Footer ──────────────────────────────────────────────────────────
    st.markdown(
        '<p class="footer">Built with Streamlit · © 2026</p>',
        unsafe_allow_html=True,
    )

with tab2:

    # import the sheet
    GOOGLE_SHEET_CSV_URL = (
        "https://docs.google.com/spreadsheets/d/"
        "1eWItYgh2UWjA94bXWqOpRkEUkh3gZVG80O00NeubMo0/export?format=csv"
    )

    @st.cache_data(ttl=300)
    def load_sheet_data(url: str) -> pd.DataFrame:
        # Sheet has no header row — each row is a progression of values
        df = pd.read_csv(url, header=None)
        return df

    raw_df = load_sheet_data(GOOGLE_SHEET_CSV_URL)

    # ── Melt: turn each cell into (column_position, value, row_label) ──
    # Columns become 1-indexed positions; each row is a separate series
    raw_df.columns = [i + 1 for i in range(len(raw_df.columns))]
    raw_df["Progression"] = [f"Row {i + 1}" for i in range(len(raw_df))]

    melted = raw_df.melt(
        id_vars="Progression",
        var_name="Step",
        value_name="Value",
    )

    # ── Build normalized data (each row ÷ its first-set value) ──────────
    norm_df = raw_df.copy()
    value_cols = [c for c in norm_df.columns if c != "Progression"]
    norm_df[value_cols] = norm_df[value_cols].astype(float)
    first_vals = norm_df[value_cols[0]].replace(0, np.nan)
    norm_df[value_cols] = norm_df[value_cols].div(first_vals, axis=0)

    melted_norm = norm_df.melt(
        id_vars="Progression",
        var_name="Step",
        value_name="Value",
    )

    exp = st.expander("📊 Show data", expanded=True)

    with exp:

        st.write("What am I looking at? 👇")
        st.write("We have asked a number of subjects to perform a benching test: 5 sets, 5 minutes rests, 80% of their 1RM, all to absolute failure.")
        st.write("The table below shows the number of repetitions performed in each set.")
        st.write("Each row corresponds to a subject and each column corresponds to a set.")
        st.write("The idea is capturing the mathematical trend of fatigue, to understand how fixed RPE sets could be developed educing reps over series to maintain fatigue.")

        col_norm, col_raw = st.columns(2)

        # ── Helper: build all three charts for a given melted df ──────
        def _render_charts(
            container,
            m_df,
            r_df,
            y_label,
            scatter_title,
            reg_title,
            mean_title,
            table_key,
        ):
            """Render scatter → regression → mean-regression inside *container*."""
            with container:
                # 1) Scatter ──────────────────────────────────────────
                fig = px.scatter(
                    m_df,
                    x="Step",
                    y="Value",
                    color="Progression",
                    template="plotly_dark",
                    title=scatter_title,
                    opacity=0.85,
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Series"),
                    yaxis=dict(title=y_label),
                    legend=dict(font=dict(size=9)),
                )
                fig.update_traces(
                    marker=dict(size=8, line=dict(width=1, color="rgba(255,255,255,0.3)"))
                )
                st.plotly_chart(fig, use_container_width=True)

                # Raw data toggle
                if st.checkbox("Show raw data table", key=table_key):
                    st.dataframe(r_df.drop(columns="Progression"), use_container_width=True)

                # 2) Quadratic regression ─────────────────────────────
                fig_reg = go.Figure()
                colors = px.colors.qualitative.Plotly
                n_sets = len(r_df.columns) - 1
                x_smooth = np.linspace(1, n_sets, 100)

                for idx, row_label in enumerate(m_df["Progression"].unique()):
                    subset = m_df[m_df["Progression"] == row_label]
                    x_pts = subset["Step"].values.astype(float)
                    y_pts = subset["Value"].values.astype(float)

                    coeffs = np.polyfit(x_pts, y_pts, 2)
                    y_smooth = np.polyval(coeffs, x_smooth)
                    color = colors[idx % len(colors)]

                    fig_reg.add_trace(go.Scatter(
                        x=x_pts, y=y_pts, mode="markers",
                        marker=dict(size=7, color=color,
                                    line=dict(width=1, color="rgba(255,255,255,0.3)")),
                        name=row_label, legendgroup=row_label, showlegend=True,
                    ))
                    fig_reg.add_trace(go.Scatter(
                        x=x_smooth, y=y_smooth, mode="lines",
                        line=dict(color=color, width=2),
                        name=f"{row_label} fit", legendgroup=row_label, showlegend=False,
                    ))

                fig_reg.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title=reg_title, title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Set"),
                    yaxis=dict(title=y_label),
                    legend=dict(font=dict(size=9)),
                )
                st.plotly_chart(fig_reg, use_container_width=True)

                # 3) Mean regression ──────────────────────────────────
                mean_y = np.zeros(len(x_smooth))
                for row_label in m_df["Progression"].unique():
                    subset = m_df[m_df["Progression"] == row_label]
                    x_pts = subset["Step"].values.astype(float)
                    y_pts = subset["Value"].values.astype(float)
                    coeffs = np.polyfit(x_pts, y_pts, 2)
                    mean_y += np.polyval(coeffs, x_smooth)
                mean_y /= len(m_df["Progression"].unique())

                fig_mean = go.Figure()
                fig_mean.add_trace(go.Scatter(
                    x=m_df["Step"].astype(float), y=m_df["Value"].astype(float),
                    mode="markers",
                    marker=dict(size=5, color="rgba(150,150,255,0.7)",
                                line=dict(width=1, color="white")),
                    name="All subjects",
                ))
                fig_mean.add_trace(go.Scatter(
                    x=x_smooth, y=mean_y, mode="lines",
                    line=dict(color="white", width=3, dash="dash"),
                    name="Mean regression",
                ))
                fig_mean.update_layout(
                    template="plotly_dark",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(family="Inter, sans-serif"),
                    title=mean_title, title_font_size=16,
                    margin=dict(t=50, b=30),
                    xaxis=dict(dtick=1, title="Set"),
                    yaxis=dict(title=y_label),
                )
                st.plotly_chart(fig_mean, use_container_width=True)

        # ── Left column: Normalized ──────────────────────────────────
        with col_norm:
            st.markdown("#### Normalized (÷ first set)")
        _render_charts(
            col_norm, melted_norm, norm_df,
            y_label="Fraction of Set 1",
            scatter_title="Normalized — Value vs Step",
            reg_title="Normalized — Fatigue Curves",
            mean_title="Normalized — Mean Fatigue Curve",
            table_key="table_norm",
        )

        # ── Right column: Absolute (current) ─────────────────────────
        with col_raw:
            st.markdown("#### Absolute (raw reps)")
        _render_charts(
            col_raw, melted, raw_df,
            y_label="Repetitions",
            scatter_title="Absolute — Value vs Step",
            reg_title="Absolute — Fatigue Curves",
            mean_title="Absolute — Mean Fatigue Curve",
            table_key="table_raw",
        )

        st.write("The left column normalizes every subject's reps by their first-set count (so set 1 = 1.0), revealing the universal fatigue *shape*. The right column shows the original absolute rep counts.")
        st.write("From the mean curves we can derive a single fatigue-decay reference for fixed-RPE set programming.")

