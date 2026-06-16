<p align="center">
  <img src="assets/banner.svg" alt="Governance Proof — route-complete no-bind evidence" width="900">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/governance-route--complete-34d399?style=for-the-badge" alt="route-complete">
  <img src="https://img.shields.io/badge/receipt-no--bind-22d3ee?style=for-the-badge" alt="no-bind receipt">
  <img src="https://img.shields.io/badge/replay-deterministic-34d399?style=for-the-badge" alt="deterministic replay">
  <img src="https://img.shields.io/badge/receipt-tamper--evident-22d3ee?style=for-the-badge" alt="tamper-evident">
</p>

<h3 align="center">An invalid action stopped <em>before it binds</em> — with a no-bind receipt and a deterministic replay trail.</h3>

<p align="center"><strong>The receipt is the proof. The replay is the audit. The prevented consequence is the governance.</strong></p>

---

## The route, end to end

```mermaid
flowchart LR
    A["📥 Attempted action<br/><code>merge_pull_request</code><br/>authority: read"] --> B{"🛡️ Pre-execution<br/>governance check"}
    B -- "authority &lt; required<br/>[write, merge]" --> C["⛔ REFUSED<br/>before binding"]
    C --> D[("🧾 No-bind receipt<br/>not_bound · not_executed<br/>replay_hash sealed")]
    C --> G["🚫 Prevented consequence<br/><code>unauthorized_repository_merge</code><br/>never formed"]
    D --> E["🔁 Replay · same conditions<br/>byte-identical refusal"]
    D --> F["🔁 Replay · authority granted<br/>→ deeper <b>evidence</b> gate refuses"]

    classDef stop fill:#1b1020,stroke:#f87171,color:#fecaca;
    classDef seal fill:#0b1f1a,stroke:#34d399,color:#a7f3d0;
    classDef gate fill:#0b1626,stroke:#22d3ee,color:#a5f3fc;
    classDef act fill:#10182b,stroke:#475569,color:#cbd5e1;
    class A act; class B gate; class C,G stop; class D,E,F seal;
```

## What each artifact proves

| The standard | Artifact | What it shows |
|---|---|---|
| 📥 attempted action recorded | [`input.request.json`](input.request.json) | the request, declared vs required authority |
| 🛡️ check **before** execution | [`route.trace.json`](route.trace.json) | `evaluated_before_execution: true` |
| ⚠️ explicit failure condition | [`refusal.receipt.json`](refusal.receipt.json) | `failure_class: authority_failure` |
| ⛔ refused **before binding** | [`refusal.receipt.json`](refusal.receipt.json) | `binding_state: not_bound`, `execution_state: not_executed` |
| 🧾 **no-bind receipt** | [`refusal.receipt.json`](refusal.receipt.json) | `receipt_type: no_bind_refusal`, sha256 `replay_hash` |
| 🔁 replays — same conditions | [`replay.same.log`](replay.same.log) | `Receipt hash match: true` |
| 🔁 replays — changed condition | [`replay.changed-condition.log`](replay.changed-condition.log) | authority granted → the **evidence** gate refuses |
| 🚫 consequence prevented | [`prevented-consequence.md`](prevented-consequence.md) | `unauthorized_repository_merge` never formed |
| 🔏 receipt is sealed | [`integrity.md`](integrity.md) | tamper one byte → verifier reports `tampered` |

## The case

An actor (`agent.demo`) requested `merge_pull_request` holding only `read` authority; the route
required `write` + `merge`. The governance check ran **before execution** and refused — nothing
bound, nothing executed. Replayed under identical conditions: byte-identical refusal. Replayed
with the missing authority **granted**: that gate clears and the **next** gate (evidence) refuses —
proving the refusal is *conditional and governed*, **not a hardcoded "no"**.

The `replay_hash` is a sha256 seal over the canonical decision inputs — identical inputs yield a
byte-identical receipt, which is why [`replay.same.log`](replay.same.log) reports
`Receipt hash match: true`. See [`verification.md`](verification.md) for how to read the packet
and the honest scope of the claim.

---

<p align="center">
  <img src="assets/logo.svg" alt="No-bind seal" width="76"><br>
  <sub>A warning is not proof. A receipt is. — <a href="verification.md">verification.md</a></sub>
</p>
