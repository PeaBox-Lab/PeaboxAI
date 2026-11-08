"""Tests for the provider abstraction layer (no network access required)."""
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

import providers


# ---------- pure helpers ----------

def test_parse_parameters():
    text = 'temperature 0.7\n"num_ctx" 8192\n\nbadline\ntop_p 0.5\ntop_p 0.9\n'
    parsed = providers._parse_parameters(text)
    assert parsed == {'temperature': '0.7', 'num_ctx': '8192', 'top_p': '0.5'}


def test_infer_cloud_capabilities():
    caps = providers.infer_cloud_capabilities('OpenAI', 'gpt-4o')
    assert {'chat', 'vision'} <= caps
    assert providers.infer_cloud_capabilities('Groq', 'llama-3-8b') == {'chat', 'attachments_text'}


# ---------- mock Ollama HTTP server ----------

class OllamaHandler(BaseHTTPRequestHandler):
    state = {}

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/api/tags':
            self._json({'models': [{'name': 'testmodel:latest'}]})
        else:
            self._json({'error': 'not found'}, 404)

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        payload = json.loads(self.rfile.read(length) or b'{}')
        OllamaHandler.state['last_request'] = payload
        if self.path == '/api/show':
            self._json({'capabilities': ['completion', 'vision', 'thinking'],
                        'parameters': 'temperature 0.7\nnum_ctx 8192\n',
                        'details': {'parameter_size': '8B'}})
        elif self.path == '/api/chat':
            self._json({'message': {'role': 'assistant', 'content': 'mock reply',
                                    'thinking': 'mock thoughts'}})
        else:
            self._json({'error': 'not found'}, 404)

    def log_message(self, *args):
        pass


@pytest.fixture()
def ollama_server():
    srv = HTTPServer(('127.0.0.1', 0), OllamaHandler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f'http://127.0.0.1:{srv.server_address[1]}'
    srv.shutdown()


def test_discover_and_test_connection(ollama_server):
    cfg = {'base_url': ollama_server}
    models = providers.discover_models('Direct Ollama', cfg)
    assert [m.id for m in models] == ['testmodel:latest']
    assert 'vision' in models[0].capabilities and 'thinking' in models[0].capabilities
    assert models[0].parameters['temperature'] == '0.7'
    assert providers.test_connection('Direct Ollama', cfg) == 1


def test_chat_sends_options_think_and_num_predict(ollama_server):
    cfg = {'base_url': ollama_server}
    msgs = [{'role': 'system', 'content': 'be brief'}, {'role': 'user', 'content': 'hi'}]
    answer, thinking = providers.chat(
        'Direct Ollama', 'testmodel:latest', msgs,
        [{'name': 'a.png', 'media_type': 'image/png', 'base64': 'QUJD'}],
        dict(cfg, use_defaults=False, reasoning='High', temperature=0.2, top_p=0.5,
             top_k=10, repeat_penalty=1.1, num_ctx=4096, max_tokens=128))
    assert answer == 'mock reply'
    assert thinking == 'mock thoughts'
    sent = OllamaHandler.state['last_request']
    assert sent['think'] == 'high'
    assert sent['options']['num_predict'] == 128
    assert sent['options']['num_ctx'] == 4096
    assert sent['messages'][-1]['images'] == ['QUJD']


def test_chat_model_defaults_omits_options(ollama_server):
    cfg = {'base_url': ollama_server}
    providers.chat('Direct Ollama', 'm', [{'role': 'user', 'content': 'hi'}], [],
                   dict(cfg, use_defaults=True))
    assert 'options' not in OllamaHandler.state['last_request']


# ---------- Anthropic adapter (mocked SDK) ----------

class _FakeBlock:
    type = 'text'
    text = 'anthropic answer'


class _FakeAnthropicResponse:
    content = [_FakeBlock()]


class _FakeAnthropicMessages:
    def __init__(self, sink):
        self._sink = sink

    def create(self, **kwargs):
        self._sink.update(kwargs)
        return _FakeAnthropicResponse()


class _FakeAnthropic:
    def __init__(self, sink, **kwargs):
        self.kwargs = kwargs
        self.messages = _FakeAnthropicMessages(sink)


def test_anthropic_system_prompt_is_forwarded(monkeypatch):
    sink = {}
    monkeypatch.setattr(providers, 'Anthropic', lambda **kw: _FakeAnthropic(sink, **kw))
    answer, _ = providers.chat(
        'Anthropic', 'claude-sonnet-4',
        [{'role': 'system', 'content': 'You are a pirate.'},
         {'role': 'user', 'content': 'ahoy'}],
        [], {'use_defaults': True, 'max_tokens': 100}, key='sk-test')
    assert answer == 'anthropic answer'
    assert sink['system'] == 'You are a pirate.'
    assert sink['messages'] == [{'role': 'user', 'content': 'ahoy'}]
    assert sink['max_tokens'] == 100


# ---------- OpenAI-compatible adapter (mocked SDK) ----------

class _FakeChoice:
    class message:
        content = 'openai answer'


class _FakeOpenAIResponse:
    choices = [_FakeChoice()]


class _FakeOpenAICompletions:
    def __init__(self, sink):
        self._sink = sink

    def create(self, **kwargs):
        self._sink.update(kwargs)
        return _FakeOpenAIResponse()


class _FakeOpenAI:
    def __init__(self, sink, **kwargs):
        self.chat = type('Chat', (), {'completions': _FakeOpenAICompletions(sink)})()


def test_openai_compatible_payload(monkeypatch):
    sink = {}
    monkeypatch.setattr(providers, 'OpenAI', lambda **kw: _FakeOpenAI(sink, **kw))
    answer, _ = providers.chat(
        'OpenAI', 'gpt-4o',
        [{'role': 'user', 'content': 'hi',
          }], [], {'use_defaults': False, 'temperature': 0.3, 'top_p': 0.9,
                   'max_tokens': 50, 'reasoning': 'Low'}, key='sk-test')
    assert answer == 'openai answer'
    assert sink['reasoning_effort'] == 'low'
    assert sink['max_tokens'] == 50
    assert sink['temperature'] == 0.3


def test_openai_reasoning_default_not_sent(monkeypatch):
    sink = {}
    monkeypatch.setattr(providers, 'OpenAI', lambda **kw: _FakeOpenAI(sink, **kw))
    providers.chat('Groq', 'llama-3', [{'role': 'user', 'content': 'hi'}], [],
                   {'use_defaults': True, 'reasoning': 'Default'}, key='sk-test')
    assert 'reasoning_effort' not in sink
