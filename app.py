"""HealthAudience AI — synthetic healthcare audience intelligence demo."""
from pathlib import Path

import plotly.express as px
import streamlit as st

from audience import (AGE_GROUPS, CHANNELS, COLUMNS, INTERESTS, REGIONS, RULES,
                      SEGMENTS, insights, metrics, read_csv, segment_data, summary_report)

st.set_page_config(page_title="HealthAudience AI", page_icon="◈", layout="wide")
st.markdown("""<style>
:root {--ivory:#F8F6F2; --ink:#20232B; --violet:#7357F5; --coral:#FF7868; --lavender:#E9E3FF;}
.stApp {background:var(--ivory); color:var(--ink);}
[data-testid="stHeader"] {background:rgba(248,246,242,.95);}
[data-testid="stMainBlockContainer"] {max-width:1500px; padding-top:2.5rem;}
h1, h2, h3 {letter-spacing:-.035em; color:var(--ink);}
[data-testid="stCaptionContainer"], [data-testid="stCaptionContainer"] p {color:#62616D;}
[data-testid="stSidebar"] {background:#F0ECF7; border-right:1px solid #DED8EA;}
[data-testid="stSidebar"] h1 {font-size:1.5rem; letter-spacing:-.045em;}
[data-testid="stSidebar"] h3 {font-size:1.05rem;}
[data-testid="stSidebar"] [data-baseweb="select"] > div {background:white; border-color:#D7D1E3;}
[data-testid="stSidebar"] [data-baseweb="tag"] {background:var(--lavender); color:var(--ink);}
[data-testid="stMetric"] {background:white; border:1px solid #E4DFE9;
 border-top:3px solid var(--violet); padding:22px; border-radius:16px;
 box-sizing:border-box; height:100%; box-shadow:0 4px 18px rgba(32,35,43,.035);
 transition:box-shadow .18s ease, border-color .18s ease;}
[data-testid="stMetric"]:hover {box-shadow:0 8px 24px rgba(115,87,245,.10); border-color:#C4B7FF;}
/* Wrap KPI columns according to available content width, including an open sidebar. */
.st-key-kpi_grid {container-type:inline-size;}
.st-key-kpi_grid [data-testid="stHorizontalBlock"] {display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:1rem;}
.st-key-kpi_grid [data-testid="stColumn"] {min-width:0 !important; width:100% !important;}
@container (max-width:1000px) {
 .st-key-kpi_grid [data-testid="stHorizontalBlock"] {grid-template-columns:repeat(2,minmax(0,1fr));}
}
@container (max-width:460px) {
 .st-key-kpi_grid [data-testid="stHorizontalBlock"] {grid-template-columns:minmax(0,1fr);}
}
.st-key-kpi_grid [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {border-top-color:var(--coral);}
.st-key-kpi_grid [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {border-top-color:#B5A5FB;}
.st-key-kpi_grid [data-testid="stMetricLabel"], .st-key-kpi_grid [data-testid="stMetricLabel"] p {
 white-space:normal; overflow:visible; text-overflow:clip; overflow-wrap:anywhere; color:#62616D;}
.st-key-kpi_grid [data-testid="stMetricValue"], .st-key-kpi_grid [data-testid="stMetricValue"] > div {
 font-size:clamp(1.7rem,2.5vw,2.4rem); font-weight:650; letter-spacing:-.04em; line-height:1.3;
 white-space:normal; overflow:visible; text-overflow:clip; overflow-wrap:anywhere; color:var(--ink);}
.hero {padding:24px 0 30px; margin-bottom:12px; border-bottom:1px solid #DED8E6;}
.hero h1 {margin:12px 0 14px; font-size:clamp(2.5rem,5vw,4.5rem); font-weight:750; line-height:1.1; letter-spacing:-.065em;}
.hero .tagline {font-family:Georgia,'Times New Roman',serif; font-style:italic; font-size:clamp(1.35rem,2.6vw,2rem); color:#5940C6; line-height:1.35; margin:0 0 16px;}
.hero .description {color:#62616D; max-width:640px; font-size:1rem; line-height:1.7; margin:0;}
.eyebrow {display:inline-flex; align-items:center; gap:9px; color:#5940C6; font-size:.72rem; letter-spacing:.14em; font-weight:700;}
.eyebrow::before {content:''; width:8px; height:8px; background:var(--coral); border-radius:50%;}
[data-testid="stPlotlyChart"] {background:white; border:1px solid #E4DFE9; border-radius:16px; padding:8px; overflow:hidden;}
[data-testid="stVerticalBlockBorderWrapper"] > div {border-color:#E4DFE9 !important; border-radius:16px;}
[class*="st-key-insight_"] {background:white; border-radius:16px;}
[data-testid="stExpander"] {background:white; border-radius:12px;}
[data-testid="stTabs"] [role="tablist"] {gap:1.5rem; border-bottom:1px solid #DED8E6;}
[data-testid="stTabs"] [role="tab"] {font-weight:600; white-space:normal; height:auto; padding:12px 0;}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {color:#5940C6;}
[data-testid="stDownloadButton"] button {background:var(--violet); color:white; border:1px solid var(--violet); border-radius:10px; min-height:44px; transition:background .18s ease;}
[data-testid="stDownloadButton"] button:hover {background:#5940C6; color:white; border-color:#5940C6;}
button:focus-visible, a:focus-visible {outline:3px solid #5940C6 !important; outline-offset:3px;}
@media (max-width:640px) {
 [data-testid="stMainBlockContainer"] {padding:1.5rem 1rem;}
 .hero {padding:12px 0 24px;}
 .eyebrow {letter-spacing:.08em;}
 .st-key-kpi_grid [data-testid="stHorizontalBlock"] {grid-template-columns:minmax(0,1fr);}
 [data-testid="stMetric"] {padding:18px;}
 [data-testid="stTabs"] [role="tablist"] {gap:1rem;}
 [data-testid="stTabs"] [role="tab"] {font-size:.85rem;}
}
@media (prefers-reduced-motion:reduce) { [data-testid="stMetric"], [data-testid="stDownloadButton"] button {transition:none;} }
</style>""", unsafe_allow_html=True)
st.markdown("""<div class="hero"><div class="eyebrow">THE AUDIENCE INTELLIGENCE WORKSPACE</div>
<h1>HealthAudience AI</h1><p class="tagline">Understand your audience. Personalize your outreach.</p>
<p class="description">An intelligent workspace for exploring healthcare audiences, identifying engagement opportunities, and informing outreach strategies.</p></div>""", unsafe_allow_html=True)

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
with st.container(key="kpi_grid"):
    for column, label, value in zip(st.columns(4),
                                  ["Audience size", "Mean engagement", "Response rate", "Registration rate"],
                                  [f"{m['consumers']:,}", f"{m['engagement']:.1f}/100" if len(filtered) else "—",
                                   f"{m['response_rate']:.1f}%" if len(filtered) else "—",
                                   f"{m['registration_rate']:.1f}%" if len(filtered) else "—"]):
        column.metric(label, value)
