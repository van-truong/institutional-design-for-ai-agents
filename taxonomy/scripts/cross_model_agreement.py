#!/usr/bin/env python3
"""Compare two independent GPT recodings with the final taxonomy coding.

Run from the repository root: python3 taxonomy/scripts/cross_model_agreement.py MODEL_A MODEL_B
Only writes coding/gpt/agreement.txt and coding/gpt/cross_model_disagreements.csv.
"""

import collections
import csv
import json
import sys
from pathlib import Path


TAX = Path(__file__).resolve().parents[1]
GPT = TAX / "coding" / "gpt"
KINDS = {"mechanism", "configuration", "phenomenon", "out_of_scope"}
REVIEW_COLUMNS = (
    "instance_id", "title", "url", "discipline", "description", "evidence",
    "p1", "p1_definition", "p2", "p2_definition", "decision", "verifier", "note",
)


def agreement(pairs):
    """Percent agreement and Cohen's kappa, as in pass2_compare.py."""
    n = len(pairs)
    if not n:
        return float("nan"), float("nan")
    observed = sum(a == b for a, b in pairs) / n
    left = collections.Counter(a for a, _ in pairs)
    right = collections.Counter(b for _, b in pairs)
    expected = sum(left[k] * right.get(k, 0) for k in left) / n**2
    return observed, (observed - expected) / (1 - expected) if expected < 1 else float("nan")


def fleiss(rows):
    """Fleiss' kappa for three labels on each row, with pooled marginals."""
    if not rows:
        return float("nan")
    counts = collections.Counter(label for row in rows for label in row)
    n = len(rows)
    p_bar = sum(sum(c * (c - 1) for c in collections.Counter(row).values()) / 6 for row in rows) / n
    p_expected = sum((count / (3 * n)) ** 2 for count in counts.values())
    return (p_bar - p_expected) / (1 - p_expected) if p_expected < 1 else float("nan")


def load_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def load_model(model, expected_ids):
    path = GPT / model
    rows = []
    for batch in range(1, 5):
        with (path / f"pass2_batch{batch}.json").open(encoding="utf-8") as stream:
            rows.extend(json.load(stream))
    ids = [row["instance_id"] for row in rows]
    if len(ids) != len(set(ids)) or set(ids) != expected_ids:
        raise ValueError(f"{model}: missing, extra, or duplicate instance IDs")
    return {row["instance_id"]: row for row in rows}


def single(row, valid, reference=False):
    key = "mechanism" if reference else "mechanism_id"
    return row.get("kind") == "mechanism" and row.get(key) in valid


def metric_line(label, pairs):
    pct, kap = agreement(pairs)
    return f"{label}: n={len(pairs)}, agreement={pct:.1%}, Cohen's kappa={kap:.3f}"


