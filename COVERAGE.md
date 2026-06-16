# Coverage matrix

Not a single refusal — every governed outcome, including a **positive case that actually binds**.
Each case ships a `receipt.json` + `canonical-inputs.json`; `verify.py` re-anchors the hashes and
re-derives every decision independently. Reproduce: `python3 verify.py`.

| Case | Decision | Failure class | Bound? | Verifier verdict |
|---|---|---|---|---|
| [`01-authority-failure`](cases/01-authority-failure) | refused | `authority_failure` | no | reject |
| [`02-policy-failure`](cases/02-policy-failure) | escalated | `policy_failure` | no | escalate |
| [`03-evidence-failure`](cases/03-evidence-failure) | refused | `evidence_failure` | no | reject |
| [`04-scope-failure`](cases/04-scope-failure) | refused | `scope_failure` | no | reject |
| [`05-state-failure`](cases/05-state-failure) | stale | `state_failure` | no | **stale (verifier overrides the envelope)** |
| [`06-positive-allow`](cases/06-positive-allow) | allowed | — | **yes — binds & executes** | execute |

Two things worth noting:
- **Case 06 is the positive control.** A legitimately authorized action is *allowed* and *binds*
  (`binding_state: bound`, `execution_state: executed`). The system is not a "no machine".
- **Case 05 answers the "circular verdict" critique.** The oracle's envelope said `allow`, but the
  verifier independently caught the **expired state** and refused (`stale`) — so the verdict is not
  the engine reading itself back; the verifier overrides on its own checks.
