source .venv/bin/activate
instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule.
The answer should only contain a sentence in FOL, no other text.
Never abbreviate any variables, functions and predicates when translating in FOL."
gemini_instruction="To translate natural language statements into first-order logic (FOL) expressions, identify key
elements like predicates, arguments, quantifiers, and connectives. Choose appropriate FOL symbols and define their
meaning. Break down the sentence structure and represent each component using FOL symbols and predicates. Combine the
components using logical connectives to form the final FOL expression. Consider tense, modality, ambiguity, and
implicit information. Test and refine the translation to ensure accuracy and clarity. These instructions provide a
general framework for translating natural language to FOL, with specific details varying depending on the complexity of
the statement and the capabilities of the language model. A good understanding of both natural language and FOL is
essential for accurate and meaningful translations. The answer should only contain a sentence in FOL, no other text. "
gpt40_instruction="To translate natural text into first-order logic (FOL), follow these steps: Identify the key
concepts, objects, and their properties in the text. Define predicates to represent properties and relations between
objects. Translate statements into logical expressions using quantifiers (∀ for 'for all' and ∃ for 'there exists')
and logical connectives (such as ∧ for 'and', ∨ for 'or', → for 'implies', and ¬ for 'not'). Ensure each predicate
clearly corresponds to a concept or relationship in the text. Finally, combine these logical expressions to represent
the original text's meaning accurately.To translate natural text into first-order logic (FOL), follow these steps:
Identify the key concepts, objects, and their properties in the text. Define predicates to represent properties and
relations between objects. Translate statements into logical expressions using quantifiers (∀ for 'for all' and ∃ for
'there exists') and logical connectives (such as ∧ for 'and', ∨ for 'or', → for 'implies', and ¬ for 'not'). Ensure
each predicate clearly corresponds to a concept or relationship in the text. Finally, combine these logical expressions
to represent the original text's meaning accurately. The answer should only contain a sentence in FOL, no other text."
python -m fol_malls \
    --path_to_test="./datasets/MALLS-v0/MALLS-v0.1-test.json" \
    --llm_pattern_name="hermes" \
    --instruction="$instruction" \
    --filter_prompt_end="<|im_end|>" \
    --temp_save_file_path="./data/malls_hermes_2_pro_llama_3_8b_Q6_K.txt" \
    --continue_process="yes" \
    --csv_save_file_path="./data/malls_hermes_2_pro_llama_3_8b_Q6_K.csv"
