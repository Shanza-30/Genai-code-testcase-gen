# generator/openai_client.py  (rename to huggingface_client.py if you want)

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# ✅ Hugging Face model load karo (1 bar load hoga, baad me reuse hoga)
MODEL_NAME = "bigcode/starcoder"  # aap CodeLlama ya CodeT5 bhi use kar sakte ho
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
)

def generate_with_huggingface(prompt, max_tokens=256, temperature=0.3):
    """
    HuggingFace se free me code generate karega
    """
    result = pipe(
        prompt,
        max_length=max_tokens,
        do_sample=True,
        temperature=temperature,
    )
    return result[0]['generated_text']
