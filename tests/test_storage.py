"""Tests for the storage layer (SQLite conversations, messages, config)."""
import json

import pytest

import storage


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    db = tmp_path / 'test_workbench.db'
    monkeypatch.setattr(storage, 'DB_PATH', db)
    storage.init_db()
    return db


def test_create_and_list_conversation(fresh_db):
    cid = storage.new_conversation('First')
    convs = storage.list_conversations()
    assert [c['id'] for c in convs] == [cid]
    assert convs[0]['title'] == 'First'
    assert convs[0]['pinned'] == 0 and convs[0]['archived'] == 0


def test_add_and_load_messages_in_order(fresh_db):
    cid = storage.new_conversation('Chat')
    storage.add_message(cid, 'user', 'hello')
    storage.add_message(cid, 'assistant', 'hi', thinking='reasoning')
    messages = storage.load_messages(cid)
    assert [m['role'] for m in messages] == ['user', 'assistant']
    assert messages[1]['thinking'] == 'reasoning'


def test_pinned_conversations_sort_first(fresh_db):
    a = storage.new_conversation('Alpha')
    b = storage.new_conversation('Beta')
    storage.update_conversation(b, pinned=1)
    convs = storage.list_conversations()
    assert convs[0]['id'] == b


def test_archive_excluded_by_default_and_search_escaping(fresh_db):
    cid = storage.new_conversation('Quarterly 100% report')
    storage.update_conversation(cid, archived=1)
    assert storage.list_conversations() == []
    assert [c['id'] for c in storage.list_conversations(archived=True)] == [cid]
    # LIKE wildcards in the search term must be treated literally
    storage.update_conversation(cid, archived=0)
    assert storage.list_conversations('Quarterly%') == []
    assert [c['id'] for c in storage.list_conversations('100%')] == [cid]
    assert [c['id'] for c in storage.list_conversations('Quarterly')] == [cid]


def test_delete_conversation_cascades_messages(fresh_db):
    cid = storage.new_conversation('Doomed')
    storage.add_message(cid, 'user', 'bye')
    storage.delete_conversation(cid)
    assert storage.load_messages(cid) == []
    assert storage.list_conversations() == []


def test_export_conversation_roundtrip(fresh_db):
    cid = storage.new_conversation('Export me')
    storage.add_message(cid, 'user', 'hello export')
    data = storage.export_conversation(cid)
    assert data['conversation']['id'] == cid
    assert data['messages'][0]['content'] == 'hello export'


def test_export_missing_conversation_raises(fresh_db):
    with pytest.raises(ValueError, match='not found'):
        storage.export_conversation(99999)


def test_config_roundtrip(tmp_path, monkeypatch):
    cfg = tmp_path / 'config.json'
    monkeypatch.setattr(storage, 'CONFIG_PATH', cfg)
    storage.save_config({'app': {'default_provider': 'Direct Ollama'}})
    assert storage.load_config()['app']['default_provider'] == 'Direct Ollama'
    cfg.write_text('not json', encoding='utf-8')
    assert storage.load_config() == {}
