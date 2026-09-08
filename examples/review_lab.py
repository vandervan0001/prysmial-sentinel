"""Reproduce synthetic fixture behavior. Does not change the target or contact a service."""
import sys
sys.dont_write_bytecode = True
import hashlib
import copy
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "tests/fixtures/review_lab"
FILES = (ROOT / "README.md", ROOT / "service.py")
BEFORE = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
spec = importlib.util.spec_from_file_location("forward_fixture", ROOT / "service.py")
svc = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = svc
spec.loader.exec_module(svc)
alpha = svc.User("alice", "alpha")
beta = svc.User("bob", "beta")
results = []

def record(name, observed, expected, kind):
    passed = observed == expected
    results.append({"case": name, "kind": kind, "observed": copy.deepcopy(observed),
                    "expected_current_behavior": copy.deepcopy(expected), "passed": passed})
    if not passed:
        raise AssertionError(name)

def denial(call):
    try:
        call()
    except PermissionError as exc:
        return str(exc)
    return "DID_NOT_DENY"

record("direct_alpha_own", svc.get_document(alpha, "a"), "ALPHA_SYNTHETIC", "legitimate")
record("direct_beta_own", svc.get_document(beta, "b"), "BETA_SYNTHETIC", "legitimate")
record("direct_alpha_foreign_denied", denial(lambda: svc.get_document(alpha, "b")), "document denied", "denial-control")
record("direct_beta_foreign_denied", denial(lambda: svc.get_document(beta, "a")), "document denied", "denial-control")
queue = []
record("anonymous_export_denied", denial(lambda: svc.queue_export(svc.User("", "alpha"), "b", queue)), "login required", "denial-control")
record("denied_export_no_job", queue, [], "denial-control")
for user, document_id, expected, kind in (
    (alpha, "a", "ALPHA_SYNTHETIC", "legitimate"),
    (beta, "b", "BETA_SYNTHETIC", "legitimate"),
    (alpha, "b", "BETA_SYNTHETIC", "F1"),
    (beta, "a", "ALPHA_SYNTHETIC", "F1"),
):
    queue = []
    count = svc.queue_export(user, document_id, queue)
    record("export_" + user.tenant + "_" + document_id,
           {"queue_length": count, "job": dict(queue[0]), "body": svc.run_export(queue[0])},
           {"queue_length": 1, "job": {"actor": user.id, "document_id": document_id}, "body": expected}, kind)

for user, expected in ((alpha, "ALPHA_SYNTHETIC"), (beta, "BETA_SYNTHETIC")):
    record("fresh_search_" + user.tenant, svc.cached_search(user, "SYNTHETIC", {}), [expected], "legitimate")
for first, second, expected in ((alpha, beta, "ALPHA_SYNTHETIC"), (beta, alpha, "BETA_SYNTHETIC")):
    shared_cache = {}
    svc.cached_search(first, "SYNTHETIC", shared_cache)
    record("shared_search_" + first.tenant + "_then_" + second.tenant,
           svc.cached_search(second, "SYNTHETIC", shared_cache), [expected], "F2")
cache = {}
record("foreign_specific_query_fresh_denied", svc.cached_search(beta, "ALPHA", cache), [], "denial-control")
record("negative_cache_hides_authorized_result", svc.cached_search(alpha, "ALPHA", cache), [], "F2-variant")
record("authorized_specific_query_fresh", svc.cached_search(alpha, "ALPHA", {}), ["ALPHA_SYNTHETIC"], "legitimate")
cache = {}
svc.cached_search(alpha, "ALPHA", cache)
record("specific_query_cached_foreign_leak", svc.cached_search(beta, "ALPHA", cache), ["ALPHA_SYNTHETIC"], "F2-variant")

def action():
    return {"id": "approval-1", "recipient": "approved@example.invalid", "body": "APPROVED_SYNTHETIC"}

payload = action()
effects = []
record("unapproved_send_denied", denial(lambda: svc.invoke(payload, set(), effects)), "approval required", "denial-control")
record("denied_send_no_effect", effects, [], "denial-control")
approvals = set()
svc.approve(payload, approvals)
record("approved_send_result", svc.invoke(payload, approvals, effects), "simulated", "legitimate")
record("approved_send_effect", effects, [("approved@example.invalid", "APPROVED_SYNTHETIC")], "legitimate")

for field, replacement, expected in (
    ("recipient", "changed@example.invalid", ("changed@example.invalid", "APPROVED_SYNTHETIC")),
    ("body", "UNAPPROVED_SYNTHETIC", ("approved@example.invalid", "UNAPPROVED_SYNTHETIC")),
):
    payload = action()
    approvals, effects = set(), []
    svc.approve(payload, approvals)
    payload[field] = replacement
    svc.invoke(payload, approvals, effects)
    record("approved_action_changed_" + field, effects, [expected], "F3")

approvals, effects = set(), []
svc.approve(action(), approvals)
replacement = {"id": "approval-1", "recipient": "replacement@example.invalid", "body": "REPLACED_SYNTHETIC"}
svc.invoke(replacement, approvals, effects)
record("new_action_reuses_approved_id", effects, [("replacement@example.invalid", "REPLACED_SYNTHETIC")], "F3-variant")

approvals, effects = set(), []
payload = action()
svc.approve(payload, approvals)
svc.invoke(payload, approvals, effects)
svc.invoke(payload, approvals, effects)
record("repeat_identical_approved_action", effects,
       [("approved@example.invalid", "APPROVED_SYNTHETIC"), ("approved@example.invalid", "APPROVED_SYNTHETIC")],
       "needs-context-single-use-policy")
AFTER = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in FILES}
record("target_hashes_unchanged", AFTER, BEFORE, "integrity")
assert len(results) > 0
print(json.dumps({"executed_at": datetime.now(timezone.utc).isoformat(), "python": sys.version,
                  "target": "tests/fixtures/review_lab", "sha256": BEFORE, "case_count": len(results),
                  "passed": sum(r["passed"] for r in results), "failed": sum(not r["passed"] for r in results),
                  "meaning": "Passed means the recorded current behavior was reproduced; findings reproduce unsafe effects.",
                  "results": results}, indent=2))
