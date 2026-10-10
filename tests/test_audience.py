from pathlib import Path
import pandas as pd
import pytest
from audience import COLUMNS, SEGMENTS, generate_data, insights, metrics, read_csv, segment_data, summary_report, validate_data

def test_reproducible_sample():
    df = generate_data()
    pd.testing.assert_frame_equal(df, generate_data())
    assert len(df) == 500 and df.consumer_id.is_unique
    assert not df.equals(generate_data(seed=43))
    pd.testing.assert_frame_equal(df, read_csv(Path("data/sample_audience.csv").read_bytes()))

def test_segment_boundaries():
    df = generate_data(7)
    df["engagement_score"] = [39, 40, 69, 70, 70, 100, 0]
    df["campaign_response"] = ["Registered", "No response", "Clicked", "No response", "Clicked", "Registered", "No response"]
    result = segment_data(df)
    assert result.segment.tolist() == [SEGMENTS[2], SEGMENTS[1], SEGMENTS[1], SEGMENTS[1], SEGMENTS[0], SEGMENTS[0], SEGMENTS[2]]
    assert "segment" not in df.columns

@pytest.mark.parametrize("column,value,message", [
    ("engagement_score", -1, "0 to 100"), ("engagement_score", 101, "0 to 100"),
    ("engagement_score", "bad", "0 to 100"), ("engagement_score", float("inf"), "0 to 100"),
    ("region", "Unknown", "Invalid region"), ("age_group", "12", "Invalid age_group"),
    ("preferred_channel", "Fax", "Invalid preferred_channel"), ("service_interest", "Other", "Invalid service_interest"),
    ("campaign_response", "Converted", "Invalid campaign_response"),
    ("consumer_id", "  ", "empty values"), ("region", None, "blank values")])
def test_invalid_fields(column, value, message):
    df = generate_data(2).astype({"engagement_score": object})
    df.loc[0, column] = value
    with pytest.raises(ValueError, match=message):
        validate_data(df)

def test_missing_duplicate_empty():
    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(generate_data().drop(columns="region"))
    df = generate_data(2)
    df.loc[1, "consumer_id"] = df.loc[0, "consumer_id"]
    with pytest.raises(ValueError, match="unique"):
        validate_data(df)
    with pytest.raises(ValueError, match="no audience records"):
        validate_data(pd.DataFrame(columns=COLUMNS))

@pytest.mark.parametrize("content", [b"", b"\xff", b'consumer_id,region\n"unclosed'])
def test_bad_csv(content):
    with pytest.raises(ValueError, match="Could not read"):
        read_csv(content)

def test_limits_and_extra_columns():
    with pytest.raises(ValueError, match="10 MB"):
        read_csv(b"x" * (10 * 1024 * 1024 + 1))
    with pytest.raises(ValueError, match="100,000"):
        validate_data(pd.concat([generate_data(1)] * 100001, ignore_index=True))
    assert validate_data(generate_data(2).assign(extra="discarded")).columns.tolist() == COLUMNS

def test_metrics_insights_report_and_empty():
    df = segment_data(generate_data(3))
    df["campaign_response"] = ["Clicked", "Registered", "No response"]
    df["preferred_channel"] = "SMS"
    assert metrics(df)["response_rate"] == pytest.approx(200 / 3)
    assert metrics(df)["registration_rate"] == pytest.approx(100 / 3)
    assert "SMS" in insights(df)[0][1] and "3/3" in insights(df)[0][1]
    assert any(title == "Small audience" for title, _ in insights(df))
    report = summary_report(df, "Synthetic test", {"region": "West"})
    assert "SYNTHETIC" in report and "West" in report and "Consumers: 3" in report
    empty = df.iloc[:0]
    assert insights(empty) == [] and metrics(empty)["consumers"] == 0
    assert "No records" in summary_report(empty, "Test", {})

def test_csv_export_roundtrip():
    df = segment_data(generate_data())
    selected = df[df.region == "West"]
    exported = read_csv(selected.to_csv(index=False).encode())
    assert len(exported) == len(selected) and exported.region.eq("West").all()
