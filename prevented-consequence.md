# Prevented consequence

Had governance not refused before binding, the would-have-bound path was:

    merge repo/example#123  →  irreversible repository state change

The actor `agent.demo` held only `read` authority; the route required `write`+`merge`.
The oracle returned DECISION_REJECT (failure_class=authority_failure) BEFORE execution,
so `binding_state=not_bound` and `execution_state=not_executed`. The unauthorized merge
**never formed**. This is the consequence prevented — named, not implied.