st.caption("Response = Clicked or Registered. Registration is a campaign action. Rates use all selected consumers as the denominator.")

overview, strategy, records = st.tabs(["Audience overview", "Insights & strategy", "Data & exports"])
COLORS = ["#7357F5", "#FF7868", "#B5A5FB"]


def chart(fig):
    fig.update_layout(meta={"heading": fig.layout.title.text})
    fig.update_layout(
        template="plotly_white", paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(color="#20232B", size=12),
        title=dict(text=""),  # Native headings wrap on narrow screens.
        margin=dict(l=12, r=12, t=20, b=20), height=360,
        legend=dict(orientation="h", yanchor="top", y=-.22, x=0, title_text=""),
        hoverlabel=dict(bgcolor="#20232B", font_color="#FFFFFF"),
    )
    fig.update_xaxes(automargin=True, gridcolor="#F0ECF5", zeroline=False,
                     tickfont_color="#20232B", title_font_color="#20232B")
    fig.update_yaxes(automargin=True, gridcolor="#F0ECF5", zeroline=False,
                     tickfont_color="#20232B", title_font_color="#20232B")
    with st.container():
        st.markdown(f"**{fig.layout.meta['heading']}**")
        st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False})


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
    for index, (title, body) in enumerate(insights(filtered)):
        with st.container(border=True, key=f"insight_{index}"):
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
    st.dataframe(filtered, hide_index=True, width="stretch")
    left, right = st.columns(2)
    with left:
        st.download_button("Download filtered synthetic CSV", filtered.to_csv(index=False).encode("utf-8"), "synthetic_audience_filtered.csv", "text/csv")
    with right:
        st.download_button("Download audience summary", summary_report(filtered, source, filters), "synthetic_audience_summary.txt", "text/plain")
st.divider()
with st.expander("About This Demo"):
    st.write("HealthAudience AI uses synthetic healthcare audience data for demonstration. Segmentation follows transparent, rule-based thresholds; insights describe the selected records and suggest campaign experiments. The application does not make medical predictions or generate analysis using an LLM.")
    st.caption("Fictional records do not represent real people or a real population. Upload only synthetic data without personal or health information.")
st.caption("HealthAudience AI · Audience intelligence, thoughtfully explained.")
