from llama_server_api import LlamaServerSimpleAPI
from llm_pattern_builder import PromptPatternBuilder
from metrics_timer import MetricLE, MetricBLEU
import pandas as pd
from tqdm import tqdm
import json
from typing import List, Dict, Any, Union
from dataclasses import dataclass
from utils import prompt_end_filter


def mean(data: List) -> float:
    return sum(data) / len(data)


class TestLLM:
    def __init__(self):
        self.le = MetricLE()
        self.bleu = MetricBLEU()

    def __call__(self, *args, **kwargs):
        pass


class TestLLMTerminal(TestLLM):
    def __call__(
        self, llm_pattern_name: str, instruction: str = "", use_correct_fol: bool = False, filter_prompt_end: str = None
    ):
        simple_api_server = LlamaServerSimpleAPI()
        prompt_fn = PromptPatternBuilder.create(llm_pattern_name)
        while True:
            # example: "I see John"
            user_input = input("User: ")
            response = simple_api_server(prompt_fn(instruction=instruction, user_input=user_input))
            llm_fol = response["content"]
            llm_fol = prompt_end_filter(output=llm_fol, filter_prompt_end=filter_prompt_end)
            if use_correct_fol:
                # llm_fol: "∃x (Person(x) ∧ Sees(x, John))"
                # correct_fol: "∃x (I(x) → Sees(x, John))"
                correct_fol = input("Correct-FOL-rule: ")
                le = self.le(true_text_FOL=correct_fol, pred_text_FOL=llm_fol)
                bleu = self.bleu(true_seq=correct_fol, pred_seq=llm_fol)
                print(f"Output: {llm_fol}\nBLEU: {bleu:.3f}, LE: {le:.3f}")
            else:
                print(f"Output: {llm_fol}")


class TestLLMCSV(TestLLM):
    def __call__(
        self,
        path: str,
        result_col_name: str,
        llm_pattern_name: str,
        instruction: str,
        text_column: str,
        correct_fol_column: str = None,
        index_column: str = None,
        delimiter: str = ";",
        filter_prompt_end: str = None,
    ) -> pd.DataFrame:
        simple_api_server = LlamaServerSimpleAPI()
        prompt_fn = PromptPatternBuilder.create(llm_pattern_name)
        df = pd.read_csv(path, index_col=index_column, delimiter=delimiter)
        result_fol = []
        result_bleu = []
        result_le = []
        with tqdm(total=df.shape[0]) as pb:
            for index, row in df.iterrows():
                text = row[text_column]
                llm_fol = simple_api_server(prompt_fn(instruction=instruction, user_input=text))["content"]
                llm_fol = prompt_end_filter(output=llm_fol, filter_prompt_end=filter_prompt_end)
                if correct_fol_column is not None:
                    correct_fol = row[correct_fol_column]
                    le = self.le(true_text_FOL=correct_fol, pred_text_FOL=llm_fol)
                    bleu = self.bleu(true_seq=correct_fol, pred_seq=llm_fol)
                    result_bleu.append(bleu)
                    result_le.append(le)
                result_fol.append(llm_fol)
                pb.update(1)
        num_columns = len(df.columns)
        df.insert(num_columns, result_col_name, result_fol, True)
        if correct_fol_column is not None:
            df.insert(num_columns, f"{result_col_name}_bleu", result_bleu, True)
            df.insert(num_columns, f"{result_col_name}_le", result_le, True)
        return df


