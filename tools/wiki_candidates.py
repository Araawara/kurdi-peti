"""وشە بیانییە گوماناوییەکان لە ویکیپیدیای کوردی (ckbwiki dump) دەدۆزێتەوە.

Only word counts are kept; article text is never stored or published.

python tools/wiki_candidates.py data/wiki/ckbwiki.xml.bz2  ->  data/wiki/wiki_candidates.tsv
"""
import bz2
import collections
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check", ROOT / "skills" / "kurdi-peti" / "scripts" / "check.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

WORD = re.compile(f"[{check.LETTERS}]+")
NORM = str.maketrans({"ك": "ک", "ي": "ی", "ى": "ی", "ة": "ە", "ـ": None, "‌": None})
SUFFIXES = sorted(set(check.SUFFIXES) - {"ش", "م", "ت", "ێ"}, key=len, reverse=True)
ARABIC_ONLY = set("صضطظثذءأإؤ")
ARABIC_HINT = set("عحق")
PATTERNS = [
    re.compile(r"^مو.{3,}"),
    re.compile(r"^(ئیستی|ئینتی|ئیجتی|ئیحتی|ئیعتی|ئیقتی|ئیفتی|ئیلتی|ئیرتی)"),
    re.compile(r"^تە.{2,}(ی|وق|ول|ور|یل|یر|یس|یق|یب|یم|ید)$"),
    re.compile(r"^(?!ئە|دە|نا|ب|دەر|ڕۆژ).{3,}(یەت|ات)$"),
    re.compile(r"^مە.{3,}(وو.)$"),
    re.compile(r".{4,}(ەتەن|یەن)$"),
]
# English loans written in Kurdish script often end like these
EN_PATTERNS = [re.compile(r".{3,}(یشن|ەیشن|ێشن|لۆژی|لۆجی|ۆگرافی|ئیزم|یزم|یک|ێک)$")]


def stem(w):
    for _ in range(3):
        for s in SUFFIXES:
            if w.endswith(s) and len(w) - len(s) >= 3:
                w = w[: -len(s)]
                break
        else:
            break
    return w


def reason(w):
    if ARABIC_ONLY & set(w):
        return "arabic-letter"
    if any(rx.search(w) for rx in PATTERNS):
        return "arabic-pattern"
    if any(rx.search(w) for rx in EN_PATTERNS):
        return "english-pattern"
    if ARABIC_HINT & set(w):
        return "ع/ح/ق"
    return ""


def texts(path):
    """Yield article wikitext from the dump, skipping markup-heavy parts."""
    buf, inside = [], False
    with bz2.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if "<text" in line:
                inside = True
            if inside:
                buf.append(line)
            if "</text>" in line:
                inside = False
                text = "".join(buf)
                buf = []
                text = re.sub(r"\{\{.*?\}\}|\[\[(?:[^|\]]*\|)?|\]\]|<[^>]+>|&[a-z]+;", " ", text, flags=re.S)
                yield text


def main(dump):
    counts = collections.Counter()
    for n, t in enumerate(texts(dump), 1):
        for w in WORD.findall(t.translate(NORM)):
            if len(w) > 2:
                counts[w] += 1
        if n % 20000 == 0:
            print(f"{n} وتار", flush=True)
    stems, forms = collections.Counter(), collections.defaultdict(collections.Counter)
    for w, c in counts.items():
        s = stem(w)
        stems[s] += c
        forms[s][w] += c
    entries = json.loads((ROOT / "skills" / "kurdi-peti" / "references" / "glossary.json").read_text(encoding="utf-8"))["entries"]
    known = {f for e in entries for f in [e["loan"], *e.get("variants", [])]} | {p for e in entries for p in e["pure"]}
    compiled = check.compile_entries(entries, False)
    rejected = set()
    rp = ROOT / "data" / "rejected.txt"
    if rp.exists():
        rejected = {w.strip() for w in rp.read_text(encoding="utf-8").splitlines()}
    out = []
    for s, c in stems.most_common():
        if c < 15:
            break
        top = forms[s].most_common(1)[0][0]
        r = reason(s)
        if not r or s in known or top in known or s in rejected or top in rejected:
            continue
        if any(rx.fullmatch(top) for rx, _ in compiled):
            continue
        out.append(f"{s}\t{c}\t{r}\t{top}")
    dest = Path(dump).with_name("wiki_candidates.tsv")
    dest.write_text("stem\tfreq\treason\texample\n" + "\n".join(out) + "\n", encoding="utf-8")
    print(f"words {sum(counts.values()):,}  unique {len(counts):,}  candidates {len(out):,} -> {dest}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1])
