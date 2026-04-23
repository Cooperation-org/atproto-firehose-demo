# atproto-firehose-demo

Small runnable samples for drinking from the AT Protocol / Bluesky firehose in Python and filtering for local posts (e.g. `#Tucson`). Lives under [Cooperation-org](https://github.com/Cooperation-org) (Linked Trust).

Two approaches:

| File | Transport | Deps | When to use |
|---|---|---|---|
| `jetstream_hashtag.py` | Jetstream WS (JSON) | `websockets` | Default. Simpler, ~99% smaller payload, no CBOR/CAR. |
| `firehose_hashtag.py` | Raw repo firehose (CBOR/CAR) | `atproto` | You need fields Jetstream drops, or you want the canonical stream. |

## Run

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python jetstream_hashtag.py        # recommended
python firehose_hashtag.py         # raw firehose via atproto SDK
```

Both print matches like:

```
https://bsky.app/profile/<did>/post/<rkey>  ::  <post text>
```

Change the `NEEDLE` constant at the top of either file to filter for a different hashtag / substring.

## How filtering works

- **Server-side** (Jetstream): you can filter by `wantedCollections` (e.g. only posts) and `wantedDids`. **You cannot filter by hashtag server-side** — see discussion linked below.
- **Client-side**: match `record.text` (substring) or walk `record.facets[*].features[*]` for `app.bsky.richtext.facet#tag` entries (strict hashtag-only match).

The samples here do substring match on text (catches `#Tucson`, `#TucsonAZ`, `Tucson` mentions without `#`, etc). Swap to facet-walking if you want strict hashtags only.

## Best resources

### Official / canonical
- [Bluesky firehose docs](https://docs.bsky.app/docs/advanced-guides/firehose)
- [Introducing Jetstream (blog)](https://docs.bsky.app/blog/jetstream)
- [bluesky-social/jetstream (server)](https://github.com/bluesky-social/jetstream)
- [Jaz's writeup — Shrinking the firehose by >99%](https://jazco.dev/2024/09/24/jetstream/)

### Python SDKs
- [MarshalX/atproto (PyPI: `atproto`)](https://github.com/MarshalX/atproto) — full AT Proto SDK, includes `FirehoseSubscribeReposClient`
- [atproto.blue firehose docs](https://atproto.blue/en/latest/atproto_firehose/index.html)
- [MarshalX/atproto firehose examples](https://github.com/MarshalX/atproto/tree/main/examples/firehose)
- [kcchu/atproto-firehose](https://github.com/kcchu/atproto-firehose) — alternate, lighter firehose client

### Walkthroughs worth sharing with devs
- [Dave Peck — Jetstream in a few lines of Python](https://davepeck.org/notes/bluesky/blueskys-jetstream-with-just-a-few-lines-of-python/)
- [Dave Peck — Decoding the firehose with zero Python deps](https://davepeck.org/notes/bluesky/decoding-the-bluesky-firehose-with-zero-python-dependencies/)
- [anderegg.ca — Playing with the Bluesky firehose](https://anderegg.ca/2024/11/25/playing-with-the-bluesky-firehose)
- [Jake Lazaroff — Drinking from the Bluesky firehose](https://jakelazaroff.com/words/drinking-from-the-bluesky-firehose/)
- [Parker Higgins — Realtime Bluesky events with Jetstream](https://parkerhiggins.net/2025/04/realtime-bluesky-events-jetstream-for-helping-friendly-bot/)

### Background
- [Server-side firehose filtering discussion (#2418)](https://github.com/bluesky-social/atproto/discussions/2418)

## Related repos in Cooperation-org

ATProto / Bluesky work already happening in this org (verified via each repo's description or README):

- **[lexistats](https://github.com/Cooperation-org/lexistats)** — Usage of Lexicons on ATProto
- **[lexistats-api](https://github.com/Cooperation-org/lexistats-api)** — LexiStats API: ATProto lexicon usage stats, live feed, and lexicon chooser ([lexistats.linkedtrust.us](https://lexistats.linkedtrust.us))
- **[claim-atproto](https://github.com/Cooperation-org/claim-atproto)** — LinkedClaims over ATProto
- **[claim-lexicon](https://github.com/Cooperation-org/claim-lexicon)** — Minimal ATProto lexicon for verifiable claims (LinkedClaims spec)
- **[atmosphere-bot](https://github.com/Cooperation-org/atmosphere-bot)** — *Ameboh*: Bluesky RAG bot for ATmosphere Conf 2026 ([@ameboh.bsky.social](https://bsky.app/profile/ameboh.bsky.social))
- **[ghost-atproto](https://github.com/Cooperation-org/ghost-atproto)** — Ghost ↔ Bluesky integration
- **[ghost-atproto-standard-site-guide](https://github.com/Cooperation-org/ghost-atproto-standard-site-guide)** — Guide for the above


## Jetstream endpoints

Public instances (pick nearest):

- `wss://jetstream1.us-east.bsky.network/subscribe`
- `wss://jetstream2.us-east.bsky.network/subscribe`
- `wss://jetstream1.us-west.bsky.network/subscribe`
- `wss://jetstream2.us-west.bsky.network/subscribe`

Query params of interest: `wantedCollections`, `wantedDids`, `cursor`, `compress`.
