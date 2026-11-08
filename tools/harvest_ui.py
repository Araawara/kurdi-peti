"""Pair Firefox en-US and ckb strings into a UI term list (English -> Sorani)."""
import collections
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
EN, CKB = HERE / "ff-en", HERE / "ff-ckb" / "ckb"
spec = importlib.util.spec_from_file_location("check", r"C:\Users\awara\Desktop\Kurdish_Project\skills\kurdi-peti\scripts\check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

SKIP = re.compile(r"regionNames|languageNames|charsetMenu|intl\.properties|mathfont|accessibility/|crashreporter|mozStorage|dom/chrome/layout")
MSG = re.compile(r"^(-?[A-Za-z][\w-]*)\s*=\s*(.*)$")
ATTR = re.compile(r"^\s+\.([\w-]+)\s*=\s*(.*)$")


def parse_ftl(path):
    out, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = MSG.match(line)
        if m:
            cur = m.group(1)
            if m.group(2).strip():
                out[cur] = m.group(2).strip()
            continue
        m = ATTR.match(line)
        if m and cur:
            out[f"{cur}.{m.group(1)}"] = m.group(2).strip()
    return out


def parse_properties(path):
    out = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line and not line.lstrip().startswith(("#", "!")):
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def strings(root):
    res = {}
    for f in root.rglob("*"):
        if f.suffix == ".ftl":
            parsed = parse_ftl(f)
        elif f.suffix == ".properties":
            parsed = parse_properties(f)
        else:
            continue
        rel = f.relative_to(root).as_posix()
        if SKIP.search(rel):
            continue
        for k, v in parsed.items():
            res[(rel, k)] = v
    return res


def usable(en, ku):
    if not en or not ku or "{" in en or "{" in ku or "%" in en or "<" in en or "&" in en:
        return False
    if len(re.sub(r"[^A-Za-z]", "", en)) < 3:
        return False
    if len(en.split()) > 4 or len(en) > 40 or not re.search("[\u0600-\u06FF]", ku):
        return False
    return not re.search("[A-Za-z]", ku)  # Kurdish side must be fully Kurdish script


def main():
    en, ku = strings(EN), strings(CKB)
    pairs = collections.defaultdict(collections.Counter)
    for key, e in en.items():
        k = ku.get(key)
        if k and usable(e, k):
            term = re.sub(r"[.…:]+$", "", e).strip()
            pairs[term.lower()][re.sub(r"[.…:]+$", "", k).strip().translate(check.CHAR_MAP)] += 1
    entries = check.compile_entries(json.loads(Path(
        r"C:\Users\awara\Desktop\Kurdish_Project\skills\kurdi-peti\references\glossary.json").read_text(encoding="utf-8"))["entries"], False)
    pure, loany = [], []
    for term, c in sorted(pairs.items()):
        ckb, n = c.most_common(1)[0]
        issues = [i for i in check.check_text(ckb, entries) if i["message"].startswith("وشەی")]
        (loany if issues else pure).append((term, ckb, n, ", ".join(i["word"] for i in issues)))
    print(f"en strings {len(en)}, ckb {len(ku)}, terms {len(pairs)}, pure {len(pure)}, with loanwords {len(loany)}")
    (HERE / "ui_pure.tsv").write_text("\n".join(f"{t}\t{k}" for t, k, _, _ in pure), encoding="utf-8")
    (HERE / "ui_loany.tsv").write_text("\n".join(f"{t}\t{k}\t{w}" for t, k, _, w in loany), encoding="utf-8")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
