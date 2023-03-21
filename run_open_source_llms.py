from multiprocessing import Process

from tools.hf_model_utils import load_model, generate, truncate


def run_model(histories, prompt_list, model_name):
    print("Loading model...")
    tokenizer, model = load_model(model_name, "cuda:0", "float32")
    print("Loading finished")

    def _wrap(p):
        return f"# {p}\n"

    for i, prompt in enumerate(prompt_list):
        histories = [h + _wrap(prompt) for h in histories]
        completions = generate(histories, tokenizer, model, "cuda:0")
        histories = [h + f"{truncate(c, model_name)}\n\n" for h, c in zip(histories, completions)]

        print("-" * 10)
        print(i)
        print("-" * 10)
        print(histories[0])
        print("-" * 10)


def main():
    models = ["Salesforce/codegen-350M-mono", "Salesforce/codegen-2B-mono"]

    history = ["# Import libraries.\n\nimport numpy as np\n\n"]
    prompts = ["Assign the string \"abcde\" to a variable named \"my_string\".",
               "Lowercase the given string \"my_string\".",
               "Assign the distinct characters of the string to a variable named \"chars\".",
               "Sort these characters in alphabetical order.", "Print the resulting list of characters."]

    for model_name in models:
        input(f"Start run with model {model_name}")
        p = Process(target=run_model, args=(history, prompts, model_name))
        p.start()


if __name__ == "__main__":
    main()
