from typing import Callable
from abc import ABC


class PromptPatternBase(ABC):
    @staticmethod
    def prompt(user_input: str, instruction: str = ""):
        pass


class HermesPromptPattern(PromptPatternBase):
    @staticmethod
    def prompt(user_input: str, instruction: str = "") -> str:
        return (f"<|im_start|>system\n{instruction}<|im_end|>\n"
                f"<|im_start|>user\n{user_input}<|im_end|>\n"
                f"<|im_start|>assistant\n")


class LogicLLaMAPattern(PromptPatternBase):
    @staticmethod
    def prompt(user_input: str, instruction: str = ""):
        return (f"### Instruction: {instruction}\n"
                f"### NL: {user_input}\n"
                f"### FOL: ")


class PromptPatternBuilder:
    pattern_map = {
        "hermes": HermesPromptPattern.prompt,
        "logic_llama": LogicLLaMAPattern.prompt
    }

    @staticmethod
    def create(name: str) -> Callable:
        fn_callable = PromptPatternBuilder.pattern_map.get(name)
        if name is None:
            raise ValueError(f"Name {name} not found in {PromptPatternBuilder.pattern_map.keys()}")
        return fn_callable
