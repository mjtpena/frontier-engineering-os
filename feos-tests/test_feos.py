import json, os, subprocess, sys
from pathlib import Path
import yaml
from conftest import run

def test_framework_self_check(repo):
    r = run(repo, "scripts/feos_validate.py"); assert r.returncode == 0, r.stdout

def test_adapters_in_sync(repo):
    r = run(repo, "scripts/feos_render.py", "--check"); assert r.returncode == 0, r.stdout

def test_adapter_drift_detected(repo):
    p = repo / ".claude/agents/feos-builder.md"; p.write_text(p.read_text() + "\nextra")
    assert run(repo, "scripts/feos_render.py", "--check").returncode == 1

def test_readonly_agent_with_write_tool_rejected(repo):
    m = repo / "feos/orchestration/agents.manifest.yaml"; d = yaml.safe_load(m.read_text())
    for a in d["agents"]:
        if a["id"] == "reviewer": a["claude"]["tools"] += ", Write"
    m.write_text(yaml.safe_dump(d, sort_keys=False))
    r = run(repo, "scripts/feos_validate.py"); assert r.returncode == 1 and "read-only agent reviewer" in r.stdout

def test_gate_without_human_rejected(repo):
    g = repo / "feos/orchestration/gates/G1-requirements.yaml"; d = yaml.safe_load(g.read_text())
    d["checks"] = [c for c in d["checks"] if c["type"] != "human"]; g.write_text(yaml.safe_dump(d))
    r = run(repo, "scripts/feos_validate.py"); assert r.returncode == 1 and "human check" in r.stdout

def test_backlog_valid(repo):
    r = run(repo, "scripts/feos_validate.py", "--backlog", "plan/backlog.yaml"); assert r.returncode == 0, r.stdout

def test_backlog_cycle_and_oversize(repo):
    p = repo / "plan/backlog.yaml"; d = yaml.safe_load(p.read_text())
    d["tasks"][0]["depends_on"] = ["TK-002"]
    p.write_text(yaml.safe_dump(d)); r = run(repo, "scripts/feos_validate.py", "--backlog", "plan/backlog.yaml")
    assert r.returncode == 1 and "cycle" in r.stdout
    d["tasks"][0]["depends_on"] = []; d["tasks"][0]["estimate_hours"] = 12
    p.write_text(yaml.safe_dump(d)); r = run(repo, "scripts/feos_validate.py", "--backlog", "plan/backlog.yaml")
    assert r.returncode == 1 and "estimate_hours" in r.stdout

def test_trace_all_stages_pass(repo):
    r = run(repo, "scripts/feos_trace.py"); assert r.returncode == 0, r.stdout

def test_trace_detects_orphans(repo):
    p = repo / "specs/prd.md"; p.write_text(p.read_text() + "\n### FR-002 — Orphan\n- **Traces:** \n")
    r = run(repo, "scripts/feos_trace.py", "--stage", "requirements"); assert r.returncode == 1 and "FR-002" in r.stdout
    r = run(repo, "scripts/feos_trace.py", "--stage", "tests"); assert "FR-002" in r.stdout

def test_artifacts_frontmatter(repo):
    assert run(repo, "scripts/feos_validate.py", "--artifacts", "specs").returncode == 0

def test_lint_flags_vague(repo):
    p = repo / "specs/prd.md"; p.write_text(p.read_text() + "\nThe UI shall be user-friendly and fast.\n")
    r = run(repo, "scripts/feos_lint_requirements.py", "specs/prd.md"); assert r.returncode == 1 and "user-friendly" in r.stdout

REVIEW = """```yaml
scores:
  correctness:     {score: 4, evidence: ["tests/test_balance.py:1"]}
  security:        {score: 4, evidence: ["scan.txt"]}
  maintainability: {score: 3, evidence: ["src/a.py"]}
  performance:     {score: 3, evidence: ["k6.txt"]}
  observability:   {score: 3, evidence: ["src/a.py:10"]}
  documentation:   {score: 4, evidence: ["README.md"]}
  cost_efficiency: {score: 3, evidence: ["arch.md"]}
  accessibility:   {score: 4, evidence: [], na: true}
hard_constraints: {build: true, tests: true}
```"""

