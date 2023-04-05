import os
from datetime import datetime
from multiprocessing import Process, set_start_method

import click
import yaml

from tools.hf_model_utils import load_model, generate, truncate, parse_model_configuration

GENERATED_SCRIPTS_PATH = "generated_scripts"


def run_model(histories, prompt_list, model_name, device, precision, folder_path, debug: bool, generation_config):
    print("Loading model...")
    tokenizer, model = load_model(model_name, device, precision)
    print("Loading finished")

    def _wrap(p):
        return f"# {p}\n"
    
    if not isinstance(prompt_list, list):
        prompt_list = [prompt_list]

    for i, prompt in enumerate(prompt_list):
        histories = [h + _wrap(prompt) for h in histories]
        completions = generate(histories, tokenizer, model, device, **generation_config)
        histories = [h + f"{truncate(c)}\n\n" for h, c in zip(histories, completions)]

        # Prettify: removes two of the four newlines
        if histories[0][-4:] == "\n\n\n\n":
            histories[0] = histories[0][:-2]

        print("-" * 10)
        print(i)
        print("-" * 10)
        print(histories[0])
        print("-" * 10)

    if not debug:
        with open(os.path.join(folder_path, f"{model_name.replace('/', '-')}.py"), "w") as f:
            f.write(histories[0])


@click.command()
@click.option("-c", "--config", type=str, required=True)
def main(config: str):
    with open(config, "r") as f:
        config = yaml.safe_load(f)

    prompts = config["prompts"]
    history = ["\n".join(config["history"]) + "\n\n"]

    models = parse_model_configuration(config["models"], config["general_device"], config["general_precision"])

    generation_config = config.get("generation_config", {})

    debug = config["debug"]

    folder_path = None

    if not debug:
        # Setup folder
        start_data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join(GENERATED_SCRIPTS_PATH, start_data)
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, "default.yaml"), "w") as f:
            yaml.safe_dump(config, f, default_flow_style=False)

    for model_name, device, precision in models:
        p = Process(target=run_model, args=(history, prompts, model_name, device, precision, folder_path, debug,
                                             generation_config))
        p.start()
        p.join()
        p.close()


if __name__ == "__main__":
    set_start_method("spawn")
    main()
