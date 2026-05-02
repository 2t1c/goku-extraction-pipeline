#!/usr/bin/env python3
"""Multi-part upload a file to Notion and attach as a video block on a page.

Usage: notion_upload.py <page_id> <file_path> <filename>
"""
import json
import os
import sys
import urllib.request
import urllib.error
import mimetypes
import uuid

TOKEN = os.environ["NOTION_TOKEN"]
API = "https://api.notion.com/v1"
HEADERS_JSON = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json",
}
HEADERS_NOJSON = {
    "Authorization": f"Bearer {TOKEN}",
    "Notion-Version": "2022-06-28",
}

PART_SIZE = 10 * 1024 * 1024  # 10 MB per part — under 20 MB cap, over 5 MB min


def http(method, url, data=None, headers=None):
    h = headers or HEADERS_JSON
    if data is not None and isinstance(data, (dict, list)):
        data = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        raise RuntimeError(f"{method} {url} → {e.code}\n{body}")


def multipart_body(fields, file_field_name, file_bytes, filename, content_type):
    boundary = "----NotionUploadBoundary" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(
            f'Content-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(
        f'Content-Disposition: form-data; name="{file_field_name}"; filename="{filename}"\r\n'.encode()
    )
    parts.append(f"Content-Type: {content_type}\r\n\r\n".encode())
    parts.append(file_bytes)
    parts.append(f"\r\n--{boundary}--\r\n".encode())
    body = b"".join(parts)
    return body, f"multipart/form-data; boundary={boundary}"


def main():
    page_id, file_path, filename = sys.argv[1], sys.argv[2], sys.argv[3]
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    size = os.path.getsize(file_path)
    n_parts = (size + PART_SIZE - 1) // PART_SIZE
    print(f"File: {file_path} ({size} bytes) → {n_parts} parts")

    print("[1/4] Creating multi-part upload session...")
    sess = http("POST", f"{API}/file_uploads", {
        "filename": filename,
        "content_type": content_type,
        "mode": "multi_part",
        "number_of_parts": n_parts,
    })
    upload_id = sess["id"]
    send_url = sess["upload_url"]
    print(f"      upload_id={upload_id}")

    with open(file_path, "rb") as f:
        for i in range(1, n_parts + 1):
            chunk = f.read(PART_SIZE)
            print(f"[2/4] Uploading part {i}/{n_parts} ({len(chunk)} bytes)...")
            body, ctype = multipart_body(
                {"part_number": str(i)}, "file", chunk, filename, content_type,
            )
            headers = dict(HEADERS_NOJSON)
            headers["Content-Type"] = ctype
            req = urllib.request.Request(send_url, data=body, method="POST", headers=headers)
            try:
                with urllib.request.urlopen(req) as r:
                    resp = json.loads(r.read())
                    print(f"      part {i} status={resp.get('status')}")
            except urllib.error.HTTPError as e:
                print(f"      ERROR part {i}: {e.code}\n{e.read().decode()}")
                sys.exit(1)

    print("[3/4] Completing upload...")
    done = http("POST", f"{API}/file_uploads/{upload_id}/complete", {})
    print(f"      status={done.get('status')}")

    print("[4/4] Attaching video block to page...")
    attach = http("PATCH", f"{API}/blocks/{page_id}/children", {
        "children": [{
            "type": "video",
            "video": {"type": "file_upload", "file_upload": {"id": upload_id}},
        }],
    })
    n_blocks = len(attach.get("results", []))
    block_id = attach.get("results", [{}])[0].get("id", "?")
    print(f"      {n_blocks} block(s) attached, block_id={block_id}")
    print("DONE")


if __name__ == "__main__":
    main()
