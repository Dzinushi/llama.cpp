source .venv/bin/activate
instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule."
python -m fol_csv \
    --path="./data/fol_text.csv" \
    --result_col_name="Logic-Llama-2-7B-Q6_K" \
    --llm_pattern_name="logic_llama" \
    --instruction="$instruction" \
    --text_column="text" \
    --index_column="index" \
    --delimiter=";" \
    --save_path="./data/fol_logic-llama_2-7b.csv"
