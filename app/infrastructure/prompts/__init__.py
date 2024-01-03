import yaml
from os.path import abspath, dirname, join

current_directory = dirname(abspath(__file__))
with open(join(current_directory, "prompts.yaml"), encoding="utf-8") as file:
    MESSAGES = yaml.load(file, Loader=yaml.SafeLoader)


def recover_prompt(prompt_name: str, parameters: dict = {}) -> str:
    if prompt_name in MESSAGES:
        prompt = MESSAGES[prompt_name]
        for key, value in parameters.items():
            prompt = prompt.replace(f"{key}", value)
        return prompt
    raise ValueError(f"Prompt {prompt_name} not found")
