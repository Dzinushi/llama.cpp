from eval_fol_llm import TestLLMTerminal
from argparse import ArgumentParser
from utils import str_to_bool


INSTRUCTION_FOL = (
    "Translate the following natural language (NL) statement to a first-order logic (FOL) rule. "
    "The answer should only contain a sentence in FOL, no other text. "
    "Never abbreviate words when translating text into FOL."
)

INSTRUCTION_FOL_LOGIC_LLAMA = (
    "Translate the following natural language (NL) statement " "to a first-order logic (FOL) rule"
)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--llm_pattern_name", type=str, default="hermes")
    parser.add_argument("--instruction", type=str, default=INSTRUCTION_FOL)
    parser.add_argument("--filter_prompt_end", type=str, default="<|im_end|>")
    parser.add_argument("--use_correct_fol", type=str_to_bool, default=False)
    return parser.parse_args()


if __name__ == "__main__":
    test_llm = TestLLMTerminal()
    args = parse_args()
    test_llm(
        llm_pattern_name=args.llm_pattern_name,
        instruction=args.instruction,
        use_correct_fol=args.use_correct_fol,
        filter_prompt_end=args.filter_prompt_end,
    )
