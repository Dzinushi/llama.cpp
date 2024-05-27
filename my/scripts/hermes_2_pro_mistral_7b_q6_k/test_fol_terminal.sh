fol_instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule. The answer
should only contain a sentence in FOL, no other text. Never abbreviate any entities, relations in translated FOL."
graph_query_logic="Translate the following natural language (NL) statement to Graph query (GQ). The answer should only contain GP, no other text."
fol_2_instruction="Identify key predicates and their arguments in natural language (NL) text. Convert NL into
expressions in the language of first-order logic (FOL) using the selected predicates and keywords. Use the quantifiers
of existence ∃ and universality ∀. Don't use key predicates with quantifiers, always use variables like x or y. For every
new object use new variable name. Example: \nNL: Me and cat like to go for walks.\nFOL: ∃x∃y (Me(x) ∧ Cat(y) → Walk(x,y)).
If it's possible, always use specific symbols: ¬, ∧, ∨, →, ⊕. Don't use symbol =, !=, >, <, >=, <=.
The answer should only contain a sentence in FOL, no other text."
python -m fol_terminal \
    --llm_pattern_name="hermes" \
    --instruction="$fol_2_instruction" \
    --use_correct_fol="no" \
    --filter_prompt_end="<|im_end|>"
