"""HealthAudience AI — synthetic healthcare audience intelligence demo."""
from pathlib import Path

import plotly.express as px
import streamlit as st

from audience import (AGE_GROUPS, CHANNELS, COLUMNS, INTERESTS, REGIONS, RULES,
                      SEGMENTS, insights, metrics, read_csv, segment_data, summary_report)

st.set_page_config(page_title="HealthAudience AI", page_icon="◈", layout="wide")
st.markdown("""<style>
.stApp {background: #f3f7fa; color: #142b45;}
[data-testid="stSidebar"] {background: #10283f;}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {color: #eef8fa;}
[data-testid="stMetric"] {background: white; border: 1px solid #dce7ed;
 border-top: 4px solid #0e948c; padding: 20px; border-radius: 12px;}
.hero {background: #10283f; padding: 30px; border-radius: 16px; color: white; margin-bottom: 18px;}
.hero h1 {color: white; margin: 0; font-size: 2.4rem;}
.hero p {color: #bfdee3; margin-bottom: 0;}
.eyebrow {color: #63d6c7; font-size: .8rem; letter-spacing: .16em; font-weight: 700;}
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="hero"><div class="eyebrow">AUDIENCE INTELLIGENCE · SYNTHETIC DEMO</div>
<h1>HealthAudience AI</h1><p>Understand engagement. Design relevant outreach. Make campaign decisions explainable.</p></div>""", unsafe_allow_html=True)
st.caption("All data is synthetic. Descriptive rules only • No medical predictions • No LLM-generated insights")

with st.sidebar:
    st.title("◈ HealthAudience AI")
    st.caption("SYNTHETIC DATA WORKSPACE")
    uploaded = st.file_uploader("Upload a synthetic audience CSV", type=["csv"])
    confirmed = st.checkbox("I confirm this upload is synthetic and contains no real personal or health information.")
    with st.expander("CSV schema & template"):
        st.write("Required columns: " + ", ".join(COLUMNS))
        st.write("Engagement score: 0–100. IDs must be unique. Download the sample for accepted category values.")
        st.download_button("Download sample CSV", Path(__file__).parent.joinpath("data/sample_audience.csv").read_bytes(), "sample_audience.csv", "text/csv")

sample_path = Path(__file__).parent / "data/sample_audience.csv"
source = "Bundled synthetic sample (seed 42)"
if uploaded is not None:
    if not confirmed:
        st.info("Confirm that your upload is synthetic before loading it. The sample remains active.")
        df = read_csv(sample_path.read_bytes())
    else:
        try:
            df = read_csv(uploaded.getvalue())
            source = "User-confirmed synthetic CSV"
            st.success(f"Validated {len(df):,} synthetic records. Extra columns are ignored.")
        except ValueError as exc:
            st.error(f"Upload rejected: {exc}")
            st.info("Correct the CSV and upload again. No uploaded data is being used.")
            st.stop()
else:
    df = read_csv(sample_path.read_bytes())
df = segment_data(df)
with st.sidebar:
    st.divider()
    st.subheader("Explore your audience")
    regions = st.multiselect("Regions", REGIONS, default=REGIONS)
    ages = st.multiselect("Age groups", AGE_GROUPS, default=AGE_GROUPS)
    interests = st.multiselect("Service interests", INTERESTS, default=INTERESTS)
    channels = st.multiselect("Preferred channels", CHANNELS, default=CHANNELS)
    segments = st.multiselect("Audience segments", SEGMENTS, default=SEGMENTS)
    score = st.slider("Engagement range", 0, 100, (0, 100))
    st.caption("Clear a selection to show no records. Filters apply to all charts, insights, and exports.")

filtered = df[df.region.isin(regions) & df.age_group.isin(ages)
              & df.service_interest.isin(interests) & df.preferred_channel.isin(channels)
              & df.segment.isin(segments) & df.engagement_score.between(*score)]
filters = {"regions": regions, "age_groups": ages, "interests": interests,
           "channels": channels, "segments": segments, "engagement_range": score}
