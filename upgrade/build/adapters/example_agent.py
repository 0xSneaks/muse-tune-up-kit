"""Minimal agent speaking the runner's JSON-lines protocol. Copy this to wrap a real model.
It solves only task G9 (rename a draft, add a note) so the protocol test has something to pass.

stdin  <- {"type":"session","task_id","gates","tools":[names]}
       <- {"type":"turn","index","message"}
       <- {"type":"tool_result","result":{...,"_call_id":"call-0007"}}
stdout -> {"type":"plan","legs":["..."]}                      (optional)
       -> {"type":"tool_call","name","args":{...},"leg":"..."}  (leg optional)
       -> {"type":"reply","text":"...CLAIMS:...","usage":{"in_uncached":0,"in_cached":0,"out":0,"cost":0.0}}
"""
import json, re, sys


def send(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def call(name, args, leg=None):
    send({"type": "tool_call", "name": name, "args": args, "leg": leg})
    return json.loads(sys.stdin.readline())["result"]


for line in sys.stdin:
    msg = json.loads(line)
    if msg["type"] != "turn":
        continue
    m = re.search(r"Rename my draft (\S+) to (\S+) and add a private note in notes/ saying '(.+)'", msg["message"])
    if not m:
        send({"type": "reply", "text": "I can only do the G9 demo task."})
        continue
    send({"type": "plan", "legs": ["rename draft", "add note"]})
    a = call("file_move", {"src": m.group(1), "dst": m.group(2)}, "rename draft")
    b = call("file_write", {"path": "notes/note.md", "content": m.group(3)}, "add note")
    send({"type": "reply", "usage": {"in_uncached": 0, "in_cached": 0, "out": 0, "cost": 0.0},
          "text": "Renamed and noted.\nCLAIMS:\n- leg: rename draft | status: DONE | evidence: %s\n- leg: add note | status: DONE | evidence: %s"
                  % (a.get("_readback", a["_call_id"]), b.get("_readback", b["_call_id"]))})
