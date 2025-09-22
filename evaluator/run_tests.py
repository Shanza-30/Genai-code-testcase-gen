# evaluator/run_tests.py
import os
import subprocess
import tempfile
from pathlib import Path
import sys
import shutil
from typing import Tuple

def write_module_and_tests(module_code: str, tests_code: str, workdir: Path = None) -> Path:
    if workdir is None:
        workdir = Path(tempfile.mkdtemp(prefix="genai_deploy_"))
    else:
        workdir = Path(workdir)
        workdir.mkdir(parents=True, exist_ok=True)

    # Write module
    module_path = workdir / "module_under_test.py"
    module_path.write_text(module_code, encoding="utf-8")

    # Write tests
    tests_path = workdir / "test_generated.py"
    tests_path.write_text(tests_code, encoding="utf-8")

    return workdir

def run_pytest_and_coverage(workdir: Path) -> Tuple[int, str, str]:
    """
    Returns (exit_code, pytest_output, coverage_report)
    """
    env = os.environ.copy()
    # Ensure pytest-cov is available
    cmd = [sys.executable, "-m", "pytest", "-q", "--disable-warnings", "--maxfail=1", "--cov=.", "--cov-report=term"]
    proc = subprocess.run(cmd, cwd=workdir, capture_output=True, text=True, env=env)
    out = proc.stdout + "\n" + proc.stderr
    # Get coverage summary if available
    # Already included in pytest-cov output. We'll return proc.returncode and out
    return proc.returncode, out

def evaluate(module_code: str, tests_code: str, workdir: Path = None) -> dict:
    workdir = write_module_and_tests(module_code, tests_code, workdir)
    code, output = run_pytest_and_coverage(workdir)
    result = {
        "exit_code": code,
        "output": output,
        "workdir": str(workdir)
    }
    return result

if __name__ == "__main__":
    # quick local test harness
    sample_module = '''
def add(a,b):
    """Return a+b"""
    return a + b
'''
    sample_tests = '''
import module_under_test as m

def test_add():
    assert m.add(2,3) == 5
'''
    res = evaluate(sample_module, sample_tests)
    print(res["exit_code"])
    print(res["output"])
    print("workdir:", res["workdir"])
