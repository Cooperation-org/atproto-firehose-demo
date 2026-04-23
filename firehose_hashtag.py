"""Stream the raw AT Proto repo firehose and print posts matching a hashtag/substring.

Uses MarshalX/atproto SDK. Heavier than Jetstream (CBOR/CAR decode per commit);
use only if you need fields Jetstream drops.
"""

from atproto import CAR, FirehoseSubscribeReposClient, models, parse_subscribe_repos_message

NEEDLE = "#tucson"


def on_message(message) -> None:
    commit = parse_subscribe_repos_message(message)
    if not isinstance(commit, models.ComAtprotoSyncSubscribeRepos.Commit):
        return
    if not commit.blocks:
        return
    car = CAR.from_bytes(commit.blocks)
    for op in commit.ops:
        if op.action != "create" or not op.cid:
            continue
        record = car.blocks.get(op.cid)
        if not record or record.get("$type") != "app.bsky.feed.post":
            continue
        text = (record.get("text") or "").lower()
        if NEEDLE not in text:
            continue
        rkey = op.path.split("/", 1)[-1]
        url = f"https://bsky.app/profile/{commit.repo}/post/{rkey}"
        print(f"{url}  ::  {record.get('text')}")


if __name__ == "__main__":
    FirehoseSubscribeReposClient().start(on_message)