def test_score_pass_and_caps(repo):
    f = repo / "review.md"; f.write_text(REVIEW)
    r = run(repo, "scripts/feos_gate.py", "score", "review.md"); out = json.loads(r.stdout)
    assert r.returncode == 0 and out["score"] >= 85
    r = run(repo, "scripts/feos_gate.py", "score", "review.md", "--signals", "tests_failed")
    assert r.returncode == 1  # correctness capped to 0 → floor breach

def test_score_no_evidence_is_zero(repo):
    f = repo / "review.md"; f.write_text(REVIEW.replace('{score: 4, evidence: ["scan.txt"]}', '{score: 4, evidence: []}'))
    out = json.loads(run(repo, "scripts/feos_gate.py", "score", "review.md").stdout)
    assert out["dimensions"]["security"]["score"] == 0 and out["result"] == "fail"

def test_ai_eval_requires_human_approved_thresholds(repo):
    good = {"cases": 60, "metrics": {"groundedness": 4.5, "relevance": 4.4, "task_success_rate": 0.9, "safety_defect_rate": 0.0,
            "jailbreak_success_rate": 0.0, "abstention_correctness": 0.95}}
    good["slices"] = {s: dict(good["metrics"]) for s in ("adversarial", "out_of_scope", "fairness")}
    (repo / "e.json").write_text(json.dumps(good))
    r = run(repo, "scripts/feos_gate.py", "ai-eval", "e.json"); assert r.returncode == 1 and "not approved" in r.stdout
    q = repo / "feos/orchestration/evaluations/ai-quality.yaml"; q.write_text(q.read_text().replace("approved_by: TBD", "approved_by: Jane Citizen"))
    assert run(repo, "scripts/feos_gate.py", "ai-eval", "e.json").returncode == 0
    good["slices"]["fairness"]["groundedness"] = 3.1; (repo / "e.json").write_text(json.dumps(good))
    r = run(repo, "scripts/feos_gate.py", "ai-eval", "e.json"); assert r.returncode == 1 and "fairness" in r.stdout

REVIEW_G1 = """```yaml
scores:
  correctness:   {score: %d, evidence: ["specs/prd.md:10"]}
  documentation: {score: %d, evidence: ["specs/prd.md:1"]}
```"""
G1_AGENT = [{"id": "G1.4", "status": "pass", "evidence": ["evidence/gates/G1-review.md"]},
            {"id": "G1.5", "status": "pass", "evidence": ["evidence/gates/G1-review.md"]}]

def claims(repo, items): (repo / "c.json").write_text(json.dumps(items)); return "c.json"
def record(repo, *a): return run(repo, "scripts/feos_gate.py", "record", *a)
def gate_record(repo, r): return {c["id"]: c for c in json.loads((repo / json.loads(r.stdout)["evidence"]).read_text())["checks"]}
def decide(repo, decision, scope, outcome):
    run(repo, "scripts/feos_state.py", "escalate", "--decision", decision, "--scope", scope, "--summary", "s")
    assert run(repo, "scripts/feos_state.py", "resolve", "--decision", decision, "--scope", scope, "--by", "Jane", "--outcome", outcome).returncode == 0

def test_gate_record_runs_checks_and_reads_human_decisions(repo):
    assert run(repo, "scripts/feos_state.py", "init").returncode == 0
    (repo / "review.md").write_text(REVIEW_G1 % (4, 4))
    lies = [{"id": i, "status": "pass", "evidence": ["trust me"]} for i in ("G1.1", "G1.2", "G1.6")]
    args = ["--gate", "G1", "--scope", "specs", "--checks", claims(repo, G1_AGENT + lies), "--review", "review.md"]
    r = record(repo, *args); assert r.returncode == 2 and "pending_human" in r.stdout   # claimed human 'pass' is ignored
    by = gate_record(repo, r)
    assert by["G1.2"]["verified_by"] == "record" and any("-> exit 0" in e for e in by["G1.2"]["evidence"])
    assert by["G1.6"]["verified_by"] == "escalation" and by["G1.6"]["status"] == "pending"
    assert json.loads(r.stdout)["score"] == 100
    assert run(repo, "scripts/feos_state.py", "resolve", "--decision", "approve_requirements_G1", "--scope", "specs",
               "--by", "Jane", "--outcome", "approved").returncode == 1                  # nothing escalated yet
    decide(repo, "approve_requirements_G1", "specs", "approved")
    assert record(repo, *args).returncode == 0
    p = repo / "specs/prd.md"; p.write_text(p.read_text() + "\n### FR-002 — Orphan\n- **Traces:** \n")
    r = record(repo, *args)                                                              # failing command beats 'pass' and 100
    assert r.returncode == 1 and "G1.2" in json.loads(r.stdout)["failed_hard_checks"]

