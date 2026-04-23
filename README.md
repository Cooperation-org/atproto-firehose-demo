# atproto-firehose-demo

Python intro to the AT Protocol firehose. Stream Bluesky posts, filter for what you care about (e.g. `#Tucson`), print matches.

## New to ATProto?

- [The AT Protocol — original Bluesky announcement](https://bsky.social/about/blog/10-18-2022-the-at-protocol) — Oct 2022, originally at blueskyweb.xyz
- [atproto.com](https://atproto.com/) — the protocol site
- [AT Protocol overview (Bluesky docs)](https://docs.bsky.app/docs/advanced-guides/atproto) — covers PDS, Relay, AppView
- [AT Protocol on Wikipedia](https://en.wikipedia.org/wiki/AT_Protocol)

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python jetstream_hashtag.py                      # default needle: Tucson
python jetstream_hashtag.py --needle "#Phoenix"  # any case-insensitive substring
```

Prints `https://bsky.app/profile/<did>/post/<rkey>  ::  <text>` per match. Pass `--needle` to filter for something else.

## The two scripts

- **`jetstream_hashtag.py`** — [Jetstream](https://docs.bsky.app/blog/jetstream): JSON over WebSocket. Start here.
- **`firehose_hashtag.py`** — raw firehose (CBOR + CAR) via [MarshalX/atproto](https://github.com/MarshalX/atproto). Use when you need signatures or fields Jetstream drops.

Neither stream supports server-side hashtag filtering. Jetstream filters server-side by collection and DID; hashtag match is in Python.

## Further reading

- [Dave Peck — Jetstream in a few lines of Python](https://davepeck.org/notes/bluesky/blueskys-jetstream-with-just-a-few-lines-of-python/)
- [Jaz — Shrinking the firehose by >99%](https://jazco.dev/2024/09/24/jetstream/)

## Making your own feed

You do **not** need to run an AppView. A custom feed is a separate service (a **Feed Generator**) that implements one RPC, `getFeedSkeleton`, returning a list of post URIs. Bluesky's AppView calls your generator and hydrates the posts for clients.

- [Custom Feeds docs](https://docs.bsky.app/docs/starter-templates/custom-feeds)
- [MarshalX/bluesky-feed-generator](https://github.com/MarshalX/bluesky-feed-generator) — Python template
- [bluesky-social/feed-generator](https://github.com/bluesky-social/feed-generator) — official TypeScript starter
- [Graze](https://www.graze.social/) — no-code feed builder

## What people build on ATProto

- **Custom feeds** — location (`#Tucson`), topic, community, ML-ranked
- **Bots** — mention-driven RAG, auto-posters
- **Labelers** — moderation and custom content labels
- **Cross-posting bridges** — Ghost, RSS, Mastodon ↔ Bluesky
- **Analytics** — lexicon usage, keyword and topic trends
- **Custom lexicons** — define your own record types, others can index them
- **Run your own PDS** — self-host identity and data
- **Third-party relay or AppView** — community-run implementations

## Beyond Bluesky

- [atproto-app-builder](https://github.com/YetAnotherJonWilson/atproto-app-builder) — TypeScript starter for atproto apps
- [LexiStats](https://lexistats.linkedtrust.us/) — live stats on which ATProto lexicons are actually in use
- [Blacksky](https://github.com/blacksky-algorithms) / [rsky](https://github.com/blacksky-algorithms/rsky) — community-run Rust atproto stack (relay, PDS, AppView), **fully independent** of Bluesky's infrastructure. Stayed up during Bluesky's April 2026 DDoS outage and saw a spike in user migrations ([TechCrunch](https://techcrunch.com/2026/04/17/its-not-just-you-bluesky-is-sorta-down/)). Relay at `atproto.africa`.

## ATProto work in Cooperation-org

- [lexistats](https://github.com/Cooperation-org/lexistats) / [lexistats-api](https://github.com/Cooperation-org/lexistats-api)
- [claim-atproto](https://github.com/Cooperation-org/claim-atproto), [claim-lexicon](https://github.com/Cooperation-org/claim-lexicon)
- [atmosphere-bot](https://github.com/Cooperation-org/atmosphere-bot)
- [ghost-atproto](https://github.com/Cooperation-org/ghost-atproto)
