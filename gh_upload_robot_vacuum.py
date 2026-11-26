"""Upload main.py and README.md to the entry's GitHub repository.

Uses the GitHub Contents API (PUT create-or-update, checking the
existing blob sha first). The parent uploads the remaining files
(LICENSE, this script, entry-state.json) with a second script so the
bundle snapshot tree matches the GitHub HEAD tree.
"""
import base64
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, "/opt/muse/skills/custom-connector-setup/bin")
from dynamic_credentials import add_surrogate_to_request  # noqa: E402

OWNER = "rezimtirani"
REPO = "u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2-entry"
API = "https://api.github.com"
ENTRY = Path("/home/hatch/workspace/makefun/u-eager-stork-81-9647-the-robot-vacuum-s-funniest-9822fbd2-entry")
FILES = ["main.py", "README.md"]


def github_request(method, url, payload=None):
    body = None
    headers = {"Accept": "application/vnd.github+json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    add_surrogate_to_request(request, "custom.github", allowed_hosts=["api.github.com"])
    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode("utf-8"))


def remote_sha(path):
    try:
        info = github_request("GET", f"{API}/repos/{OWNER}/{REPO}/contents/{path}")
    except urllib.error.HTTPError as error:
        if error.code == 404:
            return None
        raise
    return info.get("sha")


def push_one(path):
    local = ENTRY / path
    encoded = base64.b64encode(local.read_bytes()).decode("ascii")
    payload = {
        "message": f"Add {path} — Robot Vacuum entry",
        "content": encoded,
    }
    sha = remote_sha(path)
    if sha:
        payload["sha"] = sha
    result = github_request(
        "PUT", f"{API}/repos/{OWNER}/{REPO}/contents/{path}", payload
    )
    print(f"uploaded {path} -> {result['commit']['sha']}")
    return result["commit"]["sha"]


def main():
    for name in FILES:
        push_one(name)
    print(f"done: https://github.com/{OWNER}/{REPO}")


if __name__ == "__main__":
    main()
