# Verification — how to read this packet

This packet is the **evidence output** of one governed refusal, produced by the SignalBrain Core
governance engine — a deterministic CPU decision engine (no GPU, network, or services). The
engine source is **not** included in this public packet; what is published is the route-complete
evidence trail it emitted.

The integrity spine is the receipt's **`replay_hash`**: a sha256 seal over the canonical decision
inputs. Identical inputs produce a byte-identical receipt — which is exactly why `replay.same.log`
reports `Receipt hash match: true` and `Execution occurred: false`. The seal is what makes the
refusal auditable rather than asserted.

## What each artifact proves (the standard, route-complete)
| Standard element | Artifact |
|---|---|
| attempted action recorded | `input.request.json` |
| governance check before execution | `route.trace.json` (`evaluated_before_execution: true`) |
| explicit failure condition | `refusal.receipt.json` `failure_class` |
| refused before binding | `binding_state: not_bound`, `execution_state: not_executed` |
| no-bind receipt emitted | `refusal.receipt.json` (`receipt_type: no_bind_refusal`) |
| replays under same conditions | `replay.same.log` (`Receipt hash match: true`) |
| behaves predictably when condition supplied | `replay.changed-condition.log` |
| consequence prevented identified | `prevented-consequence.md` |

## Honest scope
- The five-mode failure taxonomy (authority / scope / evidence / policy / state) is a **mapping**
  onto the engine's internal fail-reason codes (e.g. policy-deny → authority, no-candidates →
  evidence, ttl-expired → state). It is not a separate five-bucket schema using those literal words.
- This packet is the evidence trail, not a runnable bundle: the engine that produced it is private.
  Independent reproduction against the engine is available on request.
- The same refuse-before-bind discipline also runs in the live system (a pre-execution answer
  governor and a mutation gate) with a signed lineage ledger; those add a live consequence (a
  blocked answer, an un-written file) but require a running service, so they are referenced here,
  not inlined.

## Independent verification (no engine)
`verify.py` (Python stdlib only — **not** the decision engine) checks the published packet:
1. **Hash anchoring** — recomputes `input_hash`/`policy_hash` from each case's published
   `canonical-inputs.json` (`packed_hex`). The hashes are no longer self-asserted: sha256 the
   published bytes yourself and they match the receipt.
2. **Decision re-derivation** — re-derives each decision from the published policy via a
   documented rule, independent of the engine's envelope (de-circularises the verdict; see
   case 05 where the verifier *overrides* an `allow`).
3. **Tamper detection** — verifies every file against `SHA256SUMS`; one changed byte → non-zero exit.

Run it: `python3 verify.py`. It runs in CI on every push/PR and daily
(`.github/workflows/verify.yml`), so tampering is caught continuously, not by hand.

## External anchor — scope + upgrade
The committed tree carries a timestamped, third-party-attested record (the GitHub commit) and a
`SHA256SUMS` manifest enforced in CI. A cryptographic transparency-log anchor is the recommended
upgrade and is a single operator step (requires a key / Sigstore tooling not present in this
generator):
```
cosign sign-blob --yes SHA256SUMS          # logs the manifest hash to the Rekor transparency log
# or: gpg --armor --detach-sign SHA256SUMS  # detached signature with the maintainer key
```
