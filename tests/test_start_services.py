import importlib.util
from contextlib import nullcontext, redirect_stdout
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"


def load_module(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


launcher = load_module("start_services")
nav = load_module("generate_nav")


class StartupTests(unittest.TestCase):
    def test_reuses_authenticated_jupyter(self):
        with (
            patch.object(launcher, "running_jupyter", return_value={"token": "test-token"}),
            patch.object(launcher, "port_in_use", return_value=True),
            patch.object(launcher, "jupyter_ready", return_value=True),
            patch.object(launcher, "start_background") as spawn,
        ):
            self.assertEqual(launcher.ensure_jupyter(Path("logs")), "test-token")
            spawn.assert_not_called()

    def test_does_not_replace_foreign_jupyter_port(self):
        with (
            patch.object(launcher, "running_jupyter", return_value=None),
            patch.object(launcher, "port_in_use", return_value=True),
            patch.object(launcher, "start_background") as spawn,
        ):
            with self.assertRaisesRegex(RuntimeError, "端口"):
                launcher.ensure_jupyter(Path("logs"))
            spawn.assert_not_called()

    def test_new_token_is_not_a_command_line_argument(self):
        with (
            patch.object(launcher, "running_jupyter", return_value=None),
            patch.object(launcher, "port_in_use", return_value=False),
            patch.object(launcher.secrets, "token_hex", return_value="test-token"),
            patch.object(launcher, "start_background", return_value=(object(), Path("log"))) as spawn,
            patch.object(launcher, "wait_ready"),
        ):
            self.assertEqual(launcher.ensure_jupyter(Path("logs")), "test-token")
            self.assertEqual(spawn.call_args.kwargs["token"], "test-token")
            self.assertNotIn("test-token", " ".join(spawn.call_args.args[1]))

    def test_reuses_reset_service_without_starting_another(self):
        with (
            patch.object(launcher, "port_in_use", return_value=True),
            patch.object(launcher, "reset_ready", return_value=True),
            patch.object(launcher, "start_background") as spawn,
        ):
            launcher.ensure_reset(Path("logs"))
            spawn.assert_not_called()

    def test_does_not_replace_foreign_reset_port(self):
        with (
            patch.object(launcher, "port_in_use", return_value=True),
            patch.object(launcher, "reset_ready", return_value=False),
            patch.object(launcher, "start_background") as spawn,
        ):
            with self.assertRaisesRegex(RuntimeError, "端口"):
                launcher.ensure_reset(Path("logs"))
            spawn.assert_not_called()

    def test_reset_health_check_never_resets_an_exercise(self):
        body = b'{"service":"practice-and-exams","version":1}'
        with patch.object(launcher, "request", return_value=(200, {}, body)) as request:
            self.assertTrue(launcher.reset_ready())
            request.assert_called_once_with(f"http://localhost:{launcher.RESET_PORT}/api/health")

    def test_reset_health_check_rejects_unrelated_services(self):
        for response in [
            (200, {}, b'{"service":"another-app","version":1}'),
            (200, {}, b'{"service":"practice-and-exams","version":2}'),
            (503, {}, b'{"service":"practice-and-exams","version":1}'),
            (200, {}, b'[]'),
            (200, {}, b'<html>another service</html>'),
        ]:
            with self.subTest(response=response), patch.object(launcher, "request", return_value=response):
                self.assertFalse(launcher.reset_ready())

    def test_navigation_does_not_receive_token(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            navigation = state / "navigation.html"
            navigation.write_text("original", encoding="utf-8")
            result = subprocess.CompletedProcess([], 0, "", "")
            with (
                patch.object(launcher, "NAVIGATION", navigation),
                patch.object(launcher.subprocess, "run", return_value=result) as run,
            ):
                launcher.refresh_navigation(state)
                self.assertEqual(run.call_args.kwargs["env"]["JUPYTER_TOKEN"], "")
                self.assertIn("--navigation-only", run.call_args.args[0])
                self.assertEqual(run.call_args.kwargs["cwd"], launcher.ROOT)
                self.assertEqual(len(list(state.glob("navigation-before-*.html"))), 1)

    def test_generation_failure_restores_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            state = Path(directory)
            navigation = state / "navigation.html"
            navigation.write_text("original", encoding="utf-8")

            def failed_generation(*args, **kwargs):
                navigation.write_text("partial output", encoding="utf-8")
                return subprocess.CompletedProcess([], 1, "", "test failure")

            with (
                patch.object(launcher, "NAVIGATION", navigation),
                patch.object(launcher.subprocess, "run", side_effect=failed_generation),
            ):
                with self.assertRaisesRegex(RuntimeError, "导航生成失败"):
                    launcher.refresh_navigation(state)
                self.assertEqual(navigation.read_text(encoding="utf-8"), "original")

    def test_navigation_only_never_writes_lectures(self):
        import builtins

        original_open = builtins.open

        def read_only_open(file, mode="r", *args, **kwargs):
            self.assertFalse(any(flag in mode for flag in "wax+"), str(file))
            return original_open(file, mode, *args, **kwargs)

        with (
            patch("builtins.open", side_effect=read_only_open),
            patch.object(nav.os, "makedirs") as mkdir,
        ):
            learning = nav.load_learning_materials(render_lectures=False)
            mkdir.assert_not_called()
            self.assertTrue(any("rendered_path" in item for item in learning.values()))

    def test_browser_authentication_opens_before_navigation(self):
        output = io.StringIO()
        with (
            patch.object(launcher.Path, "mkdir"),
            patch.object(launcher, "startup_lock", return_value=nullcontext()),
            patch.object(launcher, "ensure_jupyter", return_value="test-token"),
            patch.object(launcher, "ensure_reset"),
            patch.object(launcher, "refresh_navigation"),
            patch.object(launcher.webbrowser, "open", return_value=True) as browser,
            redirect_stdout(output),
        ):
            self.assertEqual(launcher.main([]), 0)
            self.assertEqual(browser.call_count, 2)
            self.assertEqual(browser.call_args_list[0].args[0], launcher.JUPYTER_URL + "/lab?token=test-token")
            self.assertEqual(browser.call_args_list[1].args[0], launcher.NAVIGATION.as_uri())
            self.assertNotIn("test-token", output.getvalue())


if __name__ == "__main__":
    unittest.main()
