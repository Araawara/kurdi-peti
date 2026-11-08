#!/usr/bin/env python3
"""پشکنەری کوردیی پەتی: وشەی بیانی و هەڵەی ڕێنووس لە دەقی سۆرانیدا دەدۆزێتەوە.

Usage:
  python check.py FILE_OR_DIR ...     پشکنینی پەڕگە و بوخچەکان
  echo "دەق" | python check.py        پشکنینی دەق لە stdin
Options:
  --core-only   تەنها وشە بیانییە ئاشکراکان، بێ ئاستی توند (strict)
  --fix         ڕاستکردنەوەی خۆکاری پیتە هەڵەکان (ك ي ى ة ـ ه‌)
  --json        دەرئەنجام بە JSON
  --glossary    ڕێڕەوی glossary.json

Exit code: 1 if any [هەڵە] was found, else 0 (usable in CI).
"""
import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GLOSSARY_CANDIDATES = [
    HERE.parent / "references" / "glossary.json",
    HERE / "glossary.json",
    Path("/mnt/data/glossary.json"),  # ChatGPT Code Interpreter
]

# Arabic-script letters and marks, excluding punctuation (، ؛ ؟ ۔) and digits.
LETTERS = "ؠ-ٰٟ-ۓە-ۭۺ-ۿݐ-ݿﭐ-﷿ﹰ-﻿‌"
NOT_LETTER_BEFORE = f"(?<![{LETTERS}])"
NOT_LETTER_AFTER = f"(?![{LETTERS}])"

# Sorani suffixes and light verbs that may follow a loanword.
SUFFIXES = [
    "کردنەوە", "کردن", "کراو", "کرد", "بوون", "دان",
    "ەکانی", "ەکان", "ەکەی", "ەکە", "کانی", "کان", "کە",
    "یەکی", "یەک", "ێکی", "ێک", "مان", "تان", "یان",
    "ەوە", "وە", "دا", "ەی", "ان", "ی", "ە", "م", "ت", "ش", "ێ",
]  # no bare "ن": it turned loans into other words (بەحر+ەین = بەحرەین، سۆر+ین)
SUFFIX_RE = "(?:" + "|".join(SUFFIXES) + ")*"

ORIGINS = {"ar": "عەرەبی", "fa": "فارسی", "tr": "تورکی", "en": "ئینگلیزی"}

# Same-length replacements, so match positions stay valid.
CHAR_MAP = str.maketrans({"ك": "ک", "ي": "ی", "ى": "ی", "ة": "ە"})

CHAR_RULES = [
    (re.compile("ك"), "ک", "«ك»ی عەرەبی ← «ک»ی کوردی"),
    (re.compile("[يى]"), "ی", "«ي/ى»ی عەرەبی ← «ی»ی کوردی"),
    (re.compile("ة"), "ە", "«ة» ← «ە»"),
    (re.compile("ه‌"), "ە", "«ه» + ZWNJ ← «ە»"),
    (re.compile("ـ"), "", "کێشیدە (ـ) لاببە"),
]
STYLE_RULES = [
    (re.compile(f"{NOT_LETTER_BEFORE}ر"), "وشە بە «ر» دەست پێناکات ← «ڕ»"),
    (re.compile(f"ه{NOT_LETTER_AFTER}"), "کۆتایی وشە بە «ه»: ئەگەر دەنگی «ە»یە، «ە» بنووسە"),
    (re.compile("ھ"), "«ھ» ← «ه»"),
    (re.compile(f"(?<=[{LETTERS}])\\s?\\?"), "«?» ← «؟»"),
    (re.compile(f"(?<=[{LETTERS}]),"), "«,» ← «،»"),
    (re.compile(f"(?<=[{LETTERS}]);"), "«;» ← «؛»"),
]

TEXT_EXT = {
    ".txt", ".md", ".mdx", ".html", ".htm", ".xml", ".svg", ".json", ".yaml", ".yml",
    ".toml", ".ini", ".csv", ".po", ".pot", ".arb", ".strings", ".properties",
    ".py", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".css", ".scss",
    ".java", ".kt", ".swift", ".dart", ".go", ".rs", ".rb", ".php", ".cs", ".c",
    ".cpp", ".h", ".sql", ".sh",
}
SKIP_DIRS = {".git", "node_modules", "dist", "build", "__pycache__", ".venv", "venv", ".next"}
SKIP_FILES = {"glossary.json", "glossary.md"}
IGNORE_MARK = "kurdi-peti-ignore"  # ignores this line; -start / -end ignore a block


