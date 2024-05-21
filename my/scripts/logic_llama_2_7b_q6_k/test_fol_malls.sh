source .venv/bin/activate
instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule."
python -m fol_malls \
    --path_to_test="./datasets/MALLS-v0/MALLS-v0.1-test.json" \
    --llm_pattern_name="logic_llama" \
    --instruction="$instruction" \
    --temp_save_file_path="./data/malls-logic-llama-2-7b-Q6_K.txt" \
    --continue_process="no" \
    --csv_save_file_path="./data/malls-logic-llama-2-7b-Q6_K.csv"
