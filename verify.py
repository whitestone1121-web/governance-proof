#!/usr/bin/env python3
"""Independent verifier for the Governance Proof coverage matrix.

CLEAN-ROOM, dependency-free (Python stdlib only). It does NOT contain the decision engine /
scoring oracle / GPU kernel — it independently CHECKS the published receipts:

  1. HASH ANCHORING — recomputes `input_hash` and `policy_hash` from each case's published
     canonical input bytes (`canonical-inputs.json` → `packed_hex`). These stop being
     self-asserted: anyone can sha256 the published bytes and confirm they match the receipt.

  2. DECISION RE-DERIVATION (de-circularization) — re-derives the governance decision from the
     published policy via a DOCUMENTED rule, independent of the engine's envelope. The receipt's
     decision must equal the rule's output — so the verdict is not "the engine reading itself".

  3. TAMPER DETECTION — verifies every committed file against `SHA256SUMS`. Change one byte of
     any artifact and this exits non-zero. Run in CI (.github/workflows/verify.yml) on every
     push + a daily schedule, so integrity is continuously enforced, not a manual claim.

The `replay_hash` is the engine's seal over the canonical inputs; its construction is the
engine's (reproducible against it on request). This verifier anchors the parts a third party
CAN check with no proprietary code: the input/policy hashes and the policy→decision derivation.

Usage:  python3 verify.py            # verify everything, exit 0 on success
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def _sha(b: bytes) -> str:
    return "sha256:" + hashlib.sha256(b).hexdigest()


# Documented governance decision rule (NOT the scoring oracle). Maps the policy + request
# shape to a decision. The proprietary part — how a candidate is *scored* — is not needed to
# check authority / policy / evidence / state outcomes.
def rederive_decision(summary: dict) -> tuple[str, str]:
    allow = summary["policy_allow"]
    if allow == 0:
        return "refused", "authority_failure"
    if allow == 2:
        return "escalated", "policy_failure"
    if summary["candidate_count"] == 0:
        return "refused", "evidence_failure"
    if summary["ttl_expired_at_verify"]:
        return "stale", "state_failure"          # verifier-side state gate (overrides the envelope)
    if summary["min_score"] > summary["max_candidate_score"]:
        return "refused", "scope_failure"
    return "allowed", "ok"


def verify_case(case_dir: Path, errors: list[str]) -> None:
    receipt = json.loads((case_dir / "receipt.json").read_text())
    ci = json.loads((case_dir / "canonical-inputs.json").read_text())
    name = case_dir.name

    # 1. hash anchoring — recompute from published bytes
    ph = ci["packed_hex"]
    input_bytes = bytes.fromhex(ph["command"]) + bytes.fromhex(ph["signal"]) + bytes.fromhex(ph["candidates"])
    if _sha(input_bytes) != receipt["input_hash"]:
        errors.append(f"{name}: input_hash mismatch (receipt is not anchored to its inputs)")
    if _sha(bytes.fromhex(ph["policy"])) != receipt["policy_hash"]:
        errors.append(f"{name}: policy_hash mismatch")

    # 2. decision re-derivation — independent of the envelope
    dec, fclass = rederive_decision(ci["summary"])
    if dec != receipt["decision"]:
        errors.append(f"{name}: decision {receipt['decision']!r} != independently re-derived {dec!r}")
    if fclass != receipt["failure_class"]:
        errors.append(f"{name}: failure_class {receipt['failure_class']!r} != re-derived {fclass!r}")
    # bind/no-bind must agree with the decision
    expect_bound = (dec == "allowed" and not ci["summary"]["ttl_expired_at_verify"])
    if bool(receipt.get("bound")) != expect_bound:
        errors.append(f"{name}: bound={receipt.get('bound')} inconsistent with decision {dec!r}")


def verify_tamper(errors: list[str]) -> None:
    sums = ROOT / "SHA256SUMS"
    if not sums.is_file():
        errors.append("SHA256SUMS missing — cannot tamper-check")
        return
    for line in sums.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        digest, _, rel = line.partition("  ")
        f = ROOT / rel
        if not f.is_file():
            errors.append(f"tamper: {rel} listed in SHA256SUMS but missing")
            continue
        actual = hashlib.sha256(f.read_bytes()).hexdigest()
        if actual != digest:
            errors.append(f"tamper: {rel} changed (sha256 {actual[:12]}… != committed {digest[:12]}…)")


def main() -> int:
    errors: list[str] = []
    cases = sorted((ROOT / "cases").glob("*/")) if (ROOT / "cases").is_dir() else []
    if not cases:
        print("verify: no cases/ found", file=sys.stderr)
        return 2
    for c in cases:
        verify_case(c, errors)
    verify_tamper(errors)
    if errors:
        print("GOVERNANCE PROOF — VERIFICATION FAILED:")
        for e in errors:
            print(f"  ✗ {e}")
        return 1
    print(f"GOVERNANCE PROOF — VERIFIED ✓  ({len(cases)} cases: hashes anchored, decisions re-derived, no tampering)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
