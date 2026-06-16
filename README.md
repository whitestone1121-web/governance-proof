# Governance Proof Packet — route-complete evidence

This is the evidence output of a **single governed refusal**: an invalid action stopped
**before it binds**, with a **no-bind receipt** and a **deterministic replay** trail. Not a
claim — the artifacts themselves.

**The receipt is the proof. The replay is the audit. The prevented consequence is the governance.**

## The case
An actor (`agent.demo`) requested `merge_pull_request` holding only `read` authority; the route
required `write` + `merge`. The governance check ran **before execution** and refused. Nothing
bound, nothing executed. The refusal was then replayed under identical conditions, and again with
the missing authority supplied.

## What each artifact proves (the standard, route-complete)
| Standard element | Artifact |
|---|---|
| attempted action recorded | `input.request.json` |
| governance check **before** execution | `route.trace.json` (`evaluated_before_execution: true`) |
| explicit failure condition | `refusal.receipt.json` → `failure_class` |
| refused **before binding** | `binding_state: not_bound`, `execution_state: not_executed` |
| no-bind receipt emitted | `refusal.receipt.json` (`receipt_type: no_bind_refusal`) |
| replays under same conditions | `replay.same.log` → `Receipt hash match: true` |
| predictable when condition supplied | `replay.changed-condition.log` → authority granted → the **deeper evidence gate** refuses |
| consequence prevented identified | `prevented-consequence.md` → `unauthorized_repository_merge` |
| (bonus) receipt is sealed | `integrity.md` → tamper → `tampered` |

The `replay_hash` in the receipt is a sha256 seal over the canonical decision inputs: identical
inputs yield a byte-identical receipt, which is why `replay.same.log` reports
`Receipt hash match: true`. The changed-condition log shows the refusal is **conditional and
governed** — supplying the missing authority clears that gate and exposes the next one — not a
hardcoded "no".

See `verification.md` for how to read the packet and the honest scope of the claim.
