# app/streamlit_app.py
import streamlit as st
from generator.generate import generate_code, generate_tests, extract_python_from_response
from evaluator.run_tests import evaluate
from pathlib import Path

st.set_page_config(page_title="GenAI Code & Test Generator", layout="wide")

st.title("Generative AI — Code & Test Case Generator")
st.markdown("Paste requirements or a short description; choose backend; generate code and tests; run pytest.")

requirements_text = st.text_area(
    "Requirements / Task description",
    height=200,
    value="Implement a function `is_palindrome(s: str)` that returns True for palindromes ignoring non-alphanumeric chars and case."
)
backend = st.selectbox("Backend", ["openai", "hf"])
model = st.text_input("Model name (optional)", value="gpt-4o-mini" if backend == "openai" else "bigcode/starcoder")
max_tokens = st.slider("Max tokens / max_new_tokens", 128, 2000, 512)

if st.button("Generate code + tests"):
    with st.spinner("Generating code..."):
        raw_code = generate_code(
            requirements_text,
            backend=backend,
            model=model,
            **({"max_tokens": max_tokens} if backend == "openai" else {"max_new_tokens": max_tokens}),
            temperature=0.0
        )
        code = extract_python_from_response(raw_code)

    st.subheader("Generated module")
    st.code(code, language="python")

    with st.spinner("Generating tests..."):
        raw_tests = generate_tests(
            code,
            backend=backend,
            model=model,
            **({"max_tokens": max_tokens} if backend == "openai" else {"max_new_tokens": max_tokens}),
            temperature=0.0
        )
        tests = extract_python_from_response(raw_tests)

    st.subheader("Generated tests (pytest)")
    st.code(tests, language="python")

    if st.button("Run pytest on generated code"):
        with st.spinner("Running tests..."):
            res = evaluate(code, tests)
        st.subheader("Test run output")
        st.text(res["output"])
        st.markdown(f"Workdir: `{res['workdir']}`")
