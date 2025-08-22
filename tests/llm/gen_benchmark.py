import time
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "Qwen/Qwen3-0.6B"

# load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

def run_inference(device: str):
    print(f"\n===== Running on {device.upper()} =====")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if device == "cuda" else torch.float32,
    ).to(device)

    print("Model device:", next(model.parameters()).device)

    # prepare input
    prompt = "Give me a short introduction to large language model."
    messages = [{"role": "user", "content": prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(device)

    # measure time
    start = time.time()
    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=256,  # shorter for benchmarking
    )
    end = time.time()

    # decode
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    try:
        index = len(output_ids) - output_ids[::-1].index(151668)
    except ValueError:
        index = 0

    thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
    content = tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

    print("thinking content:", thinking_content[:100], "..." if len(thinking_content) > 100 else "")
    print("content:", content[:200], "..." if len(content) > 200 else "")
    print(f"Generation time on {device.upper()}: {end - start:.2f} seconds")


# Run on CPU
run_inference("cpu")

# Run on GPU (if available)
if torch.cuda.is_available():
    run_inference("cuda")
else:
    print("\nCUDA not available.")
