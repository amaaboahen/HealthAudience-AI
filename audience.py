"""Synthetic audience data and transparent descriptive campaign rules."""
from io import BytesIO
import random

import pandas as pd

AGE_GROUPS = ["18–24", "25–34", "35–44", "45–54", "55–64", "65+"]
REGIONS = ["Northeast", "Midwest", "South", "West"]
INTERESTS = ["Preventive care", "Telehealth", "Wellness programs", "Family care", "Specialist services"]
CHANNELS = ["Email", "SMS", "Social media", "Phone"]
RESPONSES = ["No response", "Clicked", "Registered"]
COLUMNS = ["consumer_id", "age_group", "region", "service_interest", "preferred_channel", "engagement_score", "campaign_response"]
SEGMENTS = ["Active responders", "Engaged explorers", "Re-engagement audience"]
RULES = {
    SEGMENTS[0]: "Engagement ≥ 70 and campaign response is Clicked or Registered.",
    SEGMENTS[1]: "Engagement ≥ 40 and not an Active responder.",
    SEGMENTS[2]: "Engagement < 40, regardless of campaign response.",
}


def generate_data(n: int = 500, seed: int = 42) -> pd.DataFrame:
    """Return deterministic fictional consumer records; no medical attributes."""
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        score = rng.randint(0, 100)
        weights = [20, 40, 40] if score >= 70 else ([45, 40, 15] if score >= 40 else [80, 17, 3])
        rows.append([f"SYN-{i + 1:04d}", rng.choice(AGE_GROUPS), rng.choice(REGIONS),
                     rng.choice(INTERESTS), rng.choices(CHANNELS, [40, 30, 20, 10])[0],
                     score, rng.choices(RESPONSES, weights)[0]])
    return pd.DataFrame(rows, columns=COLUMNS)


def validate_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validate the public CSV contract and return only canonical columns."""
    missing = sorted(set(COLUMNS) - set(df.columns))
    if missing:
        raise ValueError("Missing required columns: " + ", ".join(missing))
    if df.empty:
        raise ValueError("The CSV contains no audience records. Add at least one row.")
    if len(df) > 100_000:
        raise ValueError("Limit the dataset to 100,000 rows or fewer.")
    result = df[COLUMNS].copy()
    if result.isna().any().any():
        raise ValueError("Required fields contain blank values. Fill every required cell.")
    for col in COLUMNS:
        if col != "engagement_score":
            result[col] = result[col].astype(str).str.strip()
            if result[col].eq("").any():
                raise ValueError(f"{col} contains empty values.")
    if result.consumer_id.duplicated().any():
        raise ValueError("consumer_id must be unique. Remove duplicate IDs.")
    for col, allowed in [("age_group", AGE_GROUPS), ("region", REGIONS),
                         ("service_interest", INTERESTS), ("preferred_channel", CHANNELS),
                         ("campaign_response", RESPONSES)]:
        if not result[col].isin(allowed).all():
            raise ValueError(f"Invalid {col}. Allowed values: {', '.join(allowed)}.")
    scores = pd.to_numeric(result.engagement_score, errors="coerce")
    if scores.isna().any() or not scores.between(0, 100).all():
        raise ValueError("engagement_score must be a finite number from 0 to 100.")
    result["engagement_score"] = scores
    return result


def read_csv(content: bytes) -> pd.DataFrame:
    if len(content) > 10 * 1024 * 1024:
        raise ValueError("CSV files must be 10 MB or smaller.")
    try:
        df = pd.read_csv(BytesIO(content), dtype={"consumer_id": str})
    except (pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeDecodeError) as exc:
        raise ValueError("Could not read this CSV. Use a UTF-8 file with a header and comma-separated fields.") from exc
    return validate_data(df)


def segment_data(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    result["segment"] = SEGMENTS[2]
    result.loc[result.engagement_score >= 40, "segment"] = SEGMENTS[1]
    result.loc[(result.engagement_score >= 70) & result.campaign_response.isin(RESPONSES[1:]), "segment"] = SEGMENTS[0]
    return result


def metrics(df: pd.DataFrame) -> dict:
    return {
        "consumers": len(df),
        "engagement": float(df.engagement_score.mean()) if len(df) else 0.0,
        "response_rate": float(df.campaign_response.ne("No response").mean() * 100) if len(df) else 0.0,
        "registration_rate": float(df.campaign_response.eq("Registered").mean() * 100) if len(df) else 0.0,
    }


def insights(df: pd.DataFrame) -> list[tuple[str, str]]:
    if df.empty:
        return []
    channel = df.preferred_channel.value_counts().idxmax()
    channel_count = int(df.preferred_channel.eq(channel).sum())
    interest = df.service_interest.value_counts().idxmax()
    interest_count = int(df.service_interest.eq(interest).sum())
    items = [
        ("Lead with the preferred channel", f"{channel} is preferred by {channel_count}/{len(df)} consumers ({channel_count / len(df):.1%}). Test an opt-in {channel.lower()} campaign with a clear call to action."),
        ("Make the message relevant", f"{interest} is the most common stated interest ({interest_count}/{len(df)} consumers). Test educational content about available services; avoid health-status assumptions."),
    ]
    for segment, action in zip(SEGMENTS, ["Test a concise registration invitation and compare results with a holdout group.", "Test useful service information with a low-friction next step.", "Test a low-frequency preference check; honor opt-outs before further outreach."]):
        count = int(df.segment.eq(segment).sum())
        if count:
            items.append((segment, f"{count}/{len(df)} consumers ({count / len(df):.1%}). {action}"))
    if len(df) < 30:
        items.append(("Small audience", "Fewer than 30 records match these filters. Treat percentages as descriptive and avoid broad conclusions."))
    return items


def summary_report(df: pd.DataFrame, source: str, filters: dict) -> str:
    m = metrics(df)
    lines = ["HealthAudience AI | SYNTHETIC DATA ONLY", "Descriptive campaign planning; no medical predictions or LLM-generated insights.",
             f"Source: {source}", f"Filters: {filters}", f"Consumers: {m['consumers']}",
             f"Mean engagement: {m['engagement']:.1f}/100", f"Response rate: {m['response_rate']:.1f}%", f"Registration rate: {m['registration_rate']:.1f}%",
             "", "Segment rules:"]
    lines += [f"{name}: {rule}" for name, rule in RULES.items()]
    lines += ["", "Insights and suggested experiments:"]
    lines += [f"{title}: {body}" for title, body in insights(df)]
    if df.empty:
        lines.append("No records match the current filters.")
    lines += ["", "Limitations: fictional sample; results do not represent a real population. Rules describe observed behavior, do not establish causation, and do not predict health outcomes. Response means Clicked or Registered; registration is a campaign action, not a medical outcome."]
    return "\n".join(lines)
