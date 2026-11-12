"""Append-only JSONL state that survives a process kill or VM replacement.
Every append is flushed and fsynced before the caller continues."""
import hashlib, json, os


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, default=str).encode()).hexdigest()[:16]


class Store:
    def __init__(self, root):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def _p(self, name):
        return os.path.join(self.root, name)

    def append(self, name, rec):
        with open(self._p(name), "a") as f:
            f.write(json.dumps(rec, sort_keys=True, default=str) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def read(self, name):
        if not os.path.exists(self._p(name)):
            return []
        with open(self._p(name)) as f:
            return [json.loads(line) for line in f if line.strip()]
