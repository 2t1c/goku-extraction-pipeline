#!/usr/bin/env python3
"""typefully_upload.py — Upload a video to a Typefully draft and attach as media.

Usage:
    typefully_upload.py <social_set_id> <draft_id> <file_path> <filename> [<post_text_file>]

Flow (per Typefully API):
    1. POST /v1/media-uploads → {media_id, upload_url} (presigned S3)
    2. PUT raw bytes to upload_url (no headers, no auth — signature was calculated without them)
    3. Poll GET /v1/media-uploads/<media_id> until status == "ready"
       (Typefully server-side video processing takes 5–15 min)
    4. PATCH /v1/drafts/<draft_id> with the existing post text + media_ids: [media_id]

Race-condition warning:
    Typefully UI edits AFTER an API attach can strip the media_ids array. If the user
    edits the draft in the browser before refreshing, their save will overwrite our attach.
    Always tell the user: refresh the Typefully tab before any further hand-editing.
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error

API = "https://api.typefully.com/v1"
TOKEN = os.environ.get("TYPEFULLY_API_KEY")
if not TOKEN:
    print("ERROR: TYPEFULLY_API_KEY env var not set", file=sys.stderr)
    sys.exit(1)

HEADERS = {
    "X-API-KEY": TOKEN,
    "Content-Type": "application/json",
}


def http(method, url, data=None, headers=None):
    h = headers or HEADERS
    if data is not None and isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"{method} {url} → {e.code}\n{e.read().decode()}", file=sys.stderr)
        raise


def put_bytes(url, file_path):
    """Plain PUT, no headers — presigned URL signature excludes them."""
    with open(file_path, "rb") as f:
        data = f.read()
    req = urllib.request.Request(url, data=data, method="PUT")
    try:
        with urllib.request.urlopen(req) as r:
            return r.status
    except urllib.error.HTTPError as e:
        print(f"PUT {url} → {e.code}\n{e.read().decode()}", file=sys.stderr)
        raise


def main():
    if len(sys.argv) < 5:
        print(__doc__, file=sys.stderr)
        sys.exit(1)

    social_set_id = sys.argv[1]
    draft_id = sys.argv[2]
    file_path = sys.argv[3]
    filename = sys.argv[4]
    post_text = open(sys.argv[5]).read() if len(sys.argv) > 5 else None

    print(f"[1/4] Creating media upload session for {filename}...")
    sess = http(
        "POST",
        f"{API}/media-uploads",
        {"social_set_id": int(social_set_id), "file_name": filename},
    )
    media_id = sess["media_id"]
    upload_url = sess["upload_url"]
    print(f"      media_id={media_id}")

    print(f"[2/4] PUT bytes to S3 ({os.path.getsize(file_path)} bytes)...")
    status = put_bytes(upload_url, file_path)
    print(f"      HTTP {status}")

    print("[3/4] Polling media status (5–15 min)...")
    while True:
        s = http("GET", f"{API}/media-uploads/{media_id}?social_set_id={social_set_id}")
        st = s.get("status")
        print(f"      status={st}")
        if st == "ready":
            break
        if st == "failed":
            print("ERROR: media processing failed", file=sys.stderr)
            sys.exit(1)
        time.sleep(15)

    print("[4/4] Attaching media to draft...")
    if post_text is None:
        # Fetch existing draft text so we don't overwrite user edits.
        d = http("GET", f"{API}/drafts/{draft_id}?social_set_id={social_set_id}")
        post_text = d["platforms"]["x"]["posts"][0]["text"]

    payload = {
        "platforms": {
            "x": {
                "enabled": True,
                "posts": [{"text": post_text, "media_ids": [media_id]}],
            }
        }
    }
    http("PATCH", f"{API}/drafts/{draft_id}?social_set_id={social_set_id}", payload)
    print("DONE — media attached.")
    print()
    print("⚠️  WARNING: Typefully UI edits will strip this media if the user doesn't")
    print("    refresh their tab first. Tell the user before they touch the draft.")


if __name__ == "__main__":
    main()
