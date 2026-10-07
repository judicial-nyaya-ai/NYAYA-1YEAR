
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NYAYA-1YEAR",
    layout="wide"
)

st.title("NYAYA-1YEAR")
st.subheader("AI Judicial Pendency Reduction Engine")

st.info(
    "AI decision-support system. "
    "It does not predict judgments or replace judicial decision-making."
)

# Load data
data = pd.read_csv("nyaya_1year_cases.csv")

# Dashboard metrics
total_cases = len(data)

high_priority = (
    data["disposal_readiness_score"] >= 75
).sum()

disposal_ready = (
    data["disposal_ready"] == 1
).sum()

adr_candidates = (
    data["adr_possible"] == 1
).sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Pending Cases", total_cases)
col2.metric("High Priority", high_priority)
col3.metric("Potentially Disposal Ready", disposal_ready)
col4.metric("ADR Candidates", adr_candidates)

st.divider()

st.header("Priority Cases")

top_cases = data.sort_values(
    "disposal_readiness_score",
    ascending=False
).head(20)

st.dataframe(
    top_cases[
        [
            "case_id",
            "case_age_years",
            "disposal_readiness_score",
            "priority_explanation",
            "recommended_action"
        ]
    ],
    use_container_width=True
)

st.divider()

st.header("Case Search")

case_id = st.text_input(
    "Enter Case ID",
    placeholder="Example: NY10000"
)

if case_id:

    result = data[
        data["case_id"].astype(str).str.upper()
        == case_id.upper()
    ]

    if len(result) == 0:
        st.warning("Case not found.")

    else:
        case = result.iloc[0]

        st.success(
            f"Priority Score: "
            f"{case['disposal_readiness_score']}/100"
        )

        st.write(
            "**Case age:**",
            case["case_age_years"],
            "years"
        )

        st.write(
            "**Why this score:**",
            case["priority_explanation"]
        )

        st.write(
            "**Recommended next action:**",
            case["recommended_action"]
        )

        st.warning(
            "Human judicial/registry review required."
        )

st.divider()

st.header("365-Day Strategy")

st.write(
    "NYAYA-1YEAR combines ML-based prioritisation "
    "with available judicial capacity to support "
    "a measurable one-year pendency-reduction strategy."
)

st.caption(
    "Prototype uses synthetic case data. "
    "Real deployment requires validated court data, "
    "security controls, legal governance and human oversight."
)
