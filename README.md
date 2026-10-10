# HealthAudience AI

A healthcare audience intelligence portfolio project using Python, Streamlit, Pandas, and Plotly. Explore fictional consumers, explain behavioral segments, and suggest campaign experiments.

**Synthetic data only. No medical predictions. No LLM-generated insights.** No credentials, database, or paid services are required.

## Setup and run

Requires Python 3.10+; validated with Python 3.12. From the repository directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
```

On a local desktop, use the address printed by Streamlit. In a cloud environment use the platform's supported application access mechanism. Stop the server with Ctrl+C.

## Features

- Navy-and-teal dashboard, four KPI cards, six interactive charts, and sidebar filters.
- 500 reproducible synthetic records (seed 42).
- Three explainable audience segments and deterministic recommendations.
- Synthetic CSV uploads with schema validation, helpful errors, and a template.
- Filtered CSV downloads and summary reports with filter context and limitations.
- Empty audience handling and small-sample cautions.

## CSV contract

Upload only fictional data. Confirmation is a user assertion, not an automatic privacy detector. Uploads are processed in memory and are not intentionally persisted. UTF-8 CSV files must have a header, be at most 10 MB, and contain 1–100,000 rows. Required cells cannot be blank. Extra columns are discarded; headers are case-sensitive.

| Column | Accepted values |
| --- | --- |
| consumer_id | Unique nonblank identifier |
| age_group | `18–24`, `25–34`, `35–44`, `45–54`, `55–64`, `65+` (en dashes) |
| region | Northeast, Midwest, South, West |
| service_interest | Preventive care, Telehealth, Wellness programs, Family care, Specialist services |
| preferred_channel | Email, SMS, Social media, Phone |
| engagement_score | Finite number from 0 to 100 |
| campaign_response | No response, Clicked, Registered |

Download the sample template from the sidebar or use `data/sample_audience.csv`.

## Transparent methodology

| Segment | Rule | Suggested experiment |
| --- | --- | --- |
| Active responders | Score ≥70 and response is Clicked or Registered | Registration invitation with a holdout comparison |
| Engaged explorers | Score ≥40, excluding Active responders | Educational content with a low-friction next step |
| Re-engagement audience | Score <40, regardless of response | Low-frequency preference check honoring opt-outs |

These segments are mutually exclusive and exhaustive. The engagement score is an arbitrary synthetic indicator. Responses are sampled with higher response probabilities at higher scores to make the demonstration useful. This designed relationship is not evidence about real consumers.

Response rate is Clicked or Registered divided by all selected consumers; registration rate is Registered divided by all selected consumers. Registration is a campaign action, not a medical outcome. Mean engagement is the arithmetic mean. Empty audiences show no rate.

Recommendations use the most frequent channel and service interest, including counts and denominators; ties follow first appearance. Fixed segment actions appear only for represented segments. Audiences below 30 receive a caution. All charts, recommendations, and exports use the same filters. Rules do not establish causation, predict lift, or infer medical conditions. Real deployment would require privacy, consent, security, accessibility, and campaign governance work.

## Tests and reproducibility

```bash
source .venv/bin/activate
python -m pytest -q
python -c 'from audience import generate_data; generate_data().to_csv("data/sample_audience.csv", index=False)'
```

Tests exercise reproducibility, schema errors, parser errors, file and row limits, segment boundaries, metric denominators, empty selections, export round-trips, and Streamlit rendering and filters. Upload integration uses an injected file object to verify confirmation, successful loading, and rejected uploads; the native browser file picker is not covered by AppTest.

## Files

- `app.py`: Streamlit interface.
- `audience.py`: generation, validation, segments, metrics, recommendations, reports.
- `requirements.txt`: pinned runtime and test dependencies.
- `data/sample_audience.csv`: 500 synthetic consumers.
- `.streamlit/config.toml`: theme and server defaults.
- `tests/`: logic and UI integration tests.

For an interview demo, explore one region, explain segment rules, download a report, and demonstrate an invalid CSV and an empty audience. Emphasize reproducibility, explicit denominators, and the distinction between descriptive rules and predictions.
