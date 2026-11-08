import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


class CodecovConfigurationTest(unittest.TestCase):
    def test_codecov_yaml_configuration(self):
        codecov_file = REPO_ROOT / "codecov.yml"
        self.assertTrue(codecov_file.is_file(), "codecov.yml must exist at repo root")
        content = codecov_file.read_text(encoding="utf-8")
        self.assertIn("coverage:", content)
        self.assertIn("flag_management:", content)
        self.assertIn("component_management:", content)
        self.assertIn("name: python", content)
        self.assertIn("name: javascript", content)
        self.assertIn("name: csharp", content)
        self.assertIn("name: go", content)
        self.assertIn("name: cpp", content)
        self.assertIn("component_id: python_code", content)
        self.assertIn("component_id: javascript_code", content)
        self.assertIn("component_id: go_code", content)

    def test_sonarcloud_configuration(self):
        sonar_file = REPO_ROOT / ".sonarcloud.properties"
        self.assertTrue(sonar_file.is_file(), ".sonarcloud.properties must exist")
        content = sonar_file.read_text(encoding="utf-8")
        self.assertIn("sonar.exclusions", content)
        self.assertIn("sonar.cpd.exclusions", content)
        self.assertIn(".github/**", content)
        self.assertIn("docs/**", content)
        self.assertIn("sphinx_docs_build/**", content)

    def test_workflow_codecov_steps(self):
        workflows = {
            "python_test.yml": "python",
            "javascript_test.yml": "javascript",
            "csharp_test.yml": "csharp",
            "go_test.yml": "go",
        }
        for wf_file, flag in workflows.items():
            path = REPO_ROOT / ".github" / "workflows" / wf_file
            self.assertTrue(path.is_file(), f"{wf_file} must exist")
            content = path.read_text(encoding="utf-8")
            self.assertIn(
                "codecov/codecov-action", content, f"{wf_file} must use codecov-action"
            )
            self.assertIn(
                "token: ${{ secrets.CODECOV_TOKEN }}",
                content,
                f"{wf_file} must provide token",
            )
            self.assertIn(f"flags: {flag}", content, f"{wf_file} must set flag {flag}")
            self.assertIn(
                "fail_ci_if_error: false",
                content,
                f"{wf_file} must set fail_ci_if_error",
            )
            self.assertIn(
                "codecov.yml",
                content,
                f"{wf_file} must track codecov.yml in changed-files",
            )


if __name__ == "__main__":
    unittest.main()
