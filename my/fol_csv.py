from eval_fol_llm import TestLLMCSV
from argparse import ArgumentParser


INSTRUCTION_FOL = (
    "Translate the following natural language (NL) statement to a first-order logic (FOL) rule. "
    "The answer should only contain a sentence in FOL, no other text. "
    "Never abbreviate words when translating text into FOL."
)

INSTRUCTION_FOL_LOGIC_LLAMA = (
    "Translate the following natural language (NL) statement " "to a first-order logic (FOL) rule"
)


def parse_csv_args():
    parser = ArgumentParser()
    parser.add_argument("--path", type=str)
    parser.add_argument("--result_col_name", type=str)
    parser.add_argument("--llm_pattern_name", type=str, default="hermes")
    parser.add_argument("--instruction", type=str, default=INSTRUCTION_FOL)
    parser.add_argument("--text_column", type=str, default="text")
    parser.add_argument("--correct_fol_column", type=str, default=None)
    parser.add_argument("--index_column", type=str, default="index")
    parser.add_argument("--delimiter", type=str, default=";")
    parser.add_argument("--filter_prompt_end", type=str, default="<|im_end|>")
    parser.add_argument("--save_path", type=str)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_csv_args()
    test_llm = TestLLMCSV()
    df = test_llm(
        path=args.path,
        result_col_name=args.result_col_name,
        llm_pattern_name=args.llm_pattern_name,
        instruction=args.instruction,
        text_column=args.text_column,
        correct_fol_column=args.correct_fol_column,
        index_column=args.index_column,
        delimiter=args.delimiter,
        filter_prompt_end=args.filter_prompt_end,
    )
    df.to_csv(path_or_buf=args.save_path, sep=args.delimiter)
