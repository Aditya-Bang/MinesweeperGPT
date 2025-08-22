# tests/llm/unsloth_benchmark_timing.py
import time
import torch
from unsloth import FastLanguageModel

model_name = "Qwen/Qwen3-0.6B"

max_seq_length = 2048
lora_rank = 32

prompt = "Give me a short introduction to large language model."
max_new_tokens = 256  # shorter for benchmarking


# Load model on specified device
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    load_in_4bit=True,
    fast_inference=True,       # Enable vLLM backend
    max_lora_rank=lora_rank,
    gpu_memory_utilization=0.7,
)

# Move model to GPU explicitly if not already
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Tokenize input
inputs = tokenizer(prompt, return_tensors="pt").to(device)

# Measure inference time
start_time = time.time()
outputs = model.generate(
    **inputs,
    max_new_tokens=max_new_tokens,
)
end_time = time.time()

# Decode the output
response = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("Response:\n", response)
print(f"\nInference time: {end_time - start_time:.3f} seconds")
