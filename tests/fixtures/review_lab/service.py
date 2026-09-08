"""Synthetic review fixture. No network, credentials, persistence or third-party code."""
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    tenant: str


DOCUMENTS = {
    "a": {"tenant": "alpha", "body": "ALPHA_SYNTHETIC"},
    "b": {"tenant": "beta", "body": "BETA_SYNTHETIC"},
}


def get_document(user, document_id):
    doc = DOCUMENTS[document_id]
    if doc["tenant"] != user.tenant:
        raise PermissionError("document denied")
    return doc["body"]


def queue_export(user, document_id, queue):
    if not user.id:
        raise PermissionError("login required")
    job = {"actor": user.id, "document_id": document_id}
    queue.append(job)
    return len(queue)


def run_export(job):
    return DOCUMENTS[job["document_id"]]["body"]


def cached_search(user, query, cache):
    if query not in cache:
        cache[query] = [doc["body"] for doc in DOCUMENTS.values()
                        if doc["tenant"] == user.tenant and query in doc["body"]]
    return cache[query]


def approve(action, approvals):
    approvals.add(action["id"])


def invoke(action, approvals, effects):
    if action["id"] not in approvals:
        raise PermissionError("approval required")
    effects.append((action["recipient"], action["body"]))
    return "simulated"
