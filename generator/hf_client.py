# generator/hf_client.py
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import os

CACHE_DIR = os.getenv("HF_CACHE", None)

def get_hf_code_generator(model_name: str = "Salesforce/codegen-350M-multi"):
    """
    Returns a text-generation pipeline for code.
    Uses Salesforce CodeGen (or other Hugging Face causal LM models).
    """
    tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir=CACHE_DIR, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        cache_dir=CACHE_DIR,
        trust_remote_code=True
    )
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device=0 if torch.cuda.is_available() else -1
    )
    return pipe

def generate_with_hf(prompt: str, model_name: str = "Salesforce/codegen-350M-multi", max_new_tokens: int = 512, temperature: float = 0.0):
    pipe = get_hf_code_generator(model_name)
    outputs = pipe(prompt, max_new_tokens=max_new_tokens, temperature=temperature, do_sample=False)
    return outputs[0]["generated_text"]
