#!/usr/bin/env python3
"""پشکنینی پەڕگەی glossary.json پێش پەسەندکردنی هەر گۆڕانکارییەک.

  python tools/validate_glossary.py

ئەگەر هەڵە هەبێت، کۆدی دەرچوون 1 دەبێت.
"""
import json
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "skills" / "kurdi-peti" / "references" / "glossary.json"
ORIGINS = {"ar", "fa", "tr", "en"}
LEVELS = {"core", "strict"}
KEYS = {"loan", "variants", "origin", "pure", "level", "review", "note", "source", "exact"}
BAD_CHARS = {"ك": "ک", "ي": "ی", "ى": "ی", "ة": "ە", "ـ": ""}


def word_problems(word):
    found = []
    if not isinstance(word, str) or not word.strip():
        return ["بەتاڵە"]
    if word != word.strip():
        found.append("بۆشایی لە سەرەتا یان کۆتاییدا")
    for ch, good in BAD_CHARS.items():
        if ch in word:
            found.append(f"پیتی «{ch}» ← «{good}»" if good else "کێشیدە (ـ)")
    for part in word.split():
        if part.startswith("ر"):
            found.append(f"«{part}» بە «ر» دەست پێدەکات ← «ڕ»")
    return found


def validate(data):
    errors, warnings = [], []
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        return ["پەڕگەکە دەبێت بەشی «entries» ی تێدا بێت"], warnings
    seen = {}
    for i, e in enumerate(entries, 1):
        where = f"ڕیزی {i}"
        if not isinstance(e, dict):
            errors.append(f"{where}: دەبێت object بێت")
            continue
        loan = e.get("loan")
        where = f"ڕیزی {i} («{loan}»)"
        extra = set(e) - KEYS
        if extra:
            errors.append(f"{where}: کلیلی نەناسراو: {', '.join(sorted(extra))}")
        if not isinstance(loan, str) or not loan.strip():
            errors.append(f"{where}: «loan» پێویستە")
            continue
        if e.get("origin") not in ORIGINS:
            errors.append(f"{where}: «origin» دەبێت یەکێک بێت لە {sorted(ORIGINS)}")
        if e.get("level") not in LEVELS:
            errors.append(f"{where}: «level» دەبێت core یان strict بێت")
        pure = e.get("pure")
        if not isinstance(pure, list) or not pure:
            errors.append(f"{where}: «pure» دەبێت لیستێکی پڕ بێت")
            pure = []
        variants = e.get("variants", [])
        if not isinstance(variants, list):
            errors.append(f"{where}: «variants» دەبێت لیست بێت")
            variants = []
        for flag in ("review", "exact"):
            if flag in e and not isinstance(e[flag], bool):
                errors.append(f"{where}: «{flag}» دەبێت true یان false بێت")
        for text_key in ("source", "note"):
            if text_key in e and not isinstance(e[text_key], str):
                errors.append(f"{where}: «{text_key}» دەبێت دەق بێت")
        for w in pure:
            for p in word_problems(w):
                errors.append(f"{where}: وشەی پەتی «{w}»: {p}")
        if len(set(pure)) != len(pure):
            errors.append(f"{where}: وشەی پەتیی دووبارە")
        for form in [loan, *variants]:
            if not isinstance(form, str) or not form.strip():
                errors.append(f"{where}: شێوەی بەتاڵ")
                continue
            if form in seen:
                errors.append(f"{where}: «{form}» پێشتر لە {seen[form]} هەیە")
            else:
                seen[form] = where
    for i, e in enumerate(entries, 1):
        if isinstance(e, dict):
            for w in e.get("pure") or []:
                if w in seen:
                    warnings.append(f"ڕیزی {i} («{e.get('loan')}»): وشەی پەتی «{w}» خۆی وەک وشەی بیانی تۆمار کراوە ({seen[w]})")
    return errors, warnings


def main():
    try:
        data = json.loads(PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[هەڵە] glossary.json دروست نییە: ڕیز {exc.lineno}، ستوون {exc.colno}: {exc.msg}")
        return 1
    errors, warnings = validate(data)
    for w in warnings:
        print(f"[ئاگاداری] {w}")
    for e in errors:
        print(f"[هەڵە] {e}")
    print(f"\n{len(data.get('entries', []))} وشە · {len(errors)} هەڵە · {len(warnings)} ئاگاداری")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
