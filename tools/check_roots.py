#!/usr/bin/env python3
"""<!-- kurdi-peti-ignore-start -->
پشکنینی ڕەگی بیانی لە ناو وشە «پەتی»یەکانی فەرهەنگدا.

بۆ هەر وشەیەکی پەتی، پاشگر و پێشگرە کوردییەکان لادەبات و دەپشکنێت:
  ١. ئایا ڕەگەکە خۆی وشەیەکی بیانیی ناو فەرهەنگە؟ (بۆ نموونە «خزمەت» لە «خزمەتگوزاری»دا)
  ٢. ئایا بە یەکێک لە ڕەگەکانی foreign_roots.tsv دەست پێدەکات؟ (بۆ نموونە «دەوڵەمەندی»)
وشەی هەڵە نییە کە بە ڕێکەوت وەک ڕەگێکی بیانی دەردەکەوێت: بیخەرە ناو root_exceptions.txt.

  python tools/check_roots.py              ڕاپۆرت بە کوردی
  python tools/check_roots.py --json       ئەنجام بە JSON
  python tools/check_roots.py --strict     کۆدی دەرچوون 1 ئەگەر هەڵەیەک دۆزرایەوە
<!-- kurdi-peti-ignore-end -->
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REFS = ROOT / "skills" / "kurdi-peti" / "references"
CHAR_MAP = str.maketrans({"ك": "ک", "ي": "ی", "ى": "ی", "ة": "ە", "ـ": "", "‌": ""})

# پاشگرە کوردییەکان، درێژترین یەکەم
SUFFIXES = sorted("""ییەکانەوە ییەکان ییەکە یەکان یەتی ایەتی ێتی کردنەوە کردن کراو بوونەوە بوون
ەکانەوە ەکان ەکە کانەوە کان کە ەوە انە ان ەیی یی ی دار مەند گوزاری گوزار کار کاری گەر گەری گا خانە ستان
نامە ناسی ناس وان وانی پەروەر پەروەری خواز خوازی باز بازی گیر گیری دەر""".split(), key=len, reverse=True)
PREFIXES = ["نا", "بێ", "هاو", "نە"]


def load_lines(path):
    if not path.exists():
        return []
    return [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]


def stems(token):
    """هەموو ڕەگە گونجاوەکانی وشەیەک، بە لابردنی پاشگر و پێشگر."""
    found, todo = set(), [token]
    while todo:
        w = todo.pop()
        if w in found or len(w) < 2:
            continue
        found.add(w)
        for s in SUFFIXES:
            if w.endswith(s) and len(w) - len(s) >= 2:
                todo.append(w[: -len(s)])
        for p in PREFIXES:
            if w.startswith(p) and len(w) - len(p) >= 3:
                todo.append(w[len(p):])
    return found


def main():
    glossary = json.loads((REFS / "glossary.json").read_text(encoding="utf-8"))["entries"]
    roots = {}
    for line in load_lines(REFS / "foreign_roots.tsv")[1:]:
        parts = (line.split("\t") + ["", ""])[:3]
        roots[parts[0].translate(CHAR_MAP)] = (parts[1], parts[2])
    exceptions = {w.translate(CHAR_MAP) for w in load_lines(REFS / "root_exceptions.txt")}
    loans = {}
    for e in glossary:
        for f in [e["loan"], *e.get("variants", [])]:
            f = f.translate(CHAR_MAP)
            if len(f) >= 3 and " " not in f:
                loans.setdefault(f, e)

    findings = []
    for e in glossary:
        for pure in e["pure"]:
            for token in pure.translate(CHAR_MAP).split():
                token_stems = stems(token)
                if token in exceptions or token_stems & exceptions:
                    continue
                hit = None
                own = {e["loan"].translate(CHAR_MAP), *(v.translate(CHAR_MAP) for v in e.get("variants", []))}
                for st in sorted(token_stems, key=len):
                    if st in own:
                        hit = (st, "هەڵە", "وشە بیانییەکە خۆی لە ناو جێگرەوەکەیدایە", "")
                        break
                    if st in loans:
                        src = loans[st]
                        level = "هەڵە" if src["level"] == "core" else "ئاگاداری"
                        hit = (st, level, f"وشەی بیانیی ناو فەرهەنگە ({src['origin']}، {src['level']})",
                               "، ".join(src["pure"]))
                        break
                if not hit:
                    for r, (origin, better) in roots.items():
                        if token.startswith(r) or r in token_stems:
                            hit = (r, "ئاگاداری", f"ڕەگی بیانی ({origin})", better)
                            break
                if hit:
                    findings.append({"loan": e["loan"], "pure": pure, "token": token, "root": hit[0],
                                     "level": hit[1], "why": hit[2], "better": hit[3],
                                     "review": bool(e.get("review"))})

    if "--json" in sys.argv:
        print(json.dumps(findings, ensure_ascii=False, indent=1))
    else:
        findings.sort(key=lambda f: (f["level"] != "هەڵە", f["loan"]))
        for f in findings:
            tip = f" ← بیر لە «{f['better']}» بکەرەوە" if f["better"] else ""
            print(f"[{f['level']}] «{f['loan']}» ← «{f['pure']}»: «{f['root']}» {f['why']}{tip}")
        errors = sum(1 for f in findings if f["level"] == "هەڵە")
        print(f"\n{errors} هەڵە و {len(findings) - errors} ئاگاداری، لە {len(glossary)} ڕیز.")
    return 1 if "--strict" in sys.argv and any(f["level"] == "هەڵە" for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
