import pandas as pd
import requests
from tqdm import tqdm
from typing import Callable


URL = "http://localhost:5002/completion"
# INSTRUCTION_FOL = ("Translate the following sentence from natural language form into first-order logic (FOL). "
#                    "Provide a logical representation that captures the meaning and structure of the sentence "
#                    "while preserving its logical consistency. Remember to define the relevant domain and specify "
#                    "any necessary predicates, functions, and constants. You may assume a standard interpretation "
#                    "of logical connectives (e.g., conjunction, disjunction, implication) and quantifiers (e.g., "
#                    "universal, existential). The answer should only contain a sentence in FOL, no other text. "
#                    "Never abbreviate words when translating text into FOL.")

INSTRUCTION_FOL = ("Translate the following natural language (NL) statement to a first-order logic (FOL) rule. "
                   "The answer should only contain a sentence in FOL, no other text. "
                   "Never abbreviate words when translating text into FOL.")

INSTRUCTION_FOL_QUALITY = ("Evaluate the quality, accuracy and completeness of the translation from sentences from"
                           " natural language text (NL) to first order logic (FOL) and in your answer give a score"
                           " from 0 to 10, where 0 is a complete inconsistency and 10 is perfect.")


INSTRUCTION_FOL_LOGIC_LLAMA = "Translate the following natural language (NL) statement to a first-order logic (FOL) rule"


default_pattern = lambda instruction, user_input: (f"<|im_start|>system\n{instruction}<|im_end|>\n"
                                                   f"<|im_start|>user\n{user_input}<|im_end|>\n"
                                                   f"<|im_start|>assistant\n")

logic_llama_pattern = lambda instruction, user_input: (f"### Instruction: {instruction}\n### NL: {user_input}\n### FOL: ")


def from_csv(path: str) -> str:
    with open(path, "r") as f:
        text = f.read()
    return text


def llm_output(instruction: str, user_input: str, llm_pattern: Callable = default_pattern):
    data = {
        "prompt": llm_pattern(instruction, user_input),
        "temperature": 0.1,
        "n_predict": 256,
        "top_p": 0.75,
        "top_k": 40,
    }
    data_revive = {
        "prompt": "!",
        "temperature": 0,
        "n_predict": 1,
    }
    requests.post(url=URL, json=data_revive)
    response = requests.post(url=URL, json=data).json()
    return response


def console_cycle(instruction: str, llm_pattern: Callable = default_pattern) -> None:
    while True:
        response = llm_output(instruction=instruction, user_input=input("Input: "), llm_pattern=llm_pattern)
        content = response["content"]
        print(f"Output: {content}")


def from_txt(path: str = "fol_text.txt", llm_pattern: Callable = default_pattern) -> None:
    texts = from_csv(path)
    list_text = texts.split("\n")
    for index, text in enumerate(list_text):
        if len(text) != 0:
            content = llm_output(instruction=INSTRUCTION_FOL, user_input=text, llm_pattern=llm_pattern)["content"]
            output = content[:content.find("<|im_end|>")]
            print(f"{index+1}) {text}\nOutput: {output}")


def from_pandas_csv(path: str, result_col_name: str, index_col: str = None, text_col_name: str = "text", delimiter: str = ";", instruction: str = INSTRUCTION_FOL_QUALITY, llm_pattern: Callable = default_pattern):
    df = pd.read_csv(path, index_col=index_col, delimiter=delimiter)
    result = []
    with tqdm(total=df.shape[0]) as pb:
        for index, row in df.iterrows():
            text = row[text_col_name]
            content = llm_output(instruction=instruction, user_input=text, llm_pattern=llm_pattern)["content"]
            output = content[:content.find("<|im_end|>")]
            result.append(output)
            pb.update(1)
    num_columns = len(df.columns)
    df.insert(num_columns, result_col_name, result, True)
    return df


if __name__ == '__main__':
    # df = from_pandas_csv(
    #     path="fol_logic_llama_instruction.csv",
    #     result_col_name="Hermes-2-Pro-Llama-3-8B-Q6_K",
    #     index_col="index",
    #     text_col_name="text",
    #     instruction=INSTRUCTION_FOL_LOGIC_LLAMA,
    #     llm_pattern=default_pattern
    # )
    # df.to_csv("fol_logic_llama_instruction.csv", sep=";")
    console_cycle(instruction=INSTRUCTION_FOL_LOGIC_LLAMA,
                  llm_pattern=default_pattern)