def test_gate_record_scores_from_review_and_needs_agent_evidence(repo):
    run(repo, "scripts/feos_state.py", "init"); decide(repo, "approve_requirements_G1", "specs", "approved")
    base = ["--gate", "G1", "--scope", "specs"]
    (repo / "review.md").write_text(REVIEW_G1 % (4, 4))
    r = record(repo, *base, "--checks", claims(repo, G1_AGENT)); assert r.returncode == 1 and "--review" in r.stdout
    (repo / "review.md").write_text(REVIEW_G1 % (2, 2))
    r = record(repo, *base, "--checks", claims(repo, G1_AGENT), "--review", "review.md")
    assert r.returncode == 1 and "score 50.0 < threshold 85" in r.stdout
    (repo / "review.md").write_text(REVIEW_G1 % (4, 4))
    r = record(repo, *base, "--checks", claims(repo, [{"id": "G1.4", "status": "pass"}, G1_AGENT[1]]), "--review", "review.md")
    assert r.returncode == 1 and "G1.4" in json.loads(r.stdout)["failed_hard_checks"]      # pass without evidence
    r = record(repo, *base, "--checks", claims(repo, G1_AGENT[1:]), "--review", "review.md")
    assert r.returncode == 1 and "G1.4" in json.loads(r.stdout)["failed_hard_checks"]      # missing agent result
    decide(repo, "approve_requirements_G1", "specs", "rejected")
    r = record(repo, *base, "--checks", claims(repo, G1_AGENT), "--review", "review.md")
    assert r.returncode == 1 and "G1.6" in json.loads(r.stdout)["failed_hard_checks"]      # latest decision wins

def test_gate_record_runs_project_commands_and_rejects_bad_scope(repo):
    py = sys.executable   # unquoted: a YAML value may not start with a quote and continue after it
    p = repo / "feos/instructions/30-project/project.md"; t = p.read_text()
    for old, new in (("build:   python -m compileall -q scripts", f'build: {py} -c "raise SystemExit(1)"'),
                     ("lint:    python scripts/feos_validate.py && python scripts/feos_render.py --check", "lint: none"),
                     ("test:    python -m pytest -q feos-tests", "test: TBD(owner, which runner?)")):
        assert old in t; t = t.replace(old, new)
    t = t.replace(t[t.index("coverage: "):t.index("\n", t.index("coverage: "))], f'coverage: {py} -c "print({{min_coverage}})"')
    p.write_text(t); run(repo, "scripts/feos_state.py", "init")
    (repo / "review.md").write_text(REVIEW)
    lies = [{"id": f"G3.{i}", "status": "pass", "evidence": ["ok"]} for i in range(1, 9)]
    r = record(repo, "--gate", "G3", "--scope", "TK-002", "--checks", claims(repo, lies), "--review", "review.md")
    assert r.returncode == 1
    by = gate_record(repo, r)
    assert by["G3.1"]["status"] == "fail" and "-> exit 1" in by["G3.1"]["evidence"][0]
    assert by["G3.2"]["status"] == "pass" and "'none'" in by["G3.2"]["evidence"][0]
    assert by["G3.3"]["status"] == "fail" and "not configured" in by["G3.3"]["evidence"][0]
    assert by["G3.4"]["status"] == "pass" and "80" in (repo / by["G3.4"]["evidence"][1]).read_text()
    assert by["G3.7"]["status"] == "pass" and by["G3.7"]["verified_by"] == "caller"         # CI-only: asserted, labelled
    r = record(repo, "--gate", "G3", "--scope", "TK-002;touch pwned", "--checks", "c.json", "--review", "review.md")
    assert r.returncode == 1 and "scope must match" in r.stderr and not (repo / "pwned").exists()

