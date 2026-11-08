"""Headless smoke tests for the Streamlit app and Settings page."""
import pathlib

import pytest
from streamlit.testing.v1 import AppTest

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_app_renders_without_exception():
    at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=60)
    at.run()
    assert not at.exception
    assert not at.error
    assert [t.label for t in at.tabs] == ['Chat', 'Attachments', 'Generation', 'Manage']
    assert any('New chat' in b.label for b in at.button)


def test_app_exposes_delete_confirmation():
    at = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=60)
    at.run()
    assert any('Confirm permanent delete' in cb.label for cb in at.checkbox)


def test_settings_page_renders_without_exception():
    at = AppTest.from_file(str(ROOT / 'pages' / '1_Settings.py'), default_timeout=60)
    at.run()
    assert not at.exception
    assert [t.label for t in at.tabs] == ['Providers & APIs', 'Workbench defaults', 'Storage & privacy']
