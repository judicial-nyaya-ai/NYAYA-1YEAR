import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="NYAYA-1YEAR",
    layout="wide"
)

st.title("NYAYA-1YEAR — AI Judicial Pendency Reduction Engine")
st.caption("AI-assisted judicial prioritisation and Environmental Justice monitoring")

st.warning(
    "Prototype only. This demonstration uses synthetic judicial and environmental "
    "data. It does not predict judgments and does not replace judicial or registry "
    "decision-making."
)

data = pd.read_csv("nyaya_1year_cases.csv")

st.header("⚖️ Judicial Pendency Dashboard")

total_cases = len(data)
priority_cases = int((data["disposal_readiness_score"] >= 75).sum())
disposal_ready = int((data["disposal_ready"] == 1).sum())
adr_cases = int((data["adr_possible"] == 1).sum())
average_age = round(data["case_age_years"].mean(), 2)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Pending Cases", total_cases)
c2.metric("Priority Cases", priority_cases)
c3.metric("Disposal Ready", disposal_ready)
c4.metric("ADR Candidates", adr_cases)
c5.metric("Average Age", f"{average_age} yrs")

st.header("🔎 Case Search")

case_id = st.text_input(
    "Enter Case ID",
    placeholder="Example: NY10665"
)

if case_id:
    result = data[
        data["case_id"].astype(str).str.upper()
        == case_id.strip().upper()
    ]

    if len(result) == 0:
        st.error("Case ID not found.")

    else:
        case = result.iloc[0]

        st.subheader(f"Case: {case['case_id']}")

        a, b, c = st.columns(3)

        a.metric(
            "Priority Score",
            f"{case['disposal_readiness_score']:.1f}/100"
        )

        b.metric(
            "Case Age",
            f"{case['case_age_years']:.1f} years"
        )

        c.metric(
            "Environmental Urgency",
            case.get("environmental_urgency", "N/A")
        )

        st.write(
            "**Why this score:**",
            case.get(
                "priority_explanation",
                "No explanation available."
            )
        )

        st.write(
            "**Recommended next action:**",
            "Consider listing for final hearing/disposal"
            if case["disposal_readiness_score"] >= 75
            else "Review procedural bottlenecks before listing."
        )

        st.info("Human judicial/registry review required.")

st.header("📌 Highest Priority Cases")

priority_table = data.sort_values(
    "disposal_readiness_score",
    ascending=False
).head(20)

st.dataframe(
    priority_table[
        [
            "case_id",
            "case_age_years",
            "disposal_readiness_score",
            "environmental_urgency",
            "adr_possible"
        ]
    ],
    use_container_width=True
)

st.header("🌊 Environmental Justice & Pollution Monitoring")

st.warning(
    "Environmental values below are synthetic demonstration indicators. "
    "They are NOT actual measurements from any river, pond, sea, applicant "
    "address, or defendant address."
)

avg_applicant_pollution = round(
    data["applicant_water_pollution_pct"].mean(), 1
)

avg_defendant_pollution = round(
    data["defendant_water_pollution_pct"].mean(), 1
)

avg_environmental_urgency = round(
    data["environmental_urgency_score"].mean(), 1
)

e1, e2, e3 = st.columns(3)

e1.metric(
    "Applicant-side Water Pollution",
    f"{avg_applicant_pollution}%"
)

e2.metric(
    "Defendant-side Water Pollution",
    f"{avg_defendant_pollution}%"
)

e3.metric(
    "Environmental Urgency",
    f"{avg_environmental_urgency}/100"
)

st.subheader("🧪 Water Quality Indicators")

water_quality = pd.DataFrame({
    "Parameter": [
        "Dissolved Oxygen (mg/L)",
        "BOD (mg/L)",
        "Turbidity (NTU)",
        "pH",
        "Fecal Indicator"
    ],
    "Applicant-side Average": [
        round(data["applicant_DO_mg_L"].mean(), 2),
        round(data["applicant_BOD_mg_L"].mean(), 2),
        round(data["applicant_turbidity_NTU"].mean(), 2),
        round(data["applicant_pH"].mean(), 2),
        round(data["applicant_fecal_indicator"].mean(), 2)
    ],
    "Defendant-side Average": [
        round(data["defendant_DO_mg_L"].mean(), 2),
        round(data["defendant_BOD_mg_L"].mean(), 2),
        round(data["defendant_turbidity_NTU"].mean(), 2),
        round(data["defendant_pH"].mean(), 2),
        round(data["defendant_fecal_indicator"].mean(), 2)
    ]
})

st.dataframe(
    water_quality,
    use_container_width=True
)

st.subheader("📈 Pollution Trend")

st.bar_chart(
    data["pollution_trend"].value_counts()
)

st.subheader("🏛️ Municipal Remediation Status")

st.bar_chart(
    data["municipal_remediation_status"].value_counts()
)

st.subheader("🔬 Scientific Pollution-Reduction Measures")

measures = data[
    "scientific_remediation_measures"
].dropna().unique()

for measure in measures:
    st.write("•", measure)

st.subheader("⚠️ Environmental Exposure-Risk Indicator")

st.bar_chart(
    data["exposure_risk_indicator"].value_counts()
)

st.caption(
    "Exposure-risk indicators are environmental screening indicators only "
    "and are not medical diagnoses."
)

st.subheader("⚖️ Pollution ↔ Judicial Delay Indicator")

correlation = data[
    ["current_pollution_pct", "judicial_delay_indicator"]
].corr().iloc[0, 1]

st.metric(
    "Observed Correlation",
    f"{correlation:.3f}"
)

st.info(
    "This is an observational correlation in synthetic demonstration data. "
    "Correlation does NOT establish that pollution causes judicial delay. "
    "Real causal analysis would require validated longitudinal data."
)

st.subheader("🌱 Pollution Reduction → Administrative Burden Scenario")

scenario_reduction = float(
    data["scenario_pollution_reduction_pct"].mean()
)

scenario_burden = float(
    data["scenario_burden_reduction_pct"].mean()
)

s1, s2 = st.columns(2)

s1.metric(
    "Illustrative Pollution Reduction",
    f"{scenario_reduction:.0f}%"
)

s2.metric(
    "Illustrative Admin-Burden Reduction",
    f"{scenario_burden:.1f}%"
)

st.caption(
    "Scenario only — not a proven causal estimate."
)

st.header("📅 365-Day Disposal Strategy")

judges = 20
working_days = 220
disposals_per_judge_per_day = 3

annual_capacity = (
    judges
    * working_days
    * disposals_per_judge_per_day
)

actionable_cases = int(
    (data["disposal_readiness_score"] >= 75).sum()
)

cases_moved = min(
    actionable_cases,
    annual_capacity
)

x1, x2, x3 = st.columns(3)

x1.metric(
    "Illustrative Annual Capacity",
    annual_capacity
)

x2.metric(
    "Actionable Cases",
    actionable_cases
)

x3.metric(
    "Cases Moved Toward Disposal",
    cases_moved
)

st.write(
    "NYAYA-1YEAR combines ML-based prioritisation with available judicial "
    "capacity to support a measurable one-year pendency-reduction strategy."
)

st.divider()

st.caption(
    "NYAYA-1YEAR is an AI-assisted administrative decision-support prototype. "
    "Real deployment requires validated court data, environmental monitoring "
    "data, privacy/security controls, legal governance and human oversight."
)
