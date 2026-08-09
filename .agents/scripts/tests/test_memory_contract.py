from __future__ import annotations

import unittest
from pathlib import Path


TOOLKIT = Path(__file__).resolve().parents[2]


class MemoryTrustContractTests(unittest.TestCase):
    def test_inferred_memory_requires_explicit_approval(self):
        skill = (TOOLKIT / "skills/memory-system/SKILL.md").read_text("utf-8")

        self.assertIn("version: 1.1.0", skill)
        self.assertIn("inferred", skill.lower())
        self.assertIn("explicit approval", skill.lower())
        self.assertIn("must not be written to `MEMORY.md`", skill)
        self.assertIn("Current instructions win over stale memory", skill)

    def test_remember_is_explicit_durable_write_path(self):
        workflow = (TOOLKIT / "workflows/remember.md").read_text("utf-8")

        self.assertIn("version: 1.1.0", workflow)
        self.assertIn("Treat `/remember` as explicit persistence intent", workflow)
        self.assertIn("Never persist background inference without approval", workflow)
        self.assertIn("Never silently overwrite contradictions", workflow)
        self.assertIn("obtain approval first", workflow)


if __name__ == "__main__":
    unittest.main()
