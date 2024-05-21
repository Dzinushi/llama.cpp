from test_fol_llm import TestLLMMALL
import json


INSTRUCTION_FOL = ("Translate the following natural language (NL) statement to a first-order logic (FOL) rule. "
                   "The answer should only contain a sentence in FOL, no other text. "
                   "Never abbreviate words when translating text into FOL.")

INSTRUCTION_FOL_LOGIC_LLAMA = ("Translate the following natural language (NL) statement "
                               "to a first-order logic (FOL) rule")


if __name__ == '__main__':
    test_llm = TestLLMMALL()
    result_json = test_llm(
        path_to_test="/Users/egormihno/Develop/Python/Third/llama.cpp/my/datasets/MALLS-v0/MALLS-v0.1-test.json",
        llm_prompt_name="logic_llama",
        instruction=INSTRUCTION_FOL_LOGIC_LLAMA,
        temp_save_file_path="/Users/egormihno/Develop/Python/Third/llama.cpp/my/data/malls_logic_llama_13b_Q5_K_M.txt",
        continue_process=True
    )
    with open("/Users/egormihno/Develop/Python/Third/llama.cpp/my/data/malls_logic_llama_13b_Q5_K_M.json", "w") as f:
        json.dump(result_json, f)
