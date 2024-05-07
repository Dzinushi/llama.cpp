import requests


URL = "http://localhost:5002/completion"
INSTRUCTION_FOL = "Translate the following sentence from natural language form into first-order logic (FOL). Provide a logical representation that captures the meaning and structure of the sentence while preserving its logical consistency. Remember to define the relevant domain and specify any necessary predicates, functions, and constants. You may assume a standard interpretation of logical connectives (e.g., conjunction, disjunction, implication) and quantifiers (e.g., universal, existential). The answer should only contain a sentence in , no other text."


def from_csv(path: str) -> str:
    with open(path, "r") as f:
        text = f.read()
    return text


def llm_output(instruction: str, user_input: str):
    pattern = (f"<|im_start|>system\n{instruction}<|im_end|>\n"
               f"<|im_start|>user\n{user_input}<|im_end|>\n"
               f"<|im_start|>assistant\n")
    data = {
        "prompt": pattern,
        "temperature": 0,
        "n_predict": 256,
    }
    data_revive = {
        "prompt": "!",
        "temperature": 0,
        "n_predict": 1,
    }
    requests.post(url=URL, json=data_revive)
    response = requests.post(url=URL, json=data).json()
    return response


def console_cycle():
    while True:
        response = llm_output(instruction=INSTRUCTION_FOL, user_input=input("Input: "))
        content = response["content"]
        print(f"Output: {content}")


if __name__ == '__main__':
    texts = from_csv("/home/haaohi/Загрузки/fol_text.txt")
    list_text = texts.split("\n")
    for index, text in enumerate(list_text):
        if len(text) != 0:
            content = llm_output(instruction=INSTRUCTION_FOL, user_input=text)["content"]
            output = content[:content.find("<|im_end|>")]
            print(f"{index+1}) {text}\nOutput: {output}")
