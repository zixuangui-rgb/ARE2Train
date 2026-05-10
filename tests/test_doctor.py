from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from are2train.doctor import run_checks  # noqa: E402


class DoctorTest(unittest.TestCase):
    def test_current_repo_has_no_failed_checks(self) -> None:
        results = run_checks(ROOT)
        failures = [result for result in results if result.status == "fail"]
        messages = [f"{result.name}: {result.message}" for result in failures]
        self.assertEqual([], messages)


if __name__ == "__main__":
    unittest.main()