def main(model_a, model_b):
    if model_a == model_b:
        raise ValueError("The two model IDs must differ")
    # The GPT coders saw the four batch files, so compare on those instances only,
    # even if instances.csv has since grown.
    expected_ids = {row["instance_id"] for batch in range(1, 5)
                    for row in json.loads((TAX / "coding" / f"batch{batch}.json").read_text(encoding="utf-8"))}
    references = [row for row in load_csv(TAX / "instances.csv") if row["instance_id"] in expected_ids]
    if len(references) != len(expected_ids):
        raise ValueError("instances.csv is missing coded batch instances")
    book = {row["mechanism_id"]: row for row in load_csv(TAX / "codebook.csv")}
    codings = {name: load_model(name, expected_ids) for name in (model_a, model_b)}
    theme = lambda mid: book[mid]["theme_id"]
    lines = [f"Cross-model coding agreement: {model_a}, {model_b}",
             f"Instances: {len(references)}", ""]

    for name, coded in codings.items():
        matched = [(r, coded[r["instance_id"]]) for r in references]
        primary = [(r["mechanism"], q["mechanism_id"]) for r, q in matched
                   if single(r, book, True) and single(q, book)]
        lines.append(metric_line(f"{name} vs final, mechanism", primary))
        lines.append(metric_line(f"{name} vs final, theme",
                                 [(theme(a), theme(b)) for a, b in primary]))
        secondary = [(r["mechanism_p2"], q["mechanism_id"]) for r, q in matched
                     if r["kind"] == "mechanism" and r["mechanism_p2"] in book
                     and single(q, book)]
        lines.append(metric_line(f"{name} vs Claude pass 2, mechanism", secondary))
        lines.append(metric_line(f"{name} vs Claude pass 2, theme",
                                 [(theme(a), theme(b)) for a, b in secondary]))
        lines.append(metric_line(f"{name} vs final, kind",
                                 [(r["kind"], q["kind"]) for r, q in matched
                                  if r["kind"] in KINDS and q["kind"] in KINDS]))
        lines.append(metric_line(f"{name} vs final, evidence_type",
                                 [(r["evidence_type"], q["evidence_type"]) for r, q in matched
                                  if r["evidence_type"] and q["evidence_type"]]))
        fits = collections.Counter(q.get("fit", "") for q in coded.values())
        lines.append(f"{name} fit: good={fits['good']}, partial={fits['partial']}, misfit={fits['misfit']}")
        code_map = load_csv(GPT / name / "pass1_code_map.csv")
        new = [row for row in code_map if row["mechanism_id_or_NEW"] == "NEW"]
        lines.append(f"{name} NEW open-code levers: {len(new)}")
        for row in new:
            lines.append(f"  {row['open_code']} (n={row['n_instances']}): {row['rationale']}")
        used = {q.get("mechanism_id") for q in coded.values()}
        used.update(mid.strip() for q in coded.values() for mid in (q.get("secondary_ids") or "").split(";"))
        lines.append(f"{name} unused mechanisms: {', '.join(sorted(book.keys() - used)) or 'none'}")
        lines.append("")

    paired = [(codings[model_a][r["instance_id"]], codings[model_b][r["instance_id"]])
              for r in references]
    pair_mechanism = [(a["mechanism_id"], b["mechanism_id"]) for a, b in paired
                      if single(a, book) and single(b, book)]
    lines.append(metric_line(f"{model_a} vs {model_b}, mechanism", pair_mechanism))
    lines.append(metric_line(f"{model_a} vs {model_b}, theme",
                             [(theme(a), theme(b)) for a, b in pair_mechanism]))
    triples = [(r["mechanism"], codings[model_a][r["instance_id"]]["mechanism_id"],
                codings[model_b][r["instance_id"]]["mechanism_id"])
               for r in references if single(r, book, True)
               and single(codings[model_a][r["instance_id"]], book)
               and single(codings[model_b][r["instance_id"]], book)]
    lines.append(f"Final + {model_a} + {model_b}, Fleiss' kappa: n={len(triples)}, kappa={fleiss(triples):.3f}")

    disagreements = []
    for r in references:
        if not single(r, book, True):
            continue
        a, b = (codings[name][r["instance_id"]] for name in (model_a, model_b))
        if not (single(a, book) and single(b, book)):
            continue
        x, y, z = r["mechanism"], a["mechanism_id"], b["mechanism_id"]
        if y == z != x:
            category = "GPT consensus differs from final"
            proposed = y
            definition = book[y]["definition"]
        elif len({x, y, z}) == 3:
            category = "all three differ"
            proposed = f"A: {y} / B: {z}"
            definition = f"A: {book[y]['definition']} / B: {book[z]['definition']}"
        else:
            continue
        disagreements.append({
            **{field: r.get(field, "") for field in REVIEW_COLUMNS[:6]},
            "p1": x, "p1_definition": book[x]["definition"],
            "p2": proposed, "p2_definition": definition,
            "decision": "", "verifier": "", "note": category,
        })
    lines.append(f"Disagreement review rows: {len(disagreements)}")
    (GPT / "agreement.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (GPT / "cross_model_disagreements.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=REVIEW_COLUMNS)
        writer.writeheader()
        writer.writerows(disagreements)
    print("\n".join(lines))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: cross_model_agreement.py MODEL_A MODEL_B")
    main(sys.argv[1], sys.argv[2])
