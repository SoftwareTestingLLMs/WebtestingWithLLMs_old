import os
from datetime import datetime
from multiprocessing import Process

from tools.hf_model_utils import load_model, generate, truncate

GENERATED_SCRIPTS_PATH = "generated_scripts"


def run_model(histories, prompt_list, model_name, folder_path):
    print("Loading model...")
    tokenizer, model = load_model(model_name, "cpu", "float32")
    print("Loading finished")

    def _wrap(p):
        return f"# {p}\n"

    for i, prompt in enumerate(prompt_list):
        histories = [h + _wrap(prompt) for h in histories]
        completions = generate(histories, tokenizer, model, "cpu")
        histories = [h + f"{truncate(c, model_name)}\n\n" for h, c in zip(histories, completions)]

        # Prettify: removes two of the four newlines
        if histories[0][-4:] == "\n\n\n\n":
            histories[0] = histories[0][:-2]

        print("-" * 10)
        print(i)
        print("-" * 10)
        print(histories[0])
        print("-" * 10)

    with open(os.path.join(folder_path, f"{model_name.replace('/', '-')}.py"), "w") as f:
        f.write(histories[0])


def main():
    # Setup folder
    start_data = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    folder_path = os.path.join(GENERATED_SCRIPTS_PATH, start_data)
    os.makedirs(folder_path, exist_ok=True)

    models = ["Salesforce/codegen-350M-mono", "Salesforce/codegen-2B-mono"]

    history = ["# Import libraries.\n\nimport numpy as np\n\n"]
    prompts = ["Assign the string \"abcde\" to a variable named \"my_string\".",
               "Lowercase the given string \"my_string\".",
               "Assign the distinct characters of the string to a variable named \"chars\".",
               "Sort these characters in alphabetical order.", "Print the resulting list of characters."]

    for model_name in models:
        p = Process(target=run_model, args=(history, prompts, model_name))
        p.start()
        p.join()
        p.close()


if __name__ == "__main__":
    main()
