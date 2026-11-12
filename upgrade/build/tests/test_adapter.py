"""Adapter mock test: adapters/muse_agent.py is driven over the runner's JSON-lines
protocol with a FAKE `claude` shim on PATH — the live model is never invoked.
The shim answers the first invocation with a harness tool_call line and the
second (after the tool result is in the transcript) with a final reply, so the
test proves: standing context reaches the CLI's system prompt, tool calls are
forwarded and results fed back, and usage is summed across invocations."""
import json, os, select, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ADAPTER = os.path.join(HERE, "..", "adapters", "muse_agent.py")
MARKER = "STANDING-CONTEXT-MARKER-7f3a"

SHIM = '''#!/usr/bin/env python3
import json, os, sys
args = sys.argv[1:]
prompt = args[-1]
sp = args[args.index("--system-prompt-file") + 1]
ctx = open(sp).read()
assert "%s" in ctx, "standing context did not reach the system prompt"
assert "CLAIMS" in ctx and "file_list" in ctx, "run instruction / tool names missing"
if "TOOL RESULT" in prompt:
    out = {"result": "Done. The list came back.\\nCLAIMS:\\n- leg: look | status: DONE | evidence: call-0001",
           "usage": {"input_tokens": 50, "output_tokens": 7, "cache_read_input_tokens": 10},
           "total_cost_usd": 0.002}
else:
    out = {"result": json.dumps({"tool_call": {"name": "file_list", "args": {"prefix": ""}, "leg": "look"}}),
           "usage": {"input_tokens": 100, "output_tokens": 5},
           "total_cost_usd": 0.001}
print(json.dumps(out))
''' % MARKER


def readline(proc, timeout=30):
    r, _, _ = select.select([proc.stdout], [], [], timeout)
    if not r:
        raise AssertionError("adapter produced no line in time")
    line = proc.stdout.readline()
    if not line:
        raise AssertionError("adapter process ended early")
    return json.loads(line)


class Adapter(unittest.TestCase):
    def test_mock_claude_round_trip(self):
        with tempfile.TemporaryDirectory() as d:
            shim = os.path.join(d, "claude")
            with open(shim, "w") as f:
                f.write(SHIM)
            os.chmod(shim, 0o755)
            standing = os.path.join(d, "standing.md")
            with open(standing, "w") as f:
                f.write(f"# fake standing file\n{MARKER}\n")
            env = {**os.environ, "MUSE_AGENT_CLAUDE": shim, "MUSE_AGENT_STANDING_FILES": standing}
            proc = subprocess.Popen([sys.executable, ADAPTER], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, text=True, env=env)
            try:
                def send(obj):
                    proc.stdin.write(json.dumps(obj) + "\n")
                    proc.stdin.flush()

                send({"type": "session", "task_id": "MOCK", "gates": False, "tools": ["file_list", "file_read"]})
                send({"type": "turn", "index": 0, "message": "List the files."})
                call = readline(proc)
                self.assertEqual(call["type"], "tool_call")
                self.assertEqual(call["name"], "file_list")
                self.assertEqual(call["leg"], "look")
                send({"type": "tool_result", "result": {"paths": ["a.md"], "_call_id": "call-0001"}})
                reply = readline(proc)
                self.assertEqual(reply["type"], "reply")
                self.assertIn("Done. The list came back.", reply["text"])
                self.assertIn("CLAIMS:", reply["text"])
                self.assertEqual(reply["usage"]["in_uncached"], 150)
                self.assertEqual(reply["usage"]["in_cached"], 10)
                self.assertEqual(reply["usage"]["out"], 12)
                self.assertAlmostEqual(reply["usage"]["cost"], 0.003)
            finally:
                proc.stdin.close()
                proc.wait(timeout=30)
            self.assertEqual(proc.returncode, 0)


if __name__ == "__main__":
    unittest.main()
