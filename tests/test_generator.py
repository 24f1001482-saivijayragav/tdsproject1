import tempfile
import os
from src.generator import generate_app


def test_generate_app_creates_files():
    body = {"brief": "Say hello", "attachments": [{"name": "sample.txt", "url": "data:text/plain;base64,SGVsbG8gd29ybGQ="}]}
    with tempfile.TemporaryDirectory() as td:
        generate_app(body, td)
        assert os.path.exists(os.path.join(td, "index.html"))
        assert os.path.exists(os.path.join(td, "README.md"))
        assert os.path.exists(os.path.join(td, "LICENSE"))
        assert os.path.exists(os.path.join(td, "assets", "sample.txt"))