m = metrics(filtered)
st.caption(f"{source} · {len(filtered):,} of {len(df):,} consumers selected")
for column, label, value in zip(st.columns(4),
                              ["Audience size", "Mean engagement", "Response rate", "Registration rate"],
                              [f"{m['consumers']:,}", f"{m['engagement']:.1f}/100" if len(filtered) else "—",
                               f"{m['response_rate']:.1f}%" if len(filtered) else "—",
                               f"{m['registration_rate']:.1f}%" if len(filtered) else "—"]):
    column.metric(label, value)
st.caption("Response = Clicked or Registered. Registration is a campaign action. Rates use all selected consumers as the denominator.")

overview, strategy, records = st.tabs(["Audience overview", "Insights & strategy", "Data & exports"])
COLORS = ["#0e948c", "#315c82", "#9cb7c9"]


def chart(fig):
    fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font_color="#142b45", margin=dict(l=15, r=15, t=50, b=25))
    st.plotly_chart(fig, use_container_width=True)


with overview:
    if filtered.empty:
        st.info("No consumers match these filters. Expand the selections or engagement range.")
    else:
        left, right = st.columns(2)
        counts = filtered.segment.value_counts().reindex(SEGMENTS, fill_value=0).rename_axis("segment").reset_index(name="consumers")
        with left:
            chart(px.pie(counts, names="segment", values="consumers", hole=.65,
                         title="Behavioral audience segments", color="segment",
                         color_discrete_map=dict(zip(SEGMENTS, COLORS))))
        with right:
            channel_counts = filtered.preferred_channel.value_counts().rename_axis("channel").reset_index(name="consumers")
            chart(px.bar(channel_counts, x="channel", y="consumers", title="Preferred communication channels", color_discrete_sequence=COLORS))
        left, right = st.columns(2)
        with left:
            chart(px.histogram(filtered, x="engagement_score", nbins=20, title="Engagement distribution", color_discrete_sequence=COLORS, labels={"engagement_score": "Engagement score"}))
        with right:
            response = filtered.groupby(["region", "campaign_response"]).size().reset_index(name="consumers")
            chart(px.bar(response, x="region", y="consumers", color="campaign_response", title="Campaign responses by region", color_discrete_sequence=COLORS))
        left, right = st.columns(2)
        with left:
            interest_counts = filtered.service_interest.value_counts().rename_axis("interest").reset_index(name="consumers")
            chart(px.bar(interest_counts, x="consumers", y="interest", orientation="h", title="Stated service interests", color_discrete_sequence=COLORS))
        with right:
            age_counts = filtered.age_group.value_counts().reindex(AGE_GROUPS, fill_value=0).rename_axis("age_group").reset_index(name="consumers")
            chart(px.bar(age_counts, x="age_group", y="consumers", title="Age group mix", color_discrete_sequence=COLORS))
with strategy:
    st.subheader("From observed behavior to campaign experiments")
    st.write("Recommendations are generated by deterministic rules from the filtered audience. They suggest experiments, not predicted outcomes.")
    for title, body in insights(filtered):
        with st.container(border=True):
            st.markdown(f"**{title}**")
            st.write(body)
    if filtered.empty:
        st.info("Select at least one record to generate recommendations.")
    with st.expander("How the segments and recommendations work", expanded=True):
        for name, rule in RULES.items():
            st.write(f"**{name}:** {rule}")
        st.write("Segments are mutually exclusive and exhaustive. Channel and interest recommendations use the most frequent category; ties follow the first observed category. Segment recommendations appear only when that segment is present. Small audiences (<30) receive a caution.")
        st.caption("Fictional data does not represent a real population. These associations do not establish causation. Respect communication consent and opt-outs in any real-world implementation.")
with records:
    st.subheader("Synthetic audience records")
    st.dataframe(filtered, hide_index=True, use_container_width=True)
    left, right = st.columns(2)
    with left:
        st.download_button("Download filtered synthetic CSV", filtered.to_csv(index=False).encode("utf-8"), "synthetic_audience_filtered.csv", "text/csv")
    with right:
        st.download_button("Download audience summary", summary_report(filtered, source, filters), "synthetic_audience_summary.txt", "text/plain")
st.divider()
st.caption("HealthAudience AI · Interview portfolio project · Synthetic data only · Transparent rules, explainable decisions")
