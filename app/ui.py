import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)

import streamlit as st

from app.data_loader import DataLoader
from app.pipeline import RecommendationPipeline


# ======================================
# PAGE CONFIG
# ======================================
st.set_page_config(
    page_title="AI Shopping Assistant",
    layout="wide"
)


# ======================================
# STYLING
# ======================================
st.markdown("""
<style>

/* =========================
GLOBAL
========================= */

.main {
    background-color: #fffafb;
}

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

/* =========================
HEADINGS
========================= */

h1 {
    color: #22223b;
    font-size: 3.2rem !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #22223b;
}

/* =========================
SUBTITLE
========================= */

.subtitle {
    color: #6c757d;
    margin-top: -10px;
    margin-bottom: 30px;
    font-size: 17px;
}

/* =========================
INPUT AREA
========================= */

.stTextInput input {
    border-radius: 12px;
    border: 1px solid #ffc2d1;
    padding: 14px;
    font-size: 16px;
    background: white;
}

.stSelectbox div[data-baseweb="select"] {
    border-radius: 12px;
}

/* =========================
BUTTON
========================= */

.stButton button {
    width: 100%;
    background: #ff4d8d;
    color: white;
    border: none;
    border-radius: 12px;
    height: 48px;
    font-size: 16px;
    font-weight: 600;
}

.stButton button:hover {
    background: #e63e7b;
}

/* =========================
RESULT CARDS
========================= */

.result-card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #ffe0ea;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}

/* =========================
PRICE
========================= */

.price {
    color: #ff4d8d;
    font-size: 1.2rem;
    font-weight: 700;
}

/* =========================
PROGRESS BAR
========================= */

.stProgress > div > div > div > div {
    background-color: #ff4d8d;
}

</style>
""", unsafe_allow_html=True)


# ======================================
# LOAD PIPELINE
# ======================================
@st.cache_resource
def load_pipeline():

    loader = DataLoader()

    products = loader.load()

    return RecommendationPipeline(products)


pipeline = load_pipeline()


# ======================================
# HEADER
# ======================================
st.title("AI Shopping Assistant")

st.markdown(
    """
<div class="subtitle">
AI-powered parenting product recommendations using semantic search and intelligent ranking
</div>
""",
    unsafe_allow_html=True
)


# ======================================
# LAYOUT
# ======================================
left_col, right_col = st.columns([1, 1.3])


# ======================================
# INPUT SECTION
# ======================================
with left_col:

    st.header("Input")

    query = st.text_input(
        "Search Product",
        placeholder="e.g. bottle warmer, stroller, diaper bag"
    )

    age = st.slider(
        "Child Age",
        0,
        5,
        2
    )

    budget = st.slider(
        "Budget",
        100,
        10000,
        2500,
        step=100
    )

    category = st.selectbox(
        "Category",
        [
            None,
            "toys",
            "feeding",
            "travel",
            "care",
            "stroller"
        ]
    )

    recommend_clicked = st.button(
        "Recommend Products"
    )


# ======================================
# RESULTS
# ======================================
with right_col:

    st.header("Results")

    if recommend_clicked:

        with st.spinner(
            "Generating recommendations..."
        ):

            result = pipeline.run(
                query=query,
                age=age,
                budget=budget,
                category=category
            )

        # ==========================
        # ERRORS
        # ==========================
        if "error" in result:

            st.error(result["error"])

        elif "message" in result:

            st.warning(result["message"])

        else:

            primary = result[
                "primary_recommendation"
            ]

            # ======================
            # PRIMARY
            # ======================
            st.markdown(f"""
<div class="result-card">

<h2>{primary['name']}</h2>

<div class="price">
₹{primary['price']}
</div>

<br>

<b>Why this product?</b>

<p>{primary['reason']}</p>

</div>
""", unsafe_allow_html=True)

            # ======================
            # ALTERNATIVES
            # ======================
            st.subheader(
                "Alternative Recommendations"
            )

            for alt in result.get(
                "alternatives",
                []
            ):

                st.markdown(f"""
<div class="result-card">

<h4>{alt['name']}</h4>

<div class="price">
₹{alt['price']}
</div>

<br>

<p>{alt['reason']}</p>

</div>
""", unsafe_allow_html=True)

            # ======================
            # CONFIDENCE
            # ======================
            confidence = float(
                result.get(
                    "confidence",
                    0
                )
            )

            st.subheader(
                "Recommendation Confidence"
            )

            st.progress(confidence)

            st.write(
                f"{confidence:.2f}"
            )