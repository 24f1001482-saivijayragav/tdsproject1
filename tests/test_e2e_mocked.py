import json
import threading
import os

from src import server


def test_e2e_round1_mocked(monkeypatch, tmp_path):
    # Ensure the server reads the expected secret
    monkeypatch.setenv('secret', 'test-secret')

    # Capture notifier payload
    captured = {}

    def fake_notify(url, payload, timeout_minutes=10):
        captured['url'] = url
        captured['payload'] = payload
        return True

    # patch the reference used by src.server
    monkeypatch.setattr('src.server.notify_evaluation', fake_notify)

    # Mock create_repo_from_dir to avoid network and git
    def fake_create_repo_from_dir(source_dir, task_name):
        return (
            f"https://github.com/fakeuser/{task_name}",
            "deadbeefcommit",
            f"https://fakeuser.github.io/{task_name}/",
        )

    # patch the reference used by src.server
    monkeypatch.setattr('src.server.create_repo_from_dir', fake_create_repo_from_dir)

    # Mock llm generator to return None (use placeholder generator)
    monkeypatch.setattr('src.llm_generator.OPENAI_API_KEY', None)

    # Replace Thread so handle_build runs synchronously for testing
    class ImmediateThread:
        def __init__(self, target, args=()):
            self._target = target
            self._args = args

        def start(self):
            # run inline
            self._target(*self._args)

    monkeypatch.setattr('threading.Thread', ImmediateThread)

    client = server.app.test_client()
    payload = {
        "email": "student@example.com",
        "secret": "test-secret",
        "task": "demo-task",
        "round": 1,
        "nonce": "n1",
        "brief": "Publish a page that shows Hello",
        "checks": [],
        "evaluation_url": "http://example.test/eval",
        "attachments": []
    }

    resp = client.post('/api-endpoint', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200

    # After synchronous run, notifier should have been called and captured
    assert 'payload' in captured
    p = captured['payload']
    assert p['email'] == payload['email']
    assert p['task'] == payload['task']
    assert p['round'] == payload['round']
    assert p['repo_url'].startswith('https://github.com/')