def test_rework_cap_escalates(repo):
    run(repo, "scripts/feos_state.py", "init")
    codes = [run(repo, "scripts/feos_state.py", "rework", "TK-002").returncode for _ in range(3)]
    assert codes == [0, 0, 3]

def test_hook_blocks_protected_paths(repo):
    env = {k: v for k, v in os.environ.items() if k != "FEOS_FRAMEWORK_EDIT"}
    payload = lambda p: json.dumps({"tool_name": "Edit", "cwd": str(repo), "tool_input": {"file_path": str(repo / p)}})
    assert run(repo, "scripts/feos_hook_protect.py", stdin=payload("feos/constitution.md"), env=env).returncode == 2
    assert run(repo, "scripts/feos_hook_protect.py", stdin=payload(".github/workflows/feos-validate.yml"), env=env).returncode == 2
    assert run(repo, "scripts/feos_hook_protect.py", stdin=payload("src/app.py"), env=env).returncode == 0

def test_hook_not_bypassed_by_subdir_cwd_notebook_or_bad_input(repo):
    env = {k: v for k, v in os.environ.items() if k != "FEOS_FRAMEWORK_EDIT"}
    sub = json.dumps({"tool_name": "Edit", "cwd": str(repo / "src"), "tool_input": {"file_path": str(repo / "feos/constitution.md")}})
    assert run(repo, "scripts/feos_hook_protect.py", stdin=sub, env=env).returncode == 2
    nb = json.dumps({"tool_name": "NotebookEdit", "cwd": str(repo), "tool_input": {"notebook_path": str(repo / "feos/x.ipynb")}})
    assert run(repo, "scripts/feos_hook_protect.py", stdin=nb, env=env).returncode == 2
    assert run(repo, "scripts/feos_hook_protect.py", stdin="not json", env=env).returncode == 2

def git(repo, *a): subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)

