from streamlit.testing.v1 import AppTest
from io import BytesIO
import streamlit as st
from audience import generate_data

def test_dashboard_filters_and_exports():
    app = AppTest.from_file("app.py", default_timeout=30).run()
    assert not app.exception
    assert app.metric[0].value == "500"
    assert len(app.get("plotly_chart")) == 6
    assert len(app.get("download_button")) == 3
    app.multiselect[0].set_value(["West"]).run()
    assert not app.exception
    assert 0 < int(app.metric[0].value) < 500
    assert app.dataframe[0].value.region.eq("West").all()
    app.multiselect[0].set_value([]).run()
    assert not app.exception and app.metric[0].value == "0"
    assert app.metric[1].value == "—"
    assert len(app.get("plotly_chart")) == 0
    assert app.dataframe[0].value.empty

def test_confirmed_upload_and_invalid_upload(monkeypatch):
    # Inject the upload boundary because AppTest cannot operate the native picker.
    upload = BytesIO(generate_data(12).to_csv(index=False).encode())
    monkeypatch.setattr(st, "file_uploader", lambda *args, **kwargs: upload)
    app = AppTest.from_file("app.py", default_timeout=30).run()
    assert not app.exception and app.metric[0].value == "500"
    app.checkbox[0].check().run()
    assert not app.exception and app.metric[0].value == "12"
    assert any("Validated 12" in element.value for element in app.success)
    monkeypatch.setattr(st, "file_uploader", lambda *args, **kwargs: BytesIO(b"wrong,headers\n1,2"))
    app.run()
    assert not app.exception
    assert any("Missing required columns" in element.value for element in app.error)
    assert len(app.metric) == 0
