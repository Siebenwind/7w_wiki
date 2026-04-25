import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import wissenswerk


class WissenswerkCliContractTests(unittest.TestCase):
    def test_default_config_is_generic(self):
        config = wissenswerk.default_config_payload()
        self.assertEqual(config["project"]["product"], "Wissenswerk")
        self.assertEqual(config["project"]["tenant_id"], "example")
        self.assertEqual(config["vector_store"]["kind"], "pgvector")
        self.assertEqual(config["agents"]["roles"], ["coordinator", "curator", "verifier", "maintainer"])

    def test_provider_status_separates_configured_from_runtime_ready(self):
        payload = wissenswerk.provider_status(wissenswerk.default_config_payload())
        self.assertEqual(payload["status"], "configured")
        self.assertIn(payload["runtime_status"], {"ready", "missing_credentials"})
        self.assertEqual(payload["vector_store"]["kind"], "pgvector")

    def test_export_plan_has_no_public_blockers(self):
        payload = wissenswerk.export_plan(wissenswerk.DEFAULT_EXPORT_MANIFEST)
        self.assertEqual(payload["status"], "ready")
        self.assertEqual(payload["blockers"], [])
        self.assertEqual(payload["summary"]["overlap"], [])

    def test_export_materialize_applies_public_mappings(self):
        payload = wissenswerk.export_materialize_plan(
            wissenswerk.DEFAULT_EXPORT_MANIFEST,
            wissenswerk.REPO_ROOT / ".tmp" / "wissenswerk-export",
        )
        destinations = {operation["destination"] for operation in payload["operations"]}
        self.assertIn("AGENTS.md", destinations)
        self.assertIn("LICENSE", destinations)
        self.assertIn("project_manifest.json", destinations)
        self.assertIn("pyproject.toml", destinations)
        self.assertIn("Makefile", destinations)
        self.assertIn("wissenswerk.yaml", destinations)

    def test_materialized_manifest_uses_public_names(self):
        payload = wissenswerk.materialized_manifest_payload(wissenswerk.DEFAULT_EXPORT_MANIFEST)
        flattened = wissenswerk.flatten_manifest_paths(payload.get("include", {}))
        self.assertIn("AGENTS.md", flattened)
        self.assertIn("LICENSE", flattened)
        self.assertIn("project_manifest.json", flattened)
        self.assertIn("pyproject.toml", flattened)
        self.assertIn("Makefile", flattened)
        self.assertIn("wissenswerk.yaml", flattened)
        self.assertEqual(payload.get("export_mappings"), {})

    def test_manifest_spec_overlap_detects_directory_specs(self):
        self.assertTrue(wissenswerk.manifest_spec_matches_file("docs/Wissenswerk/", "docs/Wissenswerk/index.md"))
        self.assertFalse(wissenswerk.manifest_spec_matches_file("docs/Wissenswerk/", "docs/setup_rag.md"))

    def test_task_store_dedupes_open_signals(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = wissenswerk.TaskStore(Path(tmp) / "tasks")
            first = store.raise_signal(
                task_type="anomaly",
                severity="medium",
                role="curator",
                summary="Duplicate chunk id",
                evidence=["fixture.json"],
                dedupe_key="test:duplicate",
                created_by="test",
            )
            second = store.raise_signal(
                task_type="anomaly",
                severity="high",
                role="curator",
                summary="Duplicate chunk id again",
                evidence=["fixture.json"],
                dedupe_key="test:duplicate",
                created_by="test",
            )
            self.assertEqual(first["status"], "created")
            self.assertEqual(second["status"], "deduped")
            self.assertEqual(first["task"]["id"], second["task"]["id"])
            self.assertEqual(second["task"]["repeat_count"], 2)
            self.assertTrue((Path(tmp) / "tasks" / "active" / f"{first['task']['id']}.md").exists())

    def test_task_lifecycle_removes_active_markdown_on_resolution(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = wissenswerk.TaskStore(Path(tmp) / "tasks")
            created = store.raise_signal(
                task_type="approval",
                severity="critical",
                role="maintainer",
                summary="Approval required",
                dedupe_key="test:approval",
                created_by="test",
            )["task"]
            claimed = store.claim(created["id"], "maintainer")
            self.assertEqual(claimed["status"], "working")
            resolved = store.resolve(created["id"], "Approved elsewhere")
            self.assertEqual(resolved["status"], "completed")
            self.assertFalse((Path(tmp) / "tasks" / "active" / f"{created['id']}.md").exists())

    def test_task_cli_raise_and_digest_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = wissenswerk.default_config_payload()
            config["paths"]["tasks"] = str(Path(tmp) / "tasks")
            config_path = Path(tmp) / "wissenswerk.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = wissenswerk.main(
                    [
                        "--config",
                        str(config_path),
                        "task",
                        "raise",
                        "--type",
                        "blocker",
                        "--severity",
                        "high",
                        "--role",
                        "maintainer",
                        "--summary",
                        "Provider unavailable",
                        "--json",
                    ]
                )
            self.assertEqual(code, 0)
            raised = json.loads(out.getvalue())
            self.assertEqual(raised["status"], "created")

            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                code = wissenswerk.main(["--config", str(config_path), "task", "digest", "--since", "24h", "--json"])
            self.assertEqual(code, 0)
            digest = json.loads(out.getvalue())
            self.assertEqual(digest["status"], "ok")
            self.assertEqual(len(digest["open"]), 1)

    def test_ingest_validation_raises_deduped_audit_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = wissenswerk.default_config_payload()
            config["paths"]["tasks"] = str(root / "tasks")
            config["paths"]["reports"] = str(root / "reports")
            config["paths"]["ragprep_imports"] = str(root / "imports")
            config_path = root / "wissenswerk.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")
            ragprep = root / "ragprep"
            ragprep.mkdir()
            (ragprep / "bad.json").write_text(
                json.dumps({"document_id": "doc-1", "chunk_id": "chunk-1", "text": "hello"}),
                encoding="utf-8",
            )

            for _ in range(2):
                out = io.StringIO()
                with contextlib.redirect_stdout(out):
                    code = wissenswerk.main(
                        ["--config", str(config_path), "ingest", "--from-ragprep", str(ragprep), "--apply", "--json"]
                    )
                self.assertEqual(code, 1)
            tasks = wissenswerk.TaskStore(root / "tasks").list()
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["type"], "audit_finding")
            self.assertEqual(tasks[0]["repeat_count"], 2)


if __name__ == "__main__":
    unittest.main()
