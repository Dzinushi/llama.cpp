source .venv/bin/activate
instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule."
python -m fol_terminal \
    --llm_pattern_name="logic_llama" \
    --instruction="$instruction" \
    --use_correct_fol="no"
