import pandas as pd
import requests
from tqdm import tqdm


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


def from_txt(path: str = "fol_text.txt"):
    texts = from_csv(path)
    list_text = texts.split("\n")
    for index, text in enumerate(list_text):
        if len(text) != 0:
            content = llm_output(instruction=INSTRUCTION_FOL, user_input=text)["content"]
            output = content[:content.find("<|im_end|>")]
            print(f"{index+1}) {text}\nOutput: {output}")


def from_pandas_csv(path: str, result_col_name: str, index_col: str = None, text_col_name: str = "text", delimiter: str = ";"):
    df = pd.read_csv(path, index_col=index_col, delimiter=delimiter)
    result = []
    with tqdm(total=df.shape[0]) as pb:
        for index, row in df.iterrows():
            text = row[text_col_name]
            content = llm_output(instruction=INSTRUCTION_FOL, user_input=text)["content"]
            output = content[:content.find("<|im_end|>")]
            result.append(output)
            pb.update(1)
    num_columns = len(df.columns)
    df.insert(num_columns, result_col_name, result, True)
    return df


if __name__ == '__main__':
    df = from_pandas_csv(
        path="fol.csv",
        result_col_name="Hermes-2-Pro-Mistral-7B.Q6_K",
        index_col="index",
        text_col_name="text"
    )
    df.to_csv("fol_result.csv")
