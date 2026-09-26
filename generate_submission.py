"""
Generate submission.jsonl for the 30 canonical test pairs.
Produces the exact format required by Section 7.2 of challenge-brief.md:
{"test_id": "T01", "body": "...", "cta": "...", "send_as": "...", "suppression_key": "...", "rationale": "..."}
"""

import json
from pathlib import Path
from bot import compose

ROOT_DIR = Path(__file__).parent
DATASET_DIR = ROOT_DIR / "dataset" / "expanded"
OUT_FILE = ROOT_DIR / "submission.jsonl"

def main():
    with open(DATASET_DIR / "test_pairs.json") as fp:
        pairs = json.load(fp)["pairs"]

    categories = {}
    for f in (DATASET_DIR / "categories").glob("*.json"):
        with open(f) as fp:
            d = json.load(fp)
            categories[d["slug"]] = d

    merchants = {}
    for f in (DATASET_DIR / "merchants").glob("*.json"):
        with open(f) as fp:
            d = json.load(fp)
            merchants[d["merchant_id"]] = d

    customers = {}
    for f in (DATASET_DIR / "customers").glob("*.json"):
        with open(f) as fp:
            d = json.load(fp)
            customers[d["customer_id"]] = d

    triggers = {}
    for f in (DATASET_DIR / "triggers").glob("*.json"):
        with open(f) as fp:
            d = json.load(fp)
            triggers[d["id"]] = d

    entries = []
    for pair in pairs:
        t_id = pair["trigger_id"]
        m_id = pair["merchant_id"]
        c_id = pair.get("customer_id")
        test_id = pair["test_id"]

        trigger = triggers[t_id]
        merchant = merchants[m_id]
        customer = customers.get(c_id) if c_id else None
        category = categories.get(merchant.get("category_slug", ""), {})

        result = compose(category, merchant, trigger, customer)
        entry = {
            "test_id": test_id,
            "body": result["body"],
            "cta": result["cta"],
            "send_as": result["send_as"],
            "suppression_key": result["suppression_key"],
            "rationale": result["rationale"]
        }
        entries.append(entry)

    with open(OUT_FILE, "w", encoding="utf-8") as fp:
        for entry in entries:
            fp.write(json.dumps(entry, ensure_ascii=False) + "\n")

    print(f"Generated {len(entries)} lines in {OUT_FILE}")

if __name__ == "__main__":
    main()