class TestLLMMALL(TestLLM):
    @dataclass(frozen=True)
    class TempFileStructure:
        NL = "NL"
        FOL = "FOL"
        LLM_FOL = "LLM_FOL"
        BLEU = "BLEU"
        LE = "LE"

    def _restore_from_temp_file(self, filepath: str, separator: str = ":") -> Dict[str, Any]:
        tfs = self.TempFileStructure
        with open(filepath, "r") as f:
            data = f.read()
            data_dict = {
                tfs.NL: [],
                tfs.FOL: [],
                tfs.LLM_FOL: [],
                tfs.BLEU: [],
                tfs.LE: [],
            }
            list_tfs = [tfs.NL, tfs.FOL, tfs.LLM_FOL, tfs.BLEU, tfs.LE]
            find_prev = 0
            repeat = True
            while repeat:
                for i in range(len(list_tfs) - 1):
                    tag = list_tfs[i]
                    next_tag = list_tfs[i + 1]
                    left = data.find(f"{tag}{separator}", find_prev) + len(tag) + len(separator)
                    right = data.find(f"{next_tag}{separator}", left)
                    data_dict[tag].append(data[left:right])
                    find_prev = left
                if data.find(f"{tfs.NL}{separator}", find_prev) == -1:
                    repeat = False
                    left, _ = self._next_left_right_data_dict(
                        data=data, separator=f"{separator}", tag=tfs.LE, next_tag=tfs.NL, find_prev=find_prev
                    )
                    right = len(data)
                else:
                    left, right = self._next_left_right_data_dict(
                        data=data, separator=f"{separator}", tag=tfs.LE, next_tag=tfs.NL, find_prev=find_prev
                    )
                data_dict[tfs.LE].append(data[left : right - 1])
                find_prev = left
            data_dict[tfs.BLEU] = [float(item) for item in data_dict[tfs.BLEU]]
            data_dict[tfs.LE] = [float(item) for item in data_dict[tfs.LE]]
        return data_dict

    @staticmethod
    def _next_left_right_data_dict(data: str, separator: str, tag: str, next_tag: str, find_prev: int):
        left = data.find(f"{tag}{separator}", find_prev) + len(tag) + len(separator)
        right = data.find(f"{next_tag}{separator}", left)
        return left, right

    def _write_to_temp_file(
        self, f, nl: str, fol: str, llm_fol: str, bleu: float, le: float, separator: str = ":"
    ) -> None:
        tfs = self.TempFileStructure
        f.write(
            f"{tfs.NL}{separator}{nl}"
            f"{tfs.FOL}{separator}{fol}"
            f"{tfs.LLM_FOL}{separator}{llm_fol}"
            f"{tfs.BLEU}{separator}{bleu}"
            f"{tfs.LE}{separator}{le}\n"
        )

    def __call__(
        self,
        path_to_test: str,
        llm_pattern_name: str,
        instruction: str,
        temp_save_file_path: str,
        filter_prompt_end: str = None,
        continue_process: bool = False,
        separator: str = ":",
    ) -> Dict[str, Union[str, float]]:
        """
        Temp save file path need for saving NL, FOL, LLM_FOL, BLEU and LE info for every processed row from MALL dataset
        """
        tfs = self.TempFileStructure
        with open(path_to_test, "r") as f:
            data = json.load(f)
        simple_server_api = LlamaServerSimpleAPI()
        prompt_fn = PromptPatternBuilder().create(llm_pattern_name)
        data_dict = {tfs.NL: [], tfs.FOL: [], tfs.LLM_FOL: [], tfs.BLEU: [], tfs.LE: []}
        skip_count = 0
        if continue_process:
            data_dict = self._restore_from_temp_file(filepath=temp_save_file_path, separator=separator)
            skip_count = len(data_dict[tfs.NL])
            print(f"Continue from {skip_count} row")
        with tqdm(total=len(data), bar_format="{l_bar}{bar:10}{r_bar}{bar:-10b}") as pb:
            pb.update(skip_count)
            with open(temp_save_file_path, "a+") as temp_f:
                for item in data[skip_count:]:
                    text = item["NL"]
                    correct_fol = item["FOL"]
                    llm_fol = simple_server_api(prompt_fn(instruction=instruction, user_input=text))["content"]
                    llm_fol = prompt_end_filter(output=llm_fol, filter_prompt_end=filter_prompt_end)
                    le = self.le(true_text_FOL=correct_fol, pred_text_FOL=llm_fol)
                    bleu = self.bleu(true_seq=correct_fol, pred_seq=llm_fol)
                    data_dict[tfs.NL].append(text)
                    data_dict[tfs.FOL].append(correct_fol)
                    data_dict[tfs.LLM_FOL].append(llm_fol)
                    data_dict[tfs.BLEU].append(bleu)
                    data_dict[tfs.LE].append(le)
                    self._write_to_temp_file(temp_f, nl=text, fol=correct_fol, llm_fol=llm_fol, bleu=bleu, le=le)
                    pb.set_postfix_str(
                        f"\t(bleu {mean(data_dict[tfs.BLEU]):.3f}, " f"le: {mean(data_dict[tfs.LE]):.3f})"
                    )
                    pb.update(1)
        return data_dict
