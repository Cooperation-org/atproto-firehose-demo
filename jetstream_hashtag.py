"""Stream Bluesky posts from Jetstream and print ones matching a hashtag/substring.

Jetstream is Bluesky's simplified JSON firehose. Payloads are ~99% smaller
than the raw repo firehose and there's no CBOR/CAR to decode.

Server-side filtering: collections + DIDs only. Hashtag filter is client-side.
"""

import asyncio
import json

import websockets

JETSTREAM = "wss://jetstream2.us-east.bsky.network/subscribe"
WANTED_COLLECTIONS = "app.bsky.feed.post"
NEEDLE = "#tucson"  # case-insensitive substring; swap to facet-walk for strict hashtag match


def matches(record: dict) -> bool:
    text = (record.get("text") or "").lower()
    return NEEDLE in text


async def run() -> None:
    uri = f"{JETSTREAM}?wantedCollections={WANTED_COLLECTIONS}"
    async for ws in websockets.connect(uri, max_size=2**20):
        try:
            async for raw in ws:
                evt = json.loads(raw)
                if evt.get("kind") != "commit":
                    continue
                commit = evt.get("commit") or {}
                if commit.get("operation") != "create":
                    continue
                record = commit.get("record") or {}
                if record.get("$type") != "app.bsky.feed.post":
                    continue
                if not matches(record):
                    continue
                did = evt.get("did")
                rkey = commit.get("rkey")
                url = f"https://bsky.app/profile/{did}/post/{rkey}"
                print(f"{url}  ::  {record.get('text')}")
        except websockets.ConnectionClosed:
            continue  # auto-reconnect


if __name__ == "__main__":
    asyncio.run(run())