def load_glossary(path=None):
    candidates = [Path(path)] if path else GLOSSARY_CANDIDATES
    for p in candidates:
        if p.is_file():
            return json.loads(p.read_text(encoding="utf-8"))["entries"]
    sys.exit("glossary.json نەدۆزرایەوە. --glossary بەکاربهێنە.")


def compile_entries(entries, core_only):
    compiled = []
    for e in entries:
        if core_only and e["level"] != "core":
            continue
        forms = sorted({e["loan"], *e.get("variants", [])}, key=len, reverse=True)
        alt = "|".join(re.escape(f).replace("\\ ", "[\\s‌]?") for f in forms)
        suffix = "" if e.get("exact") else SUFFIX_RE  # exact: no suffixes allowed
        pattern = re.compile(f"{NOT_LETTER_BEFORE}(?:{alt}){suffix}{NOT_LETTER_AFTER}")
        compiled.append((pattern, e))
    # Longest loanword first, so «مەسەلەن» wins over «مەسەلە» + suffix.
    compiled.sort(key=lambda c: len(c[1]["loan"]), reverse=True)
    return compiled


def check_text(text, entries):
    issues = []
    ignoring = False
    for lineno, raw in enumerate(text.splitlines(), 1):
        if IGNORE_MARK + "-start" in raw:
            ignoring = True
        if IGNORE_MARK + "-end" in raw:
            ignoring = False
            continue
        if ignoring or IGNORE_MARK in raw:
            continue
        line = raw.translate(CHAR_MAP)
        for rx, _, msg in CHAR_RULES:
            for m in rx.finditer(raw):
                issues.append(dict(line=lineno, col=m.start() + 1, kind="هەڵە", word=m.group(), message=msg))
        for rx, msg in STYLE_RULES:
            for m in rx.finditer(line):
                issues.append(dict(line=lineno, col=m.start() + 1, kind="پێشنیار", word=m.group().strip(), message=msg))
        taken = set()
        for rx, e in entries:
            for m in rx.finditer(line):
                if m.start() in taken:
                    continue
                taken.add(m.start())
                kind = "هەڵە" if e["level"] == "core" else "پێشنیار"
                msg = f"وشەی {ORIGINS.get(e['origin'], e['origin'])} ← " + " یان ".join(f"«{p}»" for p in e["pure"])
                issues.append(dict(line=lineno, col=m.start() + 1, kind=kind, word=m.group(), message=msg))
    issues.sort(key=lambda i: (i["line"], i["col"]))
    return issues


def fix_text(text):
    for rx, repl, _ in CHAR_RULES:
        text = rx.sub(repl, text)
    return text


def iter_files(paths):
    for p in map(Path, paths):
        if p.is_file():
            yield p
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if (f.is_file() and f.suffix.lower() in TEXT_EXT and f.name not in SKIP_FILES
                        and not SKIP_DIRS.intersection(f.parts)):
                    yield f


def main():
    for stream in (sys.stdout, sys.stdin):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="پشکنەری کوردیی پەتی")
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--core-only", action="store_true")
    ap.add_argument("--fix", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--glossary")
    args = ap.parse_args()

    entries = compile_entries(load_glossary(args.glossary), args.core_only)
    sources = []
    if args.paths:
        for f in iter_files(args.paths):
            try:
                sources.append((str(f), f.read_text(encoding="utf-8")))
            except (UnicodeDecodeError, OSError):
                continue
    else:
        sources.append(("<stdin>", sys.stdin.read()))

    report = {}
    for name, text in sources:
        if args.fix:
            fixed = fix_text(text)
            if name == "<stdin>":
                print(fixed, end="")
            elif fixed != text:
                Path(name).write_text(fixed, encoding="utf-8")
            text = fixed
        issues = check_text(text, entries)
        if issues:
            report[name] = issues

    errors = sum(i["kind"] == "هەڵە" for v in report.values() for i in v)
    hints = sum(i["kind"] == "پێشنیار" for v in report.values() for i in v)

    if args.json:
        print(json.dumps({"errors": errors, "suggestions": hints, "files": report}, ensure_ascii=False, indent=2))
    elif not (args.fix and not args.paths):
        for name, issues in report.items():
            for i in issues:
                print(f"{name}:{i['line']}:{i['col']}  [{i['kind']}] «{i['word']}»  {i['message']}")
        print(f"\nکۆی گشتی: {errors} هەڵە، {hints} پێشنیار." if report else "✓ هیچ کێشەیەک نەدۆزرایەوە. دەقەکە کوردیی پەتییە.")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
