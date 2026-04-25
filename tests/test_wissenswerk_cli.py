import unittest

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


if __name__ == "__main__":
    unittest.main()