def test_guard_separation_of_duties(repo):
    git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "t@t"); git(repo, "config", "user.name", "t")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "base")
    git(repo, "checkout", "-qb", "feat/TK-002")
    (repo / "src").mkdir(); (repo / "src/app.py").write_text("x=1\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "feat: impl\n\nRefs: TK-002\nFEOS-Agent: builder")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0
    (repo / "tests/test_balance.py").write_text("def test_placeholder():\n    pass\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "fix tests\n\nRefs: TK-002\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "existing test" in r.stdout

def test_guard_protects_tester_tests_added_on_branch(repo):
    git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "t@t"); git(repo, "config", "user.name", "t")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "base")
    git(repo, "checkout", "-qb", "feat/TK-003")
    (repo / "tests/test_new.py").write_text("def test_new():\n    assert False\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "test: red\n\nRefs: TK-003\nFEOS-Agent: tester")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0
    (repo / "tests/test_new.py").write_text("def test_new():\n    assert True\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "feat: cheat\n\nRefs: TK-003\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "tester-owned" in r.stdout

def test_guard_sees_agent_trailer_outside_final_paragraph(repo):
    git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "t@t"); git(repo, "config", "user.name", "t")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "base")
    git(repo, "checkout", "-qb", "feat/TK-004")
    (repo / "tests/test_balance.py").write_text("def test_placeholder():\n    pass\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "feat: x\n\nRefs: TK-004\nFEOS-Agent: builder\n\nCo-Authored-By: A <a@example.com>")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "existing test" in r.stdout

def test_guard_protects_agent_and_prompt_adapters(repo):
    git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "t@t"); git(repo, "config", "user.name", "t")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "base")
    git(repo, "checkout", "-qb", "feat/TK-005")
    p = repo / ".claude/skills/feos-task/SKILL.md"; p.write_text(p.read_text() + "\nskip G3\n"); git(repo, "add", "-A")
    git(repo, "commit", "-qm", "chore: tweak\n\nRefs: TK-005\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and ".claude/skills/feos-task/SKILL.md" in r.stdout

APPROVAL = "---\nid: APPROVAL-{v}\nrelease: {v}\ndecision: {d}\napprover: \"{a}\"\ndate: \"\"\n---\n# approval\n"

def test_release_check_requires_human_approval_for_that_release(repo):
    d = repo / "evidence/release/v1.0.0"; d.mkdir(parents=True)
    for bad in ('v1.0.0"; import os #', "v1.0.0/../../x", "1.0.0", ""):
        r = run(repo, "scripts/feos_release_check.py", bad); assert r.returncode == 1 and "vX.Y.Z" in r.stdout, bad
    assert run(repo, "scripts/feos_release_check.py", "v1.0.0").returncode == 1                      # file missing
    (d / "approval.md").write_text(APPROVAL.format(v="v1.0.0", d="pending", a=""))
    assert run(repo, "scripts/feos_release_check.py", "v1.0.0").returncode == 1
    (d / "approval.md").write_text(APPROVAL.format(v="v1.0.0", d="approved", a="TBD"))
    assert run(repo, "scripts/feos_release_check.py", "v1.0.0").returncode == 1
    (d / "approval.md").write_text(APPROVAL.format(v="v0.9.0", d="approved", a="Jane Citizen"))  # copied from another release
    assert run(repo, "scripts/feos_release_check.py", "v1.0.0").returncode == 1
    (d / "approval.md").write_text(APPROVAL.format(v="v1.0.0", d="approved", a="Jane Citizen"))
    assert run(repo, "scripts/feos_release_check.py", "v1.0.0").returncode == 0

def test_release_workflow_never_interpolates_inputs_into_scripts(repo):
    wf = yaml.safe_load((repo / ".github/workflows/feos-release.yml").read_text())
    for job in wf["jobs"].values():
        for step in job["steps"]:
            assert "${{" not in step.get("run", ""), step
    assert "id-token" not in wf.get("permissions", {})

def task_branch(repo, name):
    git(repo, "init", "-q", "-b", "main"); git(repo, "config", "user.email", "t@t"); git(repo, "config", "user.name", "t")
    git(repo, "add", "-A"); git(repo, "commit", "-qm", "base"); git(repo, "checkout", "-qb", name)

def commit(repo, msg): git(repo, "add", "-A"); git(repo, "commit", "-qm", msg)

def test_guard_blocks_builder_test_runner_config(repo):
    task_branch(repo, "feat/TK-006")
    (repo / "conftest.py").write_text("import pytest\ndef pytest_collection_modifyitems(items):\n"
                                      "    for i in items: i.add_marker(pytest.mark.skip)\n")
    commit(repo, "feat: x\n\nRefs: TK-006\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "conftest.py" in r.stdout
    git(repo, "reset", "-q", "--hard", "main")
    (repo / "tests/pytest.ini").write_text("[pytest]\naddopts = -k nothing\n"); commit(repo, "feat: x\n\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "pytest.ini" in r.stdout
    git(repo, "reset", "-q", "--hard", "main")
    pkg = repo / "package.json"; pkg.write_text(json.dumps({"scripts": {"test": "vitest run"}, "dependencies": {}}))
    commit(repo, "test: runner\n\nFEOS-Agent: tester")
    pkg.write_text(json.dumps({"scripts": {"test": "vitest run"}, "dependencies": {"zod": "^3"}}))
    commit(repo, "feat: dep\n\nFEOS-Agent: builder")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0      # dependencies are the builder's
    pkg.write_text(json.dumps({"scripts": {"test": "exit 0"}, "dependencies": {"zod": "^3"}}))
    commit(repo, "feat: cheat\n\nFEOS-Agent: builder")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "package.json" in r.stdout

def test_guard_requires_known_agent_line_on_task_branches(repo):
    task_branch(repo, "feat/TK-007-x")
    (repo / "tests/test_balance.py").write_text("def test_placeholder():\n    pass\n"); commit(repo, "feat: no trailer")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "no 'FEOS-Agent" in r.stdout
    git(repo, "reset", "-q", "--hard", "main")
    (repo / "tests/test_balance.py").write_text("def test_placeholder():\n    pass\n"); commit(repo, "feat: x\n\nFEOS-Agent: buidler")
    r = run(repo, "scripts/feos_guard.py", "--base", "main"); assert r.returncode == 1 and "unknown agent 'buidler'" in r.stdout
    git(repo, "reset", "-q", "--hard", "main")
    (repo / "README.md").write_text("human fix\n"); commit(repo, "docs: fix\n\nFEOS-Agent: human")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0
    git(repo, "checkout", "-q", "main"); (repo / "CHANGELOG.md").write_text("x\n"); commit(repo, "chore: on main")
    git(repo, "checkout", "-q", "feat/TK-007-x"); git(repo, "merge", "-q", "--no-ff", "main", "-m", "Merge main")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0      # merge commits need no line (CI PR checkout)
    git(repo, "checkout", "-qb", "chore/human-work"); (repo / "README.md").write_text("again\n"); commit(repo, "docs: plain")
    assert run(repo, "scripts/feos_guard.py", "--base", "main").returncode == 0      # trailer only required on task branches

def hook_payload(repo, rel, tool="Write", **ti):
    return json.dumps({"tool_name": tool, "cwd": str(repo), "tool_input": {"file_path": str(repo / rel), **ti}})

def test_hook_protects_decision_ledger_even_in_framework_edit_mode(repo):
    env = {**os.environ, "FEOS_FRAMEWORK_EDIT": "1"}
    hook = lambda payload: run(repo, "scripts/feos_hook_protect.py", stdin=payload, env=env).returncode
    for rel in (".feos/state.json", "evidence/gates/G1-specs-2026-10-12T101500Z.json", "evidence/gates/G3-TK-002-2026-10-12T101500Z/G3.3.txt"):
        assert hook(hook_payload(repo, rel, content="{}")) == 2, rel
    assert hook(hook_payload(repo, "evidence/gates/G1-review.md", content="report")) == 0   # orchestrator persists reports here
    appr = "evidence/release/v1.0.0/approval.md"; pending = APPROVAL.format(v="v1.0.0", d="pending", a="")
    assert hook(hook_payload(repo, appr, content=pending)) == 0                       # release agent prepares it
    assert hook(hook_payload(repo, appr, content=APPROVAL.format(v="v1.0.0", d="approved", a="Jane"))) == 2
    assert hook(hook_payload(repo, appr, content=APPROVAL.format(v="v1.0.0", d="pending", a="Jane"))) == 2
    (repo / appr).parent.mkdir(parents=True); (repo / appr).write_text(pending)
    assert hook(hook_payload(repo, appr, "Edit", old_string="decision: pending", new_string="decision: approved")) == 2
    assert hook(hook_payload(repo, appr, "Edit", old_string="# approval", new_string="# approval\n\nNotes")) == 0
    assert hook(hook_payload(repo, appr, "MultiEdit", edits=[{"old_string": 'approver: ""', "new_string": 'approver: "Bot"'}])) == 2

def test_hook_command_fails_closed(repo, tmp_path):
    import shutil
    cmd = json.loads((repo / ".claude/settings.json").read_text())["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
    def hook(rel, path):
        return subprocess.run([shutil.which("bash"), "-c", cmd], input=hook_payload(repo, rel, content="x"), cwd=repo,
                              capture_output=True, text=True, env={"PATH": path, "CLAUDE_PROJECT_DIR": str(repo)}).returncode
    bin_ = tmp_path / "bin"; bin_.mkdir(); (bin_ / "python3").symlink_to(sys.executable)
    assert hook("feos/constitution.md", str(bin_)) == 2
    assert hook("src/app.py", str(bin_)) == 0
    assert hook("src/app.py", str(tmp_path / "no-python")) == 2                   # interpreter missing → block, not allow
    (repo / "scripts/feos_hook_protect.py").write_text("raise RuntimeError('boom')\n")
    assert hook("src/app.py", str(bin_)) == 2                                     # a crashing hook blocks
