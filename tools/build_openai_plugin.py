#!/usr/bin/env python3
"""دروستکردنی پاکێجی ZIP بۆ فەرهەنگی پێوەکراوەکانی ChatGPT (platform.openai.com/plugins).

  python tools/build_openai_plugin.py

Output: chatgpt/kurdi-peti-openai.zip
"""
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "chatgpt" / "openai-plugin"
OUT = ROOT / "chatgpt" / "kurdi-peti-openai.zip"


def main():
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SRC.rglob("*")):
            if f.is_file():
                z.write(f, f.relative_to(SRC))
    print(OUT, OUT.stat().st_size)


if __name__ == "__main__":
    main()
