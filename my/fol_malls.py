from eval_fol_llm import TestLLMMALL
import json
from argparse import ArgumentParser
from utils import str_to_bool


INSTRUCTION_FOL = ("Translate the following natural language (NL) statement to a first-order logic (FOL) rule. "
                   "The answer should only contain a sentence in FOL, no other text. "
                   "Never abbreviate words when translating text into FOL.")

INSTRUCTION_FOL_LOGIC_LLAMA = ("Translate the following natural language (NL) statement "
                               "to a first-order logic (FOL) rule")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--path_to_test", type=str)
    parser.add_argument("--result_col_name", type=str)
    parser.add_argument("--llm_pattern_name", type=str, default="hermes")
    parser.add_argument("--instruction", type=str, default=INSTRUCTION_FOL)
    parser.add_argument("--temp_save_file_path", type=str)
    parser.add_argument("--continue_process", type=str_to_bool)
    parser.add_argument("--json_save_file_path", type=str)
    return parser.parse_args()


if __name__ == '__main__':
    test_llm = TestLLMMALL()
    args = parse_args()
    result_json = test_llm(
        path_to_test=args.path_to_test,
        llm_pattern_name=args.llm_pattern_name,
        instruction=args.instruction,
        temp_save_file_path=args.temp_save_file_path,
        continue_process=args.continue_process
    )
    with open(args.json_save_file_path, "w") as f:
        json.dump(result_json, f)
