#!/usr/bin/env python3

import json
import os
import sys
import uuid

import sentry_sdk
from sentry_sdk.envelope import Envelope, Item

SAFE_FIELDS = (
    "breadcrumbs",
    "contexts",
    "dist",
    "environment",
    "extra",
    "logentry",
    "message",
    "release",
    "request",
    "sdk",
    "tags",
    "user",
)

def main():
    if len(sys.argv) < 2:
        print("Usage: upload.py <path to minidump> [<path to event.json>]")
        return 1

    SENTRY_DSN = os.getenv("SENTRY_DSN")
    if not SENTRY_DSN:
        print("Error: SENTRY_DSN environment variable not set")
        return 1

    minidump = sys.argv[1]
    event = sys.argv[2] if len(sys.argv) > 2 else None

    with open(minidump, "rb") as f:
        minidump_data = f.read()
        if len(minidump_data) < 4 or minidump_data[:4] != b"MDMP":
            print("Error: Not a minidump")
            return 1

    event_id = uuid.uuid4().hex

    envelope = Envelope(headers={"event_id": event_id})
    envelope.add_item(Item(
        payload=minidump_data,
        type="attachment",
        filename=os.path.basename(minidump),
        headers={"attachment_type": "event.minidump"}
    ))

    if event:
        with open(event, "r") as f:
            event_data = json.load(f)

        if not isinstance(event_data, dict):
            print("Error: Event data is not a dictionary")
            return 1

        event_data = {k: v for k, v in event_data.items() if k in SAFE_FIELDS}
        envelope.add_event(event_data)

    sentry_sdk.init(dsn=SENTRY_DSN, default_integrations=False)
    sentry_sdk.Hub.current.client.transport.capture_envelope(envelope)
    sentry_sdk.flush()

    print(event_id)
    return 0


if __name__ == "__main__":
    sys.exit(main())
