import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import gate


class ReleaseGateTest(unittest.TestCase):
    def test_release_lifecycle(self):
        evidence = gate.load(gate.EVIDENCE)
        blocked = gate.review(evidence, gate.load(gate.CLAIMS))
        self.assertEqual(blocked["status"], "BLOCKED")
        self.assertEqual([row["missing"] for row in blocked["claims"]],
                         [["PG-105-FREE"], ["PG-107-XLSX"]])
        revised = gate.review(evidence, ["csv-pro"])
        self.assertEqual(revised["status"], "READY FOR HUMAN")
        with (
            tempfile.TemporaryDirectory(dir=gate.ROOT) as directory,
            patch.object(gate, "ROOT", Path(directory)),
        ):
            with self.assertRaisesRegex(ValueError, "Blocked claims"):
                gate.publish(blocked, blocked["revision"])
            with self.assertRaisesRegex(ValueError, "Stale approval"):
                gate.publish(revised, blocked["revision"])
            evidence["checks"]["PG-105-FREE"] = True
            with self.assertRaisesRegex(ValueError, "Stale approval"):
                gate.publish(gate.review(evidence, ["csv-pro"]), revised["revision"])
            self.assertFalse((gate.ROOT / "receipts").exists())
            path = gate.publish(revised, revised["revision"])
            self.assertEqual(gate.publish(revised, revised["revision"]), path)
            self.assertEqual(len(list((gate.ROOT / "receipts").iterdir())), 1)
            self.assertIn("Pro workspace admins can export reports as CSV.",
                          (gate.ROOT / path).read_text(encoding="utf-8"))

    def test_cli_review(self):
        result = subprocess.run(
            [sys.executable, str(gate.ROOT / "gate.py"), "review"],
            check=True, capture_output=True, text=True,
        )
        self.assertEqual(json.loads(result.stdout)["status"], "BLOCKED")

    def test_unrecognized_claim_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "Unknown claim"):
            gate.review(gate.load(gate.EVIDENCE), ["anything-goes"])


if __name__ == "__main__":
    unittest.main()
