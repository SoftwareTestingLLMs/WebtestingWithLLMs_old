import re
from typing import List, Union

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


def parse_device(device: str):
    if device == "gpu":
        device = "cuda:0"

        assert torch.cuda.is_available(), "Specifying the device 'gpu' requires that CUDA is available."
    else:
        assert device == "cpu", f"Device '{device}' is not valid, only 'cpu' or 'gpu' are valid devices."

    return device


def parse_precision(precision: str, parsed_device: str):
    if precision == "int8":
        return precision

    possible_dtypes = {
        "float16": torch.float16,
        "float32": torch.float32
    }

    try:
        parsed_precision = possible_dtypes[precision]
    except KeyError:
        raise ValueError(f"Precision '{precision}' is not valid, supported are: {list(possible_dtypes.keys())}")

    assert ((precision == "float16" and "cuda" in parsed_device) or precision != "float16"), (
        "'float16' is only supported when using the GPU")

    return parsed_precision


def parse_model_configuration(model_configuration: List, general_device: str, general_precision: str):
    parsed_general_device = parse_device(general_device)
    parsed_general_precision = parse_precision(general_precision, parsed_general_device)

    models = []

    for specific_model_config in model_configuration:
        error_string = f"'{specific_model_config}' is not a valid model configuration."

        if isinstance(specific_model_config, str):
            models.append((specific_model_config, parsed_general_device, parsed_general_precision))
        elif isinstance(specific_model_config, dict):
            assert len(specific_model_config) == 1, error_string

            model_name, model_specifics = next(iter(specific_model_config.items()))

            device = parse_device(model_specifics.get("device", general_device))
            precision = parse_precision(model_specifics.get("precision", general_precision), device)

            models.append((model_name, device, precision))
        else:
            raise RuntimeError(error_string)

    return models


def load_model(model_name: str, device: str, precision: Union[torch.dtype, str]):
    if precision == "int8":
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            load_in_8bit=True,
            device_map="auto"
        )
    else:
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=precision).to(device)

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    

    tokenizer.pad_token = tokenizer.eos_token

    return tokenizer, model


def find_re(string, pattern, start_pos):
    m = pattern.search(string, start_pos)
    return m.start() if m else -1


def truncate(completion):
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
             do_sample=True,
             temperature=0.6,
             max_new_tokens=256,
             top_k=0.0,
             top_p=0.95,
             pad_token_id=50256):
    input_ids = tokenizer(prompt, truncation=True, padding=True, return_tensors="pt").input_ids.to(device)
    input_ids_len = input_ids.shape[1]

    generated_ids = model.generate(input_ids, do_sample=do_sample, num_return_sequences=num_return_sequences,
                                   temperature=temperature, max_new_tokens=max_new_tokens, top_k=top_k,
                                   top_p=top_p, pad_token_id=pad_token_id, use_cache=True)

    decoded_generation = tokenizer.batch_decode(generated_ids[:, input_ids_len:])

    return decoded_generation
