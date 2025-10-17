import os
import json
from src import server


def test_api_endpoint_accepts_request(monkeypatch):
    # set shared secret for server
    monkeypatch.setenv('SHARED_SECRET', 's123')

    # patch handle_build to avoid side effects
    monkeypatch.setattr(server, 'handle_build', lambda body: None)

    app = server.app.test_client()
    payload = {
        "email": "student@example.com",
        "secret": "s123",
        "task": "demo-task",
        "round": 1,
        "nonce": "n1",
        "brief": "Say hi",
        "evaluation_url": "http://example.test/eval",
        "attachments": []
    }
    resp = app.post('/api-endpoint', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get('status') == 'accepted'
