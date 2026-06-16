# Integrity (bonus): the receipt cannot be forged

Flipping a single byte of the receipt's `replay_hash` and re-verifying yields:

    verifier_action: tampered
    reasons: ['replay_hash_mismatch', 'recomputed=03279372ae2be968... envelope=fc279372ae2be968...']

The verifier recomputes the hash over the canonical inputs; any change → `tampered`.
So the no-bind receipt is integrity-sealed, not a free-text claim.
