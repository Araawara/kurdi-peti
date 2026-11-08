"""دروستکردنی فەرهەنگی زاراوەکانی ڕووکار (ئینگلیزی ← کوردی) بۆ references/ui_terms.tsv.

Sources, by priority:
  1. kurdi-peti: the reviewed UI table in references/software.md
  2. firefox:    Mozilla Firefox Central Kurdish localization (MPL-2.0), pre-paired by harvest_ui.py

python tools/build_ui_terms.py PATH/TO/ui_pure.tsv
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "kurdi-peti" / "references"
spec = importlib.util.spec_from_file_location("check", ROOT / "skills" / "kurdi-peti" / "scripts" / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


def curated():
    """Rows of the UI table in software.md; 'A / B' cells are split into pairs."""
    out = {}
    for line in (REFS / "software.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 2 or not re.search("[A-Za-z]", cells[0]) or cells[0] in ("ئینگلیزی",):
            continue
        ens = [e.strip() for e in cells[0].split("/")]
        kus = [k.strip() for k in cells[1].split("/")]
        if len(ens) == len(kus):
            for e, k in zip(ens, kus):
                out[re.sub(r"[.…?]+$", "", e).lower()] = k
    return out


def main(firefox_tsv):
    entries = check.compile_entries(json.loads((REFS / "glossary.json").read_text(encoding="utf-8"))["entries"], False)
    terms = {e: (k, "kurdi-peti") for e, k in curated().items()}
    dropped = 0
    for line in Path(firefox_tsv).read_text(encoding="utf-8").splitlines():
        en, ku = line.split("\t")
        if en in terms:
            continue
        if check.check_text(ku, entries) or "ـ" in ku:  # any loanword or spelling issue: skip
            dropped += 1
            continue
        terms[en] = (ku, "firefox")
    rows = sorted(terms.items())
    header = ("# زاراوەکانی ڕووکار: ئینگلیزی ← کوردیی پەتی\n"
              "# سەرچاوە: kurdi-peti (پێداچوونەوەکراو، لە پێشترە) و firefox "
              "(وەرگێڕانی کوردیی Mozilla Firefox، مۆڵەتی MPL-2.0)\n"
              "english\tkurdish\tsource\n")
    (REFS / "ui_terms.tsv").write_text(header + "\n".join(f"{e}\t{k}\t{s}" for e, (k, s) in rows) + "\n", encoding="utf-8")
    print(f"ui_terms.tsv: {len(rows)} زاراوە ({sum(s == 'kurdi-peti' for _, (_, s) in rows)} kurdi-peti)، {dropped} لابران")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1])
