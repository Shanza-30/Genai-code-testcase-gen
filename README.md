# Generative AI — Code & Test Case Generator

This project is a **Streamlit-based web application** that allows users to input requirements or a short description of a function.  
The app then uses **Hugging Face models (e.g., Salesforce CodeGen, StarCoder)** to automatically generate:

 ✅ Python function code  
 ✅ Unit test cases (using `pytest`)  
✅ Execution of tests with results displayed  


## 🚀 Features
- Paste any natural language **requirement/task description**.  
- Choose the backend model (e.g., `Salesforce/codegen-350M-multi`).  
- Generate both **code implementation** and **test cases** automatically.  
- Run tests live inside the app using **pytest**.  
- Simple UI built with **Streamlit**.  


## 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Shanza-30/Genai-code-testcase-gen
   cd generative-ai-codegen
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Minimum dependencies:
   - `streamlit`
   - `transformers`
   - `torch`
   - `accelerate`
   - `pytest`

---

## ▶️ Usage

Run the app with:

```bash
streamlit run main.py
```

Then open the local URL (usually `http://localhost:8501/`) in your browser.

---

## 📝 Example

### Input (Requirement):
```
Implement a function `is_palindrome(s: str)` that returns True for palindromes ignoring non-alphanumeric chars and case.
```

### Output (Generated Code):
```python
def is_palindrome(s: str) -> bool:
    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())
    return cleaned == cleaned[::-1]
```

### Output (Generated Tests):
```python
def test_palindrome_true():
    assert is_palindrome("A man, a plan, a canal: Panama")

def test_palindrome_false():
    assert not is_palindrome("hello world")
```

---

## 📚 Example Prompts You Can Try
- `Implement fibonacci(n: int) that returns first n Fibonacci numbers as a list.`  
- `Write a function reverse_words(sentence: str) that reverses word order.`  
- `Create a function count_vowels(s: str) that counts vowels in a string.`  

---

## ⚡ Notes
- The project currently uses **Hugging Face models** (`Salesforce/codegen-350M-multi` by default).  
- Models are downloaded and cached locally in the `HF_CACHE` directory (if set).  
- Internet connection is required for the first run to download models.  

---

## 📄 License
MIT License – feel free to use and modify for learning and research.
