import json


def transform_formula_2dict(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        original_formulas = json.load(f)

    original_formulas = dict(
        sorted(original_formulas.items(), key=lambda item: len(item[1]))
    )
    transformed_formulas = {}

    for key, formula_data in original_formulas.items():
        transformed_formulas[key] = {"data": formula_data, "description": None}

    json.dump(transformed_formulas, open(file_path, "w"))


def sort_formulas(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        original_formulas = json.load(f)

    original_formulas = dict(
        sorted(original_formulas.items(), key=lambda item: len(item[1]["data"]))
    )
    json.dump(original_formulas, open(file_path, "w"))


if __name__ == "__main__":
    transform_formula_2dict("triangle_formula.json")
    # sort_formulas("triangle_formula.json")
