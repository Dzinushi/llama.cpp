fol_instruction="Translate the following natural language (NL) statement to a first-order logic (FOL) rule.
For answer you can usage next specific symbols: ¬, ∧, ∨, →, ⊕, ∀, ∃. The answer should only
contain a sentence in FOL, no other text. Here is some example of FOL rules:
∀x (Vacation(x) ∧ Relaxing(x) → (BeautifulScenery(x) ∧ EnjoyableActivities(x)))
∀x (Flower(x) ∧ SingleCotyledon(x) ∧ ParallelVeinedLeaves(x) ∧ FlowerPartsInMultiplesOfThree(x) → Monocot(x))
∀x (Fabric(x) ∧ Lightweight(x) ∧ Breathable(x) ∧ AbsorbsMoisture(x) → SuitableForAthleticWear(x))"

description_logic_instruction="Translate the following natural language (NL) statement to a attributive language with
complement (ALC) rules. The answer should only contain a sentence in ALC, no other text."

graph_query_logic="Translate the following natural language (NL) statement to Graph query (GQ). The answer should only contain GP, no other text."

python -m fol_terminal \
    --llm_pattern_name="logic_llama" \
    --instruction="$graph_query_logic" \
    --use_correct_fol="no"
