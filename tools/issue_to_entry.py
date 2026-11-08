#!/usr/bin/env python3
"""پێشنیارێکی وشە (issue) دەکات بە ڕیزێکی نوێ لە glossary.json.

GitHub Actions بەکاری دەهێنێت کاتێک خاوەنی پڕۆژە نیشانەی «پەسەندکراو» دەخاتە سەر پێشنیارێک.
دەقی پێشنیارەکە لە گۆڕاوی ISSUE_BODY دەخوێنرێتەوە.

  ISSUE_BODY="..." python tools/issue_to_entry.py
"""
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_glossary import PATH, validate  # noqa: E402

# ناونیشانی خانەکانی فۆڕمی .github/ISSUE_TEMPLATE/new-word.yml
FIELDS = {
    "loan": "وشە بیانییەکە",
    "variants": "شێوەکانی تری نووسینی",
    "origin": "زمانی بنەڕەت",
    "pure": "وشە کوردییە پەتییەکان",
    "level": "ئاست",
    "source": "سەرچاوە",
}
ORIGIN_CODES = {"عەرەبی": "ar", "فارسی": "fa", "تورکی": "tr", "ئینگلیزی": "en"}
NO_ANSWER = {"", "_No response_", "None"}


def parse_form(body):
    sections, current = {}, None
    for line in body.replace("\r\n", "\n").split("\n"):
        heading = re.match(r"^###\s+(.*?)\s*$", line)
        if heading:
            current = heading.group(1)
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return {k: "\n".join(v).strip() for k, v in sections.items()}


def split_words(text):
    parts = re.split(r"[،,؛;\n]+", text or "")
    return [p.strip() for p in parts if p.strip() and p.strip() not in NO_ANSWER]


def build_entry(form):
    get = lambda key: form.get(FIELDS[key], "").strip()  # noqa: E731
    loan = get("loan")
    origin_text = get("origin")
    origin = next((code for name, code in ORIGIN_CODES.items() if name in origin_text), None)
    level = "strict" if "strict" in get("level") else "core"
    entry = {
        "loan": loan,
        "variants": split_words(get("variants")),
        "origin": origin,
        "pure": split_words(get("pure")),
        "level": level,
        "source": "community",
        "review": True,
    }
    note = get("source")
    if note and note not in NO_ANSWER:
        entry["note"] = note[:200]
    return entry


def write_glossary(data):
    lines = ["{", f'  "version": {json.dumps(data["version"])},',
             f'  "about": {json.dumps(data["about"], ensure_ascii=False)},', '  "entries": [']
    n = len(data["entries"])
    lines += ["    " + json.dumps(e, ensure_ascii=False) + ("," if i < n - 1 else "") for i, e in enumerate(data["entries"])]
    lines += ["  ]", "}"]
    PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    entry = build_entry(parse_form(os.environ.get("ISSUE_BODY", "")))
    data = json.loads(PATH.read_text(encoding="utf-8"))
    data["entries"].append(entry)
    errors, _ = validate(data)
    if errors:
        print("ئەم پێشنیارە ناتوانرێت زیاد بکرێت:")
        for e in errors:
            print(f"- {e}")
        return 1
    write_glossary(data)
    print(f"زیاد کرا: «{entry['loan']}» ← {'، '.join(entry['pure'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
