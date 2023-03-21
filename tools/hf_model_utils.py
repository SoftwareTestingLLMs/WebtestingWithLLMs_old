import re
from typing import List

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def load_model(model_name: str, device: str, precision: str):
    _dtype = torch.float16 if precision == "float16" else torch.float32

    assert ((precision == "float16" and "cuda" in device) or precision != "float16"), (
        "'float16' is only supported when using the GPU")

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=_dtype).to(device)

    if "codegen" in model_name:
        tokenizer.pad_token = 50256

    return tokenizer, model


def find_re(string, pattern, start_pos):
    m = pattern.search(string, start_pos)
    return m.start() if m else -1


def truncate(completion, model_name: str):
    if "codegen" in model_name:
        return truncate_codegen_model_completion(completion)

    return completion


def truncate_codegen_model_completion(completion):
    terminals = [re.compile(r, re.MULTILINE) for r in ["^#", re.escape("<|endoftext|>"), "^'''", '^"""', "\n\n\n"]]

    prints = list(re.finditer('^print', completion, re.MULTILINE))
    if len(prints) > 1:
        completion = completion[:prints[1].start()]

    defs = list(re.finditer('^def', completion, re.MULTILINE))
    if len(defs) > 1:
        completion = completion[:defs[1].start()]

    start_pos = 0

    terminals_pos = [pos for pos in [find_re(completion, terminal, start_pos) for terminal in terminals] if pos != -1]
    if len(terminals_pos) > 0:
        return completion[:min(terminals_pos)]
    else:
        return completion


def generate(prompt: List[str], tokenizer, model, device: str,
             num_return_sequences=1,
             temperature=0.2,
             max_new_tokens=256,
             top_p=0.95,
             pad_token_id=50256):
    input_ids = tokenizer(prompt, truncation=True, padding=True, return_tensors="pt").input_ids.to(device)
    input_ids_len = input_ids.shape[1]

    generated_ids = model.generate(input_ids, do_sample=True, num_return_sequences=num_return_sequences,
                                   temperature=temperature, max_new_tokens=max_new_tokens, top_p=top_p,
                                   pad_token_id=pad_token_id, use_cache=True)

    decoded_generation = tokenizer.batch_decode(generated_ids[:, input_ids_len:])

    return decoded_generation
