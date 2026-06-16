# Governance Proof Scenario

The system was asked to perform an action requiring authority `write`+`merge`.

The actor (`agent.demo`) possessed only `read`.

Expected result: action refused **before binding**.

Governance mechanism tested:
- authority gate (policy deny)
- route binding gate (no-bind on refuse)
- evidence requirement (the deeper gate revealed under changed conditions)
- policy version: `governance-policy-v1` (sha256:a2fb6c01b87cdfa6a67f9c3889315129ba5e410a259bd24f254cd1f1720305ea)
