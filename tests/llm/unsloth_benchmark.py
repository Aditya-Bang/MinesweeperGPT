from unsloth import FastLanguageModel
from src.finetuning.prompt import SYSTEM_PROMPT
import torch

max_seq_length = 2048  # Can increase for longer reasoning traces
lora_rank = 32         # Larger rank = smarter, but slower

# Load model + tokenizer with vLLM acceleration
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/Qwen3-0.6B",
    max_seq_length = max_seq_length,
    load_in_4bit = False,       # False for LoRA 16bit
    fast_inference = True,      # Enable vLLM fast inference
    max_lora_rank = lora_rank,
    gpu_memory_utilization = 0.7, # Reduce if out of memory
)

# Example prompt
messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": """
* * * * * * * *
* * * * * * * *
* * * * * * * *
* * * * * * * *
* 2 1 1 1 * * *
F 1 0 0 1 * * *
1 1 0 0 1 3 * *
0 0 0 0 0 2 * *
"""}
]

# Apply chat template, enabling thinking mode
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True,
    enable_thinking=False   # key part for <think> sections
)

# Tokenize input
inputs = tokenizer([text], return_tensors="pt").to(model.device)

# Generate
generated_ids = model.generate(
    **inputs,
    max_new_tokens=512,
)

# Extract only the new tokens
output_ids = generated_ids[0][len(inputs.input_ids[0]):].tolist()

# Parse out thinking vs final content
try:
    # Look for </think> token (151668 in Qwen vocab)
    index = len(output_ids) - output_ids[::-1].index(151668)
except ValueError:
    index = 0

thinking_content = tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
content = tokenizer.decode(output_ids, skip_special_tokens=True).strip("\n")

# print("thinking content:", thinking_content)
print("content:\n", content)
