# generator/generate.py
import re
from generator.hf_client import generate_with_hf  # ✅ Only Hugging Face backend

def prompt_for_code_from_requirements(requirements_text: str) -> str:
    return f"""
You are an expert software engineer. Implement a Python module that meets the following requirements.
Provide only the Python code (no extra commentary), include docstrings, and keep functions small and testable.

Requirements:
{requirements_text}

Return the full Python source code.
""".strip()

def prompt_for_tests_from_code(code_text: str) -> str:
    return f"""
You are an expert developer writing pytest unit tests. Given the following Python module, generate a set of pytest tests that:
- cover typical and edge cases
- are self-contained (import the module)
- use temporary fixtures if needed (tmp_path)
- avoid external network calls
Return only the test file content (a single Python file).
Module:
{code_text}
""".strip()

def _normalize_kwargs(kwargs: dict) -> dict:
    """
    Convert 'max_tokens' -> 'max_new_tokens' if passed.
    Remove backend/model since HF function doesn't need them.
    """
    kwargs = kwargs.copy()
    kwargs.pop("backend", None)
    kwargs.pop("model", None)

    if "max_tokens" in kwargs:
        kwargs["max_new_tokens"] = kwargs.pop("max_tokens")

    return kwargs

def generate_code(requirements_text: str, **kwargs) -> str:
    """
    Generate code using Hugging Face.
    Automatically handles max_tokens -> max_new_tokens conversion.
    """
    prompt = prompt_for_code_from_requirements(requirements_text)
    return generate_with_hf(prompt, **_normalize_kwargs(kwargs))

def generate_tests(code_text: str, **kwargs) -> str:
    """
    Generate tests using Hugging Face.
    Automatically handles max_tokens -> max_new_tokens conversion.
    """
    prompt = prompt_for_tests_from_code(code_text)
    return generate_with_hf(prompt, **_normalize_kwargs(kwargs))

def extract_python_from_response(resp: str) -> str:
    resp = re.sub(r"```(?:python)?\n?", "", resp)
    resp = resp.replace("```", "")
    return resp.strip()
