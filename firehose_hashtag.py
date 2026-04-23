"""Stream the raw AT Proto repo firehose and print posts matching a hashtag/substring.

Uses MarshalX/atproto SDK. Heavier than Jetstream (CBOR/CAR decode per commit);
use only if you need fields Jetstream drops.
"""

import argparse

from atproto import CAR, FirehoseSubscribeReposClient, models, parse_subscribe_repos_message


def make_handler(needle: str):
    needle_lower = needle.lower()

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
            text = record.get("text") or ""
            if needle_lower not in text.lower():
                continue
            rkey = op.path.split("/", 1)[-1]
            url = f"https://bsky.app/profile/{commit.repo}/post/{rkey}"
            print(f"{url}  ::  {text}")

    return on_message


def main() -> None:
    p = argparse.ArgumentParser(description="Tail the raw atproto firehose, filter posts by substring.")
    p.add_argument(
        "--needle",
        default="Tucson",
        help="case-insensitive substring to match in post text (default: Tucson)",
    )
    args = p.parse_args()
    FirehoseSubscribeReposClient().start(make_handler(args.needle))


if __name__ == "__main__":
    main()
