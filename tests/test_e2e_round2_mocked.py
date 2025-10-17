import json
import os

from src import server


def test_e2e_round2_mocked(monkeypatch, tmp_path):
    # set secret env
    monkeypatch.setenv('secret', 'test-secret')

    captured = {}

    def fake_notify(url, payload, timeout_minutes=10):
        captured['url'] = url
        captured['payload'] = payload
        return True

    # patch the reference used by src.server
    monkeypatch.setattr('src.server.notify_evaluation', fake_notify)

    # patch get_authenticated_user to return fake owner
    monkeypatch.setattr('src.server.get_authenticated_user', lambda: 'fakeuser')

    # patch clone to create dest_dir
    def fake_clone(owner, repo_name, dest_dir):
        os.makedirs(dest_dir, exist_ok=True)
        return f"https://github.com/{owner}/{repo_name}.git"

    monkeypatch.setattr('src.server.clone_repo_to_dir', fake_clone)

    # patch commit_and_push to noop
    monkeypatch.setattr('src.server.commit_and_push', lambda dest_dir, message="": None)

    # patch subprocess.check_output used to get commit sha
    monkeypatch.setattr('src.server.subprocess.check_output', lambda *args, **kwargs: b'newsha123')

    # run handle_build synchronously by replacing Thread
    class ImmediateThread:
        def __init__(self, target, args=()):
            self._target = target
            self._args = args

        def start(self):
            self._target(*self._args)

    monkeypatch.setattr('threading.Thread', ImmediateThread)

    client = server.app.test_client()
    payload = {
        "email": "student@example.com",
        "secret": "test-secret",
        "task": "demo-task",
        "round": 2,
        "nonce": "n2",
        "brief": "Add SVG handling",
        "checks": [],
        "evaluation_url": "http://example.test/eval",
        "attachments": []
    }

    resp = client.post('/api-endpoint', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200

    assert 'payload' in captured
    p = captured['payload']
    assert p['round'] == 2
    assert p['repo_url'] == 'https://github.com/fakeuser/demo-task'
    assert p['commit_sha'] == 'newsha123'
